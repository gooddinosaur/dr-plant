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


def generate_recommendations(soil_moisture, humidity, light_intensity, ambient_temp):
    tips = []

    # Recommendations and optimal values for Soil Moisture
    recommended_soil_moisture = thresholds['Soil_Moisture']['mean']
    if soil_moisture < thresholds['Soil_Moisture']['mean'] - thresholds['Soil_Moisture']['std']:
        tips.append("💧 Soil moisture is lower than normal. Try watering.")
        tips.append(f"👉 Try to get closer to {recommended_soil_moisture:.2f} for Soil Moisture.")
    elif soil_moisture > thresholds['Soil_Moisture']['mean'] + thresholds['Soil_Moisture']['std']:
        tips.append("⚠️ Soil moisture is higher than usual. Avoid overwatering.")
        tips.append(f"👉 Try to get closer to {recommended_soil_moisture:.2f} for Soil Moisture.")

    # Recommendations and optimal values for Humidity
    recommended_humidity = thresholds['Humidity']['mean']
    if humidity < thresholds['Humidity']['mean'] - thresholds['Humidity']['std']:
        tips.append("💨 Humidity is too low. Increase humidity around the plant.")
        tips.append(f"👉 Try to get closer to {recommended_humidity:.2f} for Humidity.")
    elif humidity > thresholds['Humidity']['mean'] + thresholds['Humidity']['std']:
        tips.append("🌫️ Humidity is high. Ensure ventilation.")
        tips.append(f"👉 Try to get closer to {recommended_humidity:.2f} for Humidity.")

    # Recommendations and optimal values for Light Intensity
    recommended_light_intensity = thresholds['Light_Intensity']['mean']
    if light_intensity < thresholds['Light_Intensity']['mean'] - thresholds['Light_Intensity']['std']:
        tips.append("🌤️ Light is low. Move the plant to a brighter area.")
        tips.append(f"👉 Try to get closer to {recommended_light_intensity:.2f} for Light Intensity.")
    elif light_intensity > thresholds['Light_Intensity']['mean'] + thresholds['Light_Intensity']['std']:
        tips.append("☀️ Too much light. Provide shade if necessary.")
        tips.append(f"👉 Try to get closer to {recommended_light_intensity:.2f} for Light Intensity.")

    # Recommendations and optimal values for Ambient Temperature
    recommended_ambient_temp = thresholds['Ambient_Temperature']['mean']
    if ambient_temp < thresholds['Ambient_Temperature']['mean'] - thresholds['Ambient_Temperature']['std']:
        tips.append("🌡️ Temperature is low. Warm up the area.")
        tips.append(f"👉 Try to get closer to {recommended_ambient_temp:.2f} for Temperature.")
    elif ambient_temp > thresholds['Ambient_Temperature']['mean'] + thresholds['Ambient_Temperature']['std']:
        tips.append("🔥 Temperature is high. Try cooling down.")
        tips.append(f"👉 Try to get closer to {recommended_ambient_temp:.2f} for Temperature.")

    # If all conditions are within normal range
    if not tips:
        tips.append("✅ All inputs are within normal range. Keep it up!")

    return tips

