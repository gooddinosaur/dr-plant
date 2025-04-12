import streamlit as st
from utils.weather import get_weather_by_ip

st.header("☀️ Real-time Weather from Your Location")

weather = get_weather_by_ip()

if weather:
    st.write(f"📍 Location: {weather['city']}")
    st.write(f"🌡 Temperature: {weather['temp']} °C")
    st.write(f"💧 Humidity: {weather['humidity']}%")
else:
    st.warning("Could not fetch weather data.")
