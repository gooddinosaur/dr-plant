import streamlit as st
from utils.predictor import predict_health

st.header("🌱 Predict Your Plant's Health")

moisture = st.slider("Soil Moisture (%)", 0, 100, 50)
light = st.slider("Light Intensity (lux)", 0, 1000, 500)
temperature = st.slider("Temperature (°C)", -10, 50, 25)
humidity = st.slider("Humidity (%)", 0, 100, 50)

if st.button("Predict"):
    result = predict_health(moisture, light, temperature, humidity)
    st.success(f"🩺 Prediction: **{result}**")
