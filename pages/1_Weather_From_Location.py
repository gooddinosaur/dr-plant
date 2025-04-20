import streamlit as st
import requests
from utils.weather import get_weather_by_ip
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Weather Info", page_icon="☀️", layout="wide")

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
    .weather-card {
        background-color: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .location-info {
        margin-bottom: 15px;
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
        <span style="font-size: 2.5rem;">☀️</span>
        <h1 class="main-title">Real-time Weather Info</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# ==== Section 1: Auto Weather from User IP ====
st.markdown(
    """
    <div class="section-title">
        <span>📍</span> Your Current Location Weather
    </div>
    """,
    unsafe_allow_html=True
)

with st.spinner("Fetching weather data from your location..."):
    weather_ip = get_weather_by_ip()

if weather_ip:
    location = weather_ip['city']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    st.markdown(
        f"""
        <div class="weather-card">
            <div class="location-info">
                <p style="font-size: 16px;"><strong>📍 Location:</strong> {location}</p>
                <p style="font-size: 16px;"><strong>🕒 Time:</strong> {timestamp}</p>
            </div>
            <div style="display: flex;">
                <div style="flex: 1; text-align: center;">
                    <p style="font-size: 18px; color: #616161;">Temperature</p>
                    <p style="font-size: 2rem; color: #2e7d32; font-weight: 600;">{weather_ip['temp']} °C</p>
                </div>
                <div style="flex: 1; text-align: center;">
                    <p style="font-size: 18px; color: #616161;">Humidity</p>
                    <p style="font-size: 2rem; color: #2e7d32; font-weight: 600;">{weather_ip['humidity']} %</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <div class="info-card" style="background-color: #fff3cd; color: #856404;">
            ⚠️ Could not fetch weather from your IP location.
        </div>
        """,
        unsafe_allow_html=True
    )

# ==== Section 2: Search by City ====
st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="section-title">
        <span>🔎</span> Search Weather by City
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="info-card">
        Enter a city name below to get current weather information.
    </div>
    """,
    unsafe_allow_html=True
)

with st.form("search_form"):
    city = st.text_input("🏙️ Enter a city (e.g., Bangkok)")
    submitted = st.form_submit_button("Get Weather")

if submitted:
    if city:
        with st.spinner(f"Searching weather for {city}..."):
            try:
                response = requests.get("http://localhost:8000/weather",
                                        params={"city": city})
                if response.status_code == 200:
                    data = response.json()
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.markdown(
                        f"""
                        <div class="weather-card">
                            <div class="location-info">
                                <p style="font-size: 16px;"><strong>📍 Location:</strong> {data['city']}</p>
                                <p style="font-size: 16px;"><strong>🕒 Time:</strong> {timestamp}</p>
                            </div>
                            <div style="display: flex; gap: 20px;">
                                <div style="flex: 1; text-align: center;">
                                    <p style="font-size: 18px; color: #616161;">Temperature</p>
                                    <p style="font-size: 2rem; color: #2e7d32; font-weight: 600;">{data['temp']} °C</p>
                                </div>
                                <div style="flex: 1; text-align: center;">
                                    <p style="font-size: 18px; color: #616161;">Humidity</p>
                                    <p style="font-size: 2rem; color: #2e7d32; font-weight: 600;">{data['humidity']} %</p>
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        """
                        <div class="info-card" style="background-color: #f8d7da; color: #721c24;">
                            ⚠️ City not found or API error.
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            except Exception as e:
                st.markdown(
                    f"""
                    <div class="info-card" style="background-color: #f8d7da; color: #721c24;">
                        ❌ Error: {str(e)}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.markdown(
            """
            <div class="info-card" style="background-color: #fff3cd; color: #856404;">
                ⚠️ Please enter a city name.
            </div>
            """,
            unsafe_allow_html=True
        )