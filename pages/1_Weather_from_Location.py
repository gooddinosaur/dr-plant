import streamlit as st
import requests
from utils.weather import get_weather_by_ip

st.set_page_config(page_title="Weather Info", page_icon="☀️", layout="centered")
st.title("☀️ Real-time Weather Info")

API_URL = "http://localhost:8000/weather"

# ---- Section 1: Auto Weather from User IP ----
st.subheader("📍 Your Current Location Weather")

weather_ip = get_weather_by_ip()

if weather_ip:
    st.markdown(f"**📍 Location :** {weather_ip['city']}")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🌡 Temperature (°C)", weather_ip["temp"])
    with col2:
        st.metric("💧 Humidity (%)", weather_ip["humidity"])
else:
    st.warning("⚠️ Could not fetch weather from your IP location.")

# ---- Section 2: Search by City ----
st.markdown("---")
st.subheader("🔎 Search Weather by City")

with st.form("search_form"):
    city = st.text_input("🏙️ City (e.g., Bangkok)")
    submitted = st.form_submit_button("Get Weather")

if submitted:
    if city:
        try:
            response = requests.get(API_URL, params={"city": city})
            if response.status_code == 200:
                data = response.json()
                st.markdown(f"**📍 Location :** {data['city']}")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("🌡 Temperature (°C)", data["temp"])
                with col2:
                    st.metric("💧 Humidity (%)", data["humidity"])
            else:
                st.error("⚠️ City not found or API error.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a city name.")
