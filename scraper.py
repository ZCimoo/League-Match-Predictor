import os
from dotenv import load_dotenv
from riotwatcher import LolWatcher, RiotWatcher, ApiError
import pandas as pd
import time

load_dotenv()

api_key = os.getenv('RIOT_API_KEY')

riot_watcher = RiotWatcher(api_key)
lol_watcher = LolWatcher(api_key)

my_region = 'americas'
queue_type = 420
count = 80

try:
    player_df = pd.read_csv('challenger_players.csv')
    target_puuids = player_df['puuid'].tolist()
    print(f"Loaded {len(target_puuids)} player PUUIDs from challenger_players.csv")
except FileNotFoundError:
    print("Error: challenger_players.csv not found. Please run get_players.py first.")
    exit()

match_data = []
visited_match_ids = set()

print("Starting match scraping...")

try:
    for i, puuid in enumerate(target_puuids):
        print(f"Processing player {i+1}/{len(target_puuids)}: {puuid}")
        try:
            matches = lol_watcher.match.matchlist_by_puuid(my_region, 
                                                           puuid, 
                                                           queue=queue_type, 
                                                           count=count)
            
            print(f"  Found {len(matches)} matches for player {puuid}")
            for match_id in matches:
                if match_id in visited_match_ids:
                    continue

                try:
                    match_details = lol_watcher.match.by_id(my_region, match_id)
                    participants = match_details['info']['participants']

                    row = {'match_id': match_id,}

                    for p_index, player in enumerate(participants):
                        row[f'player_{p_index}_champ'] = player['championId']
                        row[f'player_{p_index}_team'] = player['teamId']

                    blue_win = False
                    for player in participants:
                        if player['teamId'] == 100 and player['win']:
                            blue_win = True
                            break
                    row['blue_win'] = 1 if blue_win else 0

                    match_data.append(row)
                    visited_match_ids.add(match_id)
                    print(f"  Processed match {match_id} | Total matches collected: {len(match_data)}")

                    time.sleep(1.2)

                except ApiError as err:
                    if err.response.status_code == 429:
                        print("Rate limit hit. Sleeping for 10 seconds...")
                        time.sleep(10)
                    else:
                        print(f"Error fetching match {match_id}: {err}")

        except ApiError as err:
            print(f"Error fetching matches for player {puuid}: {err}")
        
        if(i+1) % 5 == 0:
            backup_df = pd.DataFrame(match_data)
            backup_df.to_csv('match_data_backup.csv', index=False)
            print(f"Saved backup after processing {i+1} players. Total matches collected: {len(match_data)}")

except KeyboardInterrupt:
    print("Scraping interrupted by user.")

finally:
    if len(match_data) > 0:
        df = pd.DataFrame(match_data)
        df.to_csv('match_data.csv', index=False)
        print(f"Saved {len(match_data)} matches to match_data.csv")
    else:
        print("No match data collected.")
           


