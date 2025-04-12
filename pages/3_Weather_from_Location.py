import streamlit as st
from utils.weather import get_weather_by_ip, get_weather_by_city

st.set_page_config(page_title="Weather Info", page_icon="☀️", layout="centered")
st.title("☀️ Real-time Weather Info")

# ---- Section 1: Auto Weather from User IP ----
st.subheader("📍 Your Current Location Weather")

weather_ip = get_weather_by_ip()

if weather_ip:
    st.markdown(f"**📍 Location:** {weather_ip['city']}")
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
        searched_weather = get_weather_by_city(city)
        if searched_weather:
            st.markdown(f"**📍 Location:** {searched_weather['city']}")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("🌡 Temperature (°C)", searched_weather["temp"])
            with col2:
                st.metric("💧 Humidity (%)", searched_weather["humidity"])
        else:
            st.error("⚠️ Could not fetch weather for the specified city.")
    else:
        st.warning("Please enter a city name.")
