import requests
import urllib3
import time
import json
import pandas as pd
import joblib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LIVE_CLIENT_URL = "https://127.0.0.1:2999/liveclientdata/allgamedata"

print("Loading Machine Leanrning model and champion data...")
#Load pre-trained model and champion data
draft_model = joblib.load('draft_model.pkl')

with open('champion_tags.json', 'r') as f:
    champ_data = json.load(f)

with open('champion_winrates.json', 'r') as f:
    champ_winrates = json.load(f)

#To map champ names to ids call data dragon 
ddragon_url = "https://ddragon.leagueoflegends.com/cdn/14.4.1/data/en_US/champion.json"
champ_mapping_data = requests.get(ddragon_url).json()['data']
name_to_id = {}
for champ_name, data in champ_mapping_data.items():
    name_to_id[data['name']] = data['key']


def calculate_live_win_probability(baseline_prob, blue_stats, red_stats):
    #Takes pregame probability we predicted and adjusts based on live game economy
    #blue_stats and red_stats are dicts with keys like 'kills', 'dragons', 'barons', 'cs', etc.
    #I am approximating gold for each stat

    blue_gold = (
        (blue_stats['kills'] * 300) +
        (blue_stats['assists'] * 150) +
        (blue_stats['cs'] * 20) +
        (blue_stats['dragons'] * 500) +
        (blue_stats['barons'] * 1500)
    )

    red_gold = (
        (red_stats['kills'] * 300) +
        (red_stats['assists'] * 150) +
        (red_stats['cs'] * 20) +
        (red_stats['dragons'] * 500) +
        (red_stats['barons'] * 1500)
    )

    gold_diff = blue_gold - red_gold
    #Adjust baseline probability based on gold difference
    #Every 100 gold lead shifts probability by 0.2% (1000 gold diff = 2%)
    #"+" gold diff favors blue team, "-" gold diff favors red team
    prob_adjustment = (gold_diff / 100) * 0.002
    live_prob = baseline_prob + prob_adjustment

    #Cap live probability between 0.1% and 99.9% 
    live_prob = max(0.001, min(0.999, live_prob))

    return live_prob, gold_diff

ROLES = ['Fighter', 'Tank', 'Assassin', 'Mage', 'Marksman', 'Support']

def get_draft_baseline(blue_team_champs, red_team_champs):
    features = {}
    for role in ROLES:
        features[f'blue_{role}'] = 0
        features[f'red_{role}'] = 0

    blue_team_total_wr = 0.0
    red_team_total_wr = 0.0

    for champ_name in blue_team_champs:
        champ_id = name_to_id.get(champ_name, "0")

        blue_team_total_wr += champ_winrates.get(champ_id, 0.50)

        if champ_id in champ_data:
            for tag in champ_data[champ_id]['tags']:
                features[f'blue_{tag}'] += 1
    
    for champ_name in red_team_champs:
        champ_id = name_to_id.get(champ_name, "0")

        red_team_total_wr += champ_winrates.get(champ_id, 0.50)

        if champ_id in champ_data:
            for tag in champ_data[champ_id]['tags']:
                features[f'red_{tag}'] += 1
    
    features['blue_avg_winrate'] = blue_team_total_wr / 5.0
    features['red_avg_winrate'] = red_team_total_wr / 5.0

    df_features = pd.DataFrame([features])

    win_probability = draft_model.predict(df_features)[0] #Probability of blue team win

    return win_probability



def get_live_match_data():
    try:

        blue_team_champs = []
        red_team_champs = []

        response = requests.get(LIVE_CLIENT_URL, verify=False)

        if response.status_code == 200:
            data = response.json()
            game_time = data['gameData']['gameTime']

            #convert format of game time to minutes and seconds
            minutes = int(game_time // 60)
            seconds = int(game_time % 60)

            print(f"Game time: {minutes}:{seconds:02d}")

            player_teams = {}

            #Initialize kill count
            blue_team_kills,red_team_kills = 0, 0
            blue_team_assists, red_team_assists = 0, 0
            blue_team_cs, red_team_cs = 0, 0
            

            print("Live Player Stats:")
            for player in data['allPlayers']:
                raw_name = player['summonerName']

                #Strip #Tagline from name
                clean_name = raw_name.split('#')[0].strip()

                team = player['team'] #ORDER = blue team, CHAOS = red team
                player_teams[clean_name] = team
                level = player['level']

                champ_name = player['championName']

                kills = player['scores']['kills']
                deaths = player['scores']['deaths']
                assists = player['scores']['assists']
                cs = player['scores']['creepScore']

                if team == "ORDER":
                    blue_team_kills += kills
                    blue_team_assists += assists
                    blue_team_cs += cs
                    blue_team_champs.append(champ_name)
                elif team == "CHAOS":
                    red_team_kills += kills
                    red_team_assists += assists
                    red_team_cs += cs
                    red_team_champs.append(champ_name)
                
                print (f"{raw_name} | Team: {team} | Level: {level} | Kills: {kills} | Deaths: {deaths} | Assists: {assists} | CS: {cs}")


            
            print(f"\nBlue Team Champions: {blue_team_champs}")
            print(f"Red Team Champions: {red_team_champs}")

            # Initialize dragon and baron count
            blue_dragons, red_dragons = 0, 0
            blue_barons, red_barons = 0, 0
            

            #List of events since the game started
            events = data['events']['Events']

            for event in events:
                event_name = event['EventName']

                #Check if event is a monster kill (objective)
                if event_name in ["DragonKill", "BaronKill"]:
                    raw_killer = event.get('KillerName','')

                    clean_killer = raw_killer.split('#')[0].strip()

                    team = player_teams.get(clean_killer, "Unknown")

                    if event_name == "DragonKill":
                        if team == "ORDER":
                            blue_dragons += 1
                        elif team == "CHAOS":
                            red_dragons += 1
                    elif event_name == "BaronKill":
                        if team == "ORDER":
                            blue_barons += 1
                        elif team == "CHAOS":
                            red_barons += 1

            blue_stats = {
                'kills': blue_team_kills,
                'assists': blue_team_assists,
                'cs': blue_team_cs,
                'dragons': blue_dragons,
                'barons': blue_barons
            }

            red_stats = {
                'kills': red_team_kills,
                'assists': red_team_assists,
                'cs': red_team_cs,
                'dragons': red_dragons,
                'barons': red_barons
            }

            baseline_prob = get_draft_baseline(blue_team_champs, red_team_champs)

            live_prob, gold_diff = calculate_live_win_probability(baseline_prob, blue_stats, red_stats)

            print("\n--- Live Prediction ---")
            print(f"Estimated Gold Difference: {gold_diff} (Positive favors Blue, Negative favors Red)")
            print(f"Live Win Probability for Blue Team: {live_prob*100:.1f}%")
            return True
        
        elif response.status_code == 404:
            print(f"Game found but no live data available yet (Loading screen).")
            return False
        
    except requests.exceptions.ConnectionError:
        print("Not currently in a game or unable to connect to live client data.")
        return False
    
print("Starting live match data tracker...")
while True:
    success = get_live_match_data()

    time.sleep(5)