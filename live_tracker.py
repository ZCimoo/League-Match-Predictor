import requests
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LIVE_CLIENT_URL = "https://127.0.0.1:2999/liveclientdata/allgamedata"

def get_live_match_data():
    try:

        response = requests.get(LIVE_CLIENT_URL, verify=False)

        if response.status_code == 200:
            data = response.json()
            game_time = data['gameData']['gameTime']

            #convert format of game time to minutes and seconds
            minutes = int(game_time // 60)
            seconds = int(game_time % 60)

            print(f"Game time: {minutes}:{seconds:02d}")

            #Initialize kill count
            blue_team_kills = 0
            red_team_kills = 0

            print("Live Player Stats:")
            for players in data['allPlayers']:
                name = players['summonerName']
                team = players['team'] #ORDER = blue team, CHAOS = red team
                level = players['level']

                kills = players['scores']['kills']
                deaths = players['scores']['deaths']
                assists = players['scores']['assists']
                cs = players['scores']['creepScore']

                if team == "ORDER":
                    blue_team_kills += kills
                elif team == "CHAOS":
                    red_team_kills += kills
                
                print (f"{name} | Team: {team} | Level: {level} | Kills: {kills} | Deaths: {deaths} | Assists: {assists} | CS: {cs}")

            print(f"Blue Team Kills: {blue_team_kills} | Red Team Kills: {red_team_kills}")
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