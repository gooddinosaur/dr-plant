import numpy as np
import joblib

model = joblib.load("model/plant_health_model.pkl")
scaler = joblib.load("model/scaler.pkl")

label_mapping = {0: "Healthy", 1: "Moderate Stress", 2: "High Stress"}


def predict_health(moisture, light, temperature, humidity):
    features = np.array([[moisture, humidity, light, temperature]])
    scaled_features = scaler.transform(features)
    prediction = model.predict(scaled_features)
    label = label_mapping[prediction[0]]
    return label


thresholds = joblib.load("model/feature_thresholds.pkl")


def generate_recommendations(soil_moisture, humidity, light_intensity,
                             ambient_temp):
    tips = []

    if soil_moisture < thresholds['Soil_Moisture']['mean'] - thresholds['Soil_Moisture']['std']:
        tips.append("💧 Soil moisture is lower than normal. Consider watering.")
    elif soil_moisture > thresholds['Soil_Moisture']['mean'] + thresholds['Soil_Moisture']['std']:
        tips.append("⚠️ Soil moisture is higher than usual. Avoid overwatering.")

    if humidity < thresholds['Humidity']['mean'] - thresholds['Humidity']['std']:
        tips.append("💨 Humidity is too low. Increase humidity around the plant.")
    elif humidity > thresholds['Humidity']['mean'] + thresholds['Humidity']['std']:
        tips.append("🌫️ Humidity is high. Ensure ventilation.")

    if light_intensity < thresholds['Light_Intensity']['mean'] - thresholds['Light_Intensity']['std']:
        tips.append("🌤️ Light is low. Move the plant to a brighter area.")
    elif light_intensity > thresholds['Light_Intensity']['mean'] + thresholds['Light_Intensity']['std']:
        tips.append("☀️ Too much light. Provide shade if necessary.")

    if ambient_temp < thresholds['Ambient_Temperature']['mean'] - thresholds['Ambient_Temperature']['std']:
        tips.append("🌡️ Temperature is low. Warm up the area.")
    elif ambient_temp > thresholds['Ambient_Temperature']['mean'] + thresholds['Ambient_Temperature']['std']:
        tips.append("🔥 Temperature is high. Try cooling down.")

    if not tips:
        tips.append("✅ All inputs are within normal range. Keep it up!")

    return tips
