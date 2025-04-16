import streamlit as st
from utils.predictor import predict_health, generate_recommendations

st.set_page_config(page_title="Predict Plant Health", layout="wide")
st.title("🌿 Dr.Plant: Plant Health Prediction")

st.markdown("Fill in the sensor data below to predict your plant's health condition.")
st.divider()


col1, col2 = st.columns(2)

with col1:
    moisture_input = st.text_input("🟫 Soil Moisture (%)", placeholder="e.g. 45.5")
    temperature_input = st.text_input("🌡️ Temperature (°C)", placeholder="e.g. 25.0")

with col2:
    light_input = st.text_input("💡 Light Intensity (lux)", placeholder="e.g. 300")
    humidity_input = st.text_input("💧 Humidity (%)", placeholder="e.g. 70.0")

st.markdown("")


predict_button = st.button("🔍 Predict Plant Health", use_container_width=True)

if predict_button:
    try:
        moisture = float(moisture_input)
        temperature = float(temperature_input)
        light = float(light_input)
        humidity = float(humidity_input)

        result = predict_health(moisture, light, temperature, humidity)

        st.success(f"🩺 **Prediction Result:** {result}")
        st.markdown("---")
        st.markdown("### 🌱 Personalized Care Recommendations:")
        recommendations = generate_recommendations(moisture, humidity, light, temperature)
        for tip in recommendations:
            st.write(f"✅ {tip}")

    except ValueError:
        st.error("⚠️ Please fill in all inputs with valid numbers.")
