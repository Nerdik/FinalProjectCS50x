'''Import main packages for functions'''
import requests


def get_city(c):
    '''Get the correct city name'''
    c = c.lstrip().rstrip()
    params = {"name": c}
    BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"
    response = requests.get(BASE_URL, params=params, timeout=20)
    if response.status_code == 200:
        try:
            data = response.json()
            check = data["results"][0]
        except Exception:
            return 1
        else:
             return 2         
    else:
        return 0


def get_weather(d, lt, lg):
    '''Get weather info'''
    params = {
        "latitude": lt,
        "longitude": lg,
        "daily": "temperature_2m_min,temperature_2m_max,precipitation_sum",
        "timezone": "auto",
        "start_date": d,
        "end_date": d
    }
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    response = requests.get(BASE_URL, params=params, timeout=20)

    data = response.json()
    temp_min = data['daily']['temperature_2m_min'][0]
    temp_max = data['daily']['temperature_2m_max'][0]
    precipitation = data['daily']['precipitation_sum'][0]
    result = [temp_min, temp_max, precipitation]
    return result


def get_coordinates(c):
    '''Get and manage city coordinates'''
    BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": c}
    response = requests.get(BASE_URL, params=params, timeout=20)

    if response.status_code == 200:
        data = response.json()
        latitude = data["results"][0]["latitude"]
        longitude = data["results"][0]["longitude"]
        coordinates = [latitude, longitude]
        return coordinates