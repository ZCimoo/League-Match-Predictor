import os
import time
import pandas as pd
from dotenv import load_dotenv
from riotwatcher import LolWatcher, RiotWatcher, ApiError

load_dotenv()
api_key = os.getenv('RIOT_API_KEY')
watcher = LolWatcher(api_key)

platform = 'na1'

print(f"Fetching Challenger players for region {platform}...")

try:
    challenger_players = watcher.league.challenger_by_queue(platform, 'RANKED_SOLO_5x5')
   
    entries = challenger_players['entries']
    print(f"Successfully retrieved {len(entries)} challenger players.")

    entries.sort(key=lambda x: x['leaguePoints'], reverse=True)

    top_50 = entries[:50]

    player_data = []

    print("Extracting PUUIDs...")

    for i, entry in enumerate(top_50):
        
        player_data.append({
            'puuid': entry['puuid'],
            'lp': entry['leaguePoints'],
            'wins': entry['wins'],
            'losses': entry['losses'],
        })

    df = pd.DataFrame(player_data)
    df.to_csv('challenger_players.csv', index=False)
    print("Saved player data to challenger_players.csv")

except ApiError as err:
    print(f"Critical Error: {err}")