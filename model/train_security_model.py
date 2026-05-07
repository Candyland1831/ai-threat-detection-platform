import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib

# Load dataset
df = pd.read_csv("data/UNSW_NB15_training-set.csv")

print("Dataset Loaded")
print(df.head())

# Encode categorical columns
label_encoders = {}

categorical_columns = ['proto', 'service', 'state']

for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Features and target
X = df.drop(columns=['label'])
y = df['label']

# Remove attack_cat if present
if 'attack_cat' in X.columns:
    X = X.drop(columns=['attack_cat'])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

# Evaluation
print(classification_report(y_test, predictions))

# Save model
joblib.dump(model, "model/security_model.pkl")

print("Security model trained successfully!")