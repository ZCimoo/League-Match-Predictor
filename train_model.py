import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import lightgbm as lgb

df= pd.read_csv('match_data.csv')
print(f"Loaded {len(df)} rows of match data")

df = df.dropna()

with open('champion_tags.json', 'r') as f:
    champion_tags = json.load(f)

with open('champion_winrates.json', 'r') as f:
    champion_winrates = json.load(f)

ROLES = ['Fighter', 'Tank', 'Assassin', 'Mage', 'Marksman', 'Support']

def build_composition_features(row):
    features = {}

    for role in ROLES:
        features[f'blue_{role}'] = 0
        features[f'red_{role}'] = 0
    
    blue_team_total_wr = 0.0
    red_team_total_wr = 0.0

    for i in range(5):
        champ_id = str(int(row[f"player_{i}_champ"]))

        blue_team_total_wr += champion_winrates.get(champ_id, 0.50)

        if champ_id in champion_tags:
            for tag in champion_tags[champ_id]['tags']:
                features[f'blue_{tag}'] += 1
    
    for i in range(5, 10):
        champ_id = str(int(row[f"player_{i}_champ"]))

        red_team_total_wr += champion_winrates.get(champ_id, 0.50)

        if champ_id in champion_tags:
            for tag in champion_tags[champ_id]['tags']:
                features[f'red_{tag}'] += 1
    
    features['blue_avg_winrate'] = blue_team_total_wr / 5.0
    features['red_avg_winrate'] = red_team_total_wr / 5.0
    
    return pd.Series(features)

X = df.apply(build_composition_features, axis=1)
y=df['blue_win']

print(f"Feature Matrix Shape: {X.shape}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

train_data = lgb.Dataset(X_train, label=y_train)
test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

params = {
    'objective': 'binary',
    'metric': 'binary_error',
    'learning_rate': 0.05,
    'num_leaves': 31,
    'verbose': -1
}

model = lgb.train(
    params,
    train_data,
    num_boost_round=150,
    valid_sets=[train_data, test_data],
    callbacks=[lgb.log_evaluation(period=25)]
)

print("\n--- Evaluating Model ---")
y_pred_prob=model.predict(X_test)
y_pred = [1 if prob > 0.5 else 0 for prob in y_pred_prob]

accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy * 100:.2f}%")