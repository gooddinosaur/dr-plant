import requests

API_KEY = "f453040f74cc60b5166a170317ef1d36"


def get_weather_by_ip():
    try:
        ip_info = requests.get("https://ipinfo.io").json()
        loc = ip_info["loc"].split(",")
        lat, lon = loc[0], loc[1]
        city = ip_info["city"]

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        res = requests.get(url).json()

        return {
            "city": city,
            "temp": res["main"]["temp"],
            "humidity": res["main"]["humidity"]
        }
    except:
        return None


def get_weather_by_city(city):
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"q={city}&appid={API_KEY}&units=metric"
        )
        res = requests.get(url).json()

        if res.get("cod") != 200:
            return None

        return {
            "city": res["name"],
            "temp": res["main"]["temp"],
            "humidity": res["main"]["humidity"]
        }
    except:
        return None
