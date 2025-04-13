import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


df = pd.read_csv("plant_health_data.csv")
custom_mapping = {'High Stress': 2, 'Moderate Stress': 1, 'Healthy': 0}
df['Plant_Health_Status_Encoded'] = df['Plant_Health_Status'].map(
    custom_mapping)
df= df.drop(columns=['Plant_Health_Status', 'Timestamp'])
selected_features = ['Soil_Moisture', 'Humidity', 'Light_Intensity', 'Ambient_Temperature']
X = df[selected_features]
y = df['Plant_Health_Status_Encoded']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = RandomForestClassifier(random_state=42)
model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)
print("Random Forest Classifier Accuracy:", accuracy_score(y_test, y_pred))

joblib.dump(model, "plant_health_model.pkl")
joblib.dump(scaler, "scaler.pkl")
