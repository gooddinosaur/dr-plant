import numpy as np


def predict_health(moisture, light, temperature, humidity, model,
                   label_encoder):
    features = np.array([[moisture, temperature, humidity, light]])
    prediction = model.predict(features)
    label = label_encoder.inverse_transform(prediction)
    return label[0]


import joblib

thresholds = joblib.load("model/feature_thresholds.pkl")


def generate_recommendations(soil_moisture, humidity, light_intensity,
                             ambient_temp):
    tips = []

    if soil_moisture < thresholds['Soil_Moisture']['mean'] - \
            thresholds['Soil_Moisture']['std']:
        tips.append("💧 Soil moisture is lower than normal. Consider watering.")
    elif soil_moisture > thresholds['Soil_Moisture']['mean'] + \
            thresholds['Soil_Moisture']['std']:
        tips.append(
            "⚠️ Soil moisture is higher than usual. Avoid overwatering.")

    if humidity < thresholds['Humidity']['mean'] - thresholds['Humidity'][
        'std']:
        tips.append(
            "💨 Humidity is too low. Increase humidity around the plant.")
    elif humidity > thresholds['Humidity']['mean'] + thresholds['Humidity'][
        'std']:
        tips.append("🌫️ Humidity is high. Ensure ventilation.")

    if light_intensity < thresholds['Light_Intensity']['mean'] - \
            thresholds['Light_Intensity']['std']:
        tips.append("🌤️ Light is low. Move the plant to a brighter area.")
    elif light_intensity > thresholds['Light_Intensity']['mean'] + \
            thresholds['Light_Intensity']['std']:
        tips.append("☀️ Too much light. Provide shade if necessary.")

    if ambient_temp < thresholds['Ambient_Temperature']['mean'] - \
            thresholds['Ambient_Temperature']['std']:
        tips.append("🌡️ Temperature is low. Warm up the area.")
    elif ambient_temp > thresholds['Ambient_Temperature']['mean'] + \
            thresholds['Ambient_Temperature']['std']:
        tips.append("🔥 Temperature is high. Try cooling down.")

    if not tips:
        tips.append("✅ All inputs are within normal range. Keep it up!")

    return tips
