print("🌱 Starting Advanced Plant AI Model Training...")

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Step 1: Load the dataset
print("\n📥 Loading dataset from 'Crop_recommendation.csv'...")
data = pd.read_csv('Crop_recommendation.csv')

# Step 2: Select correct columns
X = data[['temperature', 'humidity', 'ph', 'rainfall']]
y = data['label']

print("\n📊 Selected Features (X):")
print(X.head())

# Step 3: Encode labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Step 4: Train the model
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Step 5: Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\n✅ Model Accuracy: {accuracy * 100:.2f}%")

# Step 6: Save model and label encoder
joblib.dump(model, 'plant_suggestion_model.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')
print("💾 Model and Label Encoder saved successfully!")
