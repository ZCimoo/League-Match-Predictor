import os
from dotenv import load_dotenv
from riotwatcher import LolWatcher, RiotWatcher, ApiError
import pandas as pd
import time

load_dotenv()

api_key = os.getenv('RIOT_API_KEY')

if not api_key:
    raise ValueError("RIOT_API_KEY not found in environment variables")

riot_watcher = RiotWatcher(api_key)
lol_watcher = LolWatcher(api_key)

my_region = 'americas'

game_name = 'Bee'
tag_line = '0928'

try:
    me = riot_watcher.account.by_riot_id(my_region, game_name, tag_line)
    print(f"Success! Found PUUID: {me['puuid']}")

except ApiError as err:
    print(f"Failed to connect: {err}")

print(f"Searching for matches in region {my_region}")

queue_type=420
count=5

try:
    match_ids = lol_watcher.match.matchlist_by_puuid(region=my_region, 
                                                      puuid=me['puuid'], 
                                                      queue=queue_type, 
                                                      count=count
                                                      )
    print(f"Successfully retrieved {len(match_ids)} match IDs.")
    print(f"Example Match ID: {match_ids[0]}")
except ApiError as err:
    print(f"Failed to retrieve match IDs: {err}")

print(f"Starting to scrape {len(match_ids)} matches...")

match_data = []

for match_id in match_ids:
    try:
        match_detail = lol_watcher.match.by_id(my_region, match_id)
        participants = match_detail['info']['participants']

        row = {}
        row['match_id'] = match_id

        for i, player in enumerate(participants):
            row[f'player_{i}_champ'] = player['championId']
            row[f'player{i}_team'] = player['teamId']
            row['blue_win'] = 1 if participants[0]['win'] else 0
        
        match_data.append(row)
        print(f"Successfully scraped match ID: {match_id}")

        time.sleep(1.0)  # Sleep to respect rate limits

    except ApiError as err:
        if err.response.status_code == 429:
            print("Rate limit exceeded. Sleeping for 10 seconds...")
            time.sleep(10)
        else:
            print(f"Failed to scrape match ID {match_id}: {err}")

df = pd.DataFrame(match_data)
df.to_csv('league_data.csv', index=False)

print("Data scraping complete. Saved to league_data.csv")