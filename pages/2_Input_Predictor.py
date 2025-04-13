import streamlit as st
from utils.predictor import predict_health, generate_recommendations


st.header("🌱 Predict Your Plant's Health")

# รับค่าจากผู้ใช้แบบกรอกตัวเลข
moisture = st.number_input("Soil Moisture (%)", min_value=0.0, max_value=100.0, value=50.0, step=0.1)
light = st.number_input("Light Intensity (lux)", min_value=0.0, max_value=1000.0, value=500.0, step=1.0)
temperature = st.number_input("Temperature (°C)", min_value=-10.0, max_value=60.0, value=25.0, step=0.1)
humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=50.0, step=0.1)

# เมื่อกดปุ่ม Predict
if st.button("Predict"):
    result = predict_health(moisture, light, temperature, humidity)
    st.success(f"🩺 Prediction: **{result}**")

    st.markdown("### 🌱 Recommendations:")
    recommendations = generate_recommendations(moisture, humidity, light, temperature)
    for tip in recommendations:
        st.write("- " + tip)
