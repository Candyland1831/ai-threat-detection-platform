import pandas as pd
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("data/UNSW_NB15_training-set.csv")

# Encode categorical columns
categorical_columns = ['proto', 'service', 'state']

for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])

# Remove non-feature columns
X = df.drop(columns=['label'])

if 'attack_cat' in X.columns:
    X = X.drop(columns=['attack_cat'])

print(X.iloc[0].tolist())