import streamlit as st
import requests
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Dr.Plant",
    page_icon="🌿",
    layout="wide"
)

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
    .intro-text {
        background-color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .section-title {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.5rem;
        font-weight: 500;
        color: #2e7d32;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    .sensor-card {
        background-color: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        text-align: center;
        height: 100%;
    }
    .sensor-icon {
        font-size: 1.2rem;
        margin-bottom: 5px;
    }
    .sensor-label {
        color: #616161;
        font-size: 0.9rem;
        margin-bottom: 5px;
    }
    .sensor-value {
        color: #2e7d32;
        font-size: 1.8rem;
        font-weight: 600;
    }
    .timestamp-container {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        margin-top: 10px;
    }
    .timestamp {
        color: #616161;
        font-size: 0.9rem;
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
        <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/seedling.svg" width="50" height="50" style="filter: invert(42%) sepia(93%) saturate(1352%) hue-rotate(87deg) brightness(119%) contrast(119%);">
        <h1 class="main-title">Dr.Plant: Plant Health Predictor</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Introduction section
st.markdown(
    """
    <div class="intro-text">
        <strong>Welcome to Dr.Plant!</strong><br>
        A smart assistant that helps you take care of your plant using sensor data and weather info.<br>
        Navigate through the pages using the sidebar.
    </div>
    """,
    unsafe_allow_html=True
)

# Horizontal line separator
st.markdown("<hr>", unsafe_allow_html=True)

# Latest sensor data section title with icon
st.markdown(
    """
    <div class="section-title">
        <span>🌱</span> Latest Sensor Data
    </div>
    """,
    unsafe_allow_html=True
)

# Sensor data display
try:
    # API call
    response = requests.get("http://localhost:8000/latest-data")

    if response.status_code == 200:
        data = response.json()

        # Create columns for sensor data
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f"""
                <div class="sensor-card">
                    <div class="sensor-icon">🌡️</div>
                    <div class="sensor-label">Temperature (°C)</div>
                    <div class="sensor-value">{data['temperature']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div class="sensor-card">
                    <div class="sensor-icon">💧</div>
                    <div class="sensor-label">Humidity (%)</div>
                    <div class="sensor-value">{data['humidity']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"""
                <div class="sensor-card">
                    <div class="sensor-icon">🌞</div>
                    <div class="sensor-label">Light Intensity (lux)</div>
                    <div class="sensor-value">{data['light']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col4:
            st.markdown(
                f"""
                <div class="sensor-card">
                    <div class="sensor-icon">🌱</div>
                    <div class="sensor-label">Soil Moisture (%)</div>
                    <div class="sensor-value">{data['soil']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Timestamp display
        timestamp = datetime.fromisoformat(data['timestamp']).strftime(
            '%Y-%m-%d %H:%M:%S')
        st.markdown(
            f"""
            <div class="timestamp-container">
                <div class="timestamp">🕒 Time: {timestamp}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.error("❌ Could not fetch data from API.")

except Exception as e:
    st.error(f"❌ Error connecting to API: {e}")