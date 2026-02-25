import pandas as pd
import json

print("Loading match data...")
df= pd.read_csv('match_data.csv')
df = df.dropna()

champ_stats = {}

# Calculate wins and games for each champion
for index, row in df.iterrows():
    blue_won = row['blue_win'] == 1

    for i in range(5):
        champ_id = str(int(row[f"player_{i}_champ"]))
        if champ_id not in champ_stats:
            champ_stats[champ_id] = {'wins': 0, 'games': 0}
        champ_stats[champ_id]['games'] += 1

        if blue_won:
            champ_stats[champ_id]['wins'] += 1

    for i in range(5, 10):
        champ_id = str(int(row[f"player_{i}_champ"]))
        if champ_id not in champ_stats:
            champ_stats[champ_id] = {'wins': 0, 'games': 0}
        champ_stats[champ_id]['games'] += 1

        if not blue_won:
            champ_stats[champ_id]['wins'] += 1

# Calculate win rates
champ_winrates = {}

for champ_id, stats in champ_stats.items():
    # Prevents 1-game win rates from skewing data
    if stats['games'] > 30:
        champ_winrates[champ_id] = stats['wins'] / stats['games']
    else:
        champ_winrates[champ_id] = 0.50

with open('champion_winrates.json', 'w') as f:
    json.dump(champ_winrates, f, indent=4)

print("Champion win rates calculated and saved to champion_winrates.json")
    