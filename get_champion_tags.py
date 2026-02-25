import json
from riotwatcher import LolWatcher

#Key not needed, its public
watcher = LolWatcher('dummy_api_key')

print("Fetching latest game version...")
versions = watcher.data_dragon.versions_for_region('na1')
champion_version = versions['n']['champion']

print(f"Downloading champion data for patch {champion_version}...")
champion_data = watcher.data_dragon.champions(champion_version)

champ_dict = champion_data['data']
champion_tags = {}

print("Extracting champion tags...")

for champ_name, champ_info in champ_dict.items():
    champ_id = int(champ_info['key'])
    tags = champ_info['tags']
    champion_tags[champ_id] = {
        'name': champ_info['name'],
        'tags': tags
    }

with open('champion_tags.json', 'w') as f:
    json.dump(champion_tags, f, indent=4)

print(f"Saved champion tags for {len(champion_tags)} champions to champion_tags.json")
