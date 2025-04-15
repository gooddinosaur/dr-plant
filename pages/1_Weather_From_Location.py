import streamlit as st
import requests
from utils.weather import get_weather_by_ip
from datetime import datetime

st.set_page_config(page_title="Weather Info", page_icon="☀️", layout="wide")
st.title("☀️ Real-time Weather Info")

# ==== Section 1: Auto Weather from User IP ====
st.subheader("Your Current Location Weather")

with st.spinner("Fetching weather data from your location..."):
    weather_ip = get_weather_by_ip()

if weather_ip:
    location = weather_ip['city']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"""
    <p style="font-size: 16px;">📍 Location : {location}</p>
    <p style="font-size: 16px;">🕒 Time : {timestamp}</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("🌡 Temperature (°C)", f"{weather_ip['temp']} °C")
    with col2:
        st.metric("💧 Humidity (%)", f"{weather_ip['humidity']} %")
else:
    st.warning("⚠️ Could not fetch weather from your IP location.")

# ==== Section 2: Search by City ====
st.markdown("---")
st.subheader("🔎 Search Weather by City")

with st.form("search_form"):
    city = st.text_input("🏙️ Enter a city (e.g., Bangkok)")
    submitted = st.form_submit_button("Get Weather")

if submitted:
    if city:
        with st.spinner(f"Searching weather for {city}..."):
            try:
                response = requests.get("http://localhost:8000/weather", params={"city": city})
                if response.status_code == 200:
                    data = response.json()
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.markdown(f"""
                    **📍 Location:** {data['city']}  
                    🕒 **Time:** {timestamp}
                    """)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("🌡 Temperature (°C)", f"{data['temp']} °C")
                    with col2:
                        st.metric("💧 Humidity (%)", f"{data['humidity']} %")
                else:
                    st.error("⚠️ City not found or API error.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("⚠️ Please enter a city name.")
