import streamlit as st
from utils.predictor import predict_health, generate_recommendations

st.set_page_config(page_title="Predict Plant Health", layout="wide")
st.title("🌿 Dr.Plant: Plant Health Prediction")

st.markdown(
    "Fill in the sensor data below to predict your plant's health condition.")

st.divider()

# แสดง input แบบแบ่งสองคอลัมน์
col1, col2 = st.columns(2)

with col1:
    moisture = st.number_input("🟫 Soil Moisture (%)", min_value=0.0,
                               max_value=100.0, value=50.0, step=0.1)
    temperature = st.number_input("🌡️ Temperature (°C)", min_value=-10.0,
                                  max_value=60.0, value=25.0, step=0.1)

with col2:
    light = st.number_input("💡 Light Intensity (lux)", min_value=0.0,
                            max_value=1000.0, value=500.0, step=1.0)
    humidity = st.number_input("💧 Humidity (%)", min_value=0.0,
                               max_value=100.0, value=50.0, step=0.1)

st.markdown("")

# ปุ่มทำนาย
predict_button = st.button("🔍 Predict Plant Health", use_container_width=True)

if predict_button:
    result = predict_health(moisture, light, temperature, humidity)

    st.success(f"🩺 **Prediction Result:** {result}")
    st.markdown("---")
    st.markdown("### 🌱 Personalized Care Recommendations:")

    recommendations = generate_recommendations(moisture, humidity, light,
                                               temperature)
    for tip in recommendations:
        st.write(f"✅ {tip}")
