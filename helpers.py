'''Import main packages for functions'''
import datetime
import requests


def get_city(c):
    '''Get the correct city name'''
    c = c.lstrip().rstrip()
    params = {"name": c}
    BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"
    response = requests.get(BASE_URL, params=params, timeout=20)
    if response.status_code == 200:
        while True:
            c = c.lstrip().rstrip()
            params = {"name": c}
            response = requests.get(BASE_URL, params=params, timeout=20)
            try:
                data = response.json()
                check = data["results"][0]
            except Exception:
                c = input("Please try to type the City name again: ")
            else:
                return c.capitalize().title()
    else:
        return "The server is offline. Please try later"


def get_date(d):
    '''Get the correct date/interval'''
    while True:
        if d.lower() == "today":
            dates = [datetime.date.today().isoformat()]
            break
        elif d.lower() == "tomorrow":
            today = datetime.date.today()
            plus1 = today + datetime.timedelta(days=1)
            dates = [plus1.isoformat()]
            break
        elif d.lower() == "week":
            today = datetime.date.today()
            plus7 = [today.isoformat()]
            for i in range(1, 7):
                plus7.append((today + datetime.timedelta(days=i)).isoformat())
            dates = plus7
            break
        else:
            d = input("Please input Today or Tomorrow or Week: ")
            continue
    return dates


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

    else:
        return "The server is offline. Please try later"


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


def output_form(d, c, lt, lg):
    '''Manage info with outout form'''
    print(f"{c}")
    if len(d) == 7:
        for i in d:
            print(f"{i}")
            print(f"Temperature: {round((get_weather(i, lt, lg)[0] + (get_weather(i, lt, lg)[1]) / 2), 1)}°C\n")
    else:
        print(f"{d[0]}")
        print(f"Min temperature: {get_weather(d, lt, lg)[0]}°C")
        print(f"Max temperature: {get_weather(d, lt, lg)[1]}°C")
        print(f"Precipitation: {get_weather(d, lt, lg)[2]} mm\n")
