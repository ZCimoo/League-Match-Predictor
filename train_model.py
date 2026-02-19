import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import lightgbm as lgb

df= pd.read_csv('match_data.csv')
print(f"Loaded{len(df)} rows of match data")

df = df.dropna()

max_champ_id = 950

def preprocess_champ_id(row):

    features = np.zeros(max_champ_id)

    #Blue Team (Players 0-4)
    for i in range(5):
        champ_id = row[f"player_{i}_champ"]
        if champ_id < max_champ_id:
            features[champ_id] = 1

    for i in range(5, 10):
        champ_id = row[f"player_{i}_champ"]
        if champ_id < max_champ_id:
            features[champ_id] = -1

    return features

print("Processing matches...")

X_raw = df.apply(preprocess_champ_id, axis=1)

X = pd.DataFrame(X_raw.tolist())

y = df["blue_win"]

print(f"Feature Matrix Shape: {X.shape}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Training on {len(X_train)} matches, testing on {len(X_test)} matches")

print("Training LightGBM model...")
train_data = lgb.Dataset(X_train, label=y_train)
test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

params = {
    'objective': 'binary',
    'metric': 'binary_error',
    'boosting_type': 'gbdt',
    'learning_rate': 0.05,
    'num_leaves': 31,
    'verbose': -1
}

model = lgb.train(
    params, 
    train_data, 
    num_boost_round=100, 
    valid_sets=[train_data, test_data], 
    callbacks=[lgb.log_evaluation(10)]
)

print("Evaluating model...")
y_pred_prob = model.predict(X_test)
y_pred = [1 if prob > 0.5 else 0 for prob in y_pred_prob]

accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")
    