import streamlit as st
from utils.predictor import predict_health, generate_recommendations

# Page configuration
st.set_page_config(page_title="Predict Plant Health", page_icon="🌿", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .title-container {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 20px;
    }
    .main-title {
        color: #2e7d32;
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 0;
        padding-top: 20px;
        padding-bottom: 10px;
    }
    .info-card {
        background-color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .input-container {
        background-color: white;
        border-radius: 8px;
        padding: 5px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 30px;
    }
    .result-container {
        background-color: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    .health-result {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2e7d32;
        text-align: center;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 8px;
        background-color: #e8f5e9;
    }
    .recommendation-container {
        background-color: #f5f5f5;
        border-radius: 8px;
        padding: 15px;
    }
    .recommendation-item {
        padding: 8px 0;
        border-bottom: 1px solid #e0e0e0;
    }
    .recommendation-item:last-child {
        border-bottom: none;
    }
    hr {
        margin-top: 20px;
        margin-bottom: 20px;
        border: 0;
        border-top: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# Title section with icon
st.markdown(
    """
    <div class="title-container">
        <span style="font-size: 2.5rem;">🌿</span>
        <h1 class="main-title">Dr.Plant: Plant Health Prediction</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="info-card">
        Fill in the sensor data below to predict your plant's health condition. Our AI model will analyze the data and provide personalized care recommendations.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="input-container">
        <h3 style="color: #2e7d32;">Enter Sensor Data</h3>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    moisture_input = st.text_input("🟫 Soil Moisture (%)", placeholder="Example : 45.5")
    temperature_input = st.text_input("🌡️ Temperature (°C)", placeholder="Example : 25")

with col2:
    light_input = st.text_input("💡 Light Intensity (lux)", placeholder="Example : 500")
    humidity_input = st.text_input("💧 Humidity (%)", placeholder="Example : 55")

st.markdown("</div>", unsafe_allow_html=True)

predict_button = st.button("🔍 Predict Plant Health", use_container_width=True)

if predict_button:
    try:
        moisture = float(moisture_input)
        temperature = float(temperature_input)
        light = float(light_input)
        humidity = float(humidity_input)

        result = predict_health(moisture, light, temperature, humidity)
        recommendations = generate_recommendations(moisture, humidity, light, temperature)

        st.markdown(
            f"""
            <div class="result-container">
                <div class="health-result">
                    🩺 Plant Health Prediction: {result}
                </div>
                <h3 style="color: #2e7d32; margin-bottom: 15px;">🌱 Personalized Care Recommendations:</h3>
                <div class="recommendation-container">
            """,
            unsafe_allow_html=True
        )

        for tip in recommendations:
            st.markdown(
                f"""
                <div class="recommendation-item">
                    ✅ {tip}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("</div></div>", unsafe_allow_html=True)

    except ValueError:
        st.markdown(
            """
            <div class="info-card" style="background-color: #f8d7da; color: #721c24;">
                ⚠️ Please fill in all inputs with valid numbers.
            </div>
            """,
            unsafe_allow_html=True
        )