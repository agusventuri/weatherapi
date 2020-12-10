from datetime import datetime, timedelta

import requests
import xmltodict


# this method fetches and parses content from different data sources into one json that provides the needed information
def get_weather(city, country, appid):
    # first I fetch current weather data and create some variables for clearer code later
    openweather_weather = fetch_openweather_weather(city, country, appid)

    try:
        openweather_weather = openweather_weather["current"]
    except KeyError:
        return openweather_weather["ClientError"]

    location_name = openweather_weather["city"]["@name"] + ", " + openweather_weather["city"]["country"]
    temperature = openweather_weather["temperature"]["@value"] + " " + openweather_weather["temperature"]["@unit"]

    wind_name = openweather_weather["wind"]["speed"]["@name"] + ", "
    wind_speed = openweather_weather["wind"]["speed"]["@value"] + " " + openweather_weather["wind"]["speed"]["@unit"]
    wind_direction = ", " + openweather_weather["wind"]["direction"]["@name"]
    wind = wind_name + wind_speed + wind_direction

    cloudiness = openweather_weather["clouds"]["@name"]
    pressure = openweather_weather["pressure"]["@value"] + " " + openweather_weather["pressure"]["@unit"]
    humidity = openweather_weather["humidity"]["@value"] + openweather_weather["humidity"]["@unit"]

    sunrise = openweather_weather["city"]["sun"]["@rise"][-8:]
    sunset = openweather_weather["city"]["sun"]["@set"][-8:]

    lat = openweather_weather["city"]["coord"]["@lat"]
    lon = openweather_weather["city"]["coord"]["@lon"]
    geo_coordinates = "[" + lat + ", " + lon + "]"

    requested_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # now I fetch forecast data and remove every field I don't need
    openweather_forecast = fetch_openweather_forecast(lat, lon, appid)
    counter = 1

    for forecast in openweather_forecast["daily"]:
        forecast["date"] = (datetime.now() + timedelta(days=counter)).strftime("%Y-%m-%d")
        counter += 1
        forecast.pop("dew_point", None)
        forecast.pop("dt", None)
        forecast.pop("feels_like", None)
        forecast.pop("pop", None)
        forecast.pop("clouds", None)
        forecast["temp"].pop("morn", None)
        forecast["temp"].pop("night", None)
        forecast["temp"].pop("eve", None)
        forecast["temp"].pop("day", None)
        forecast.pop("uvi", None)
        forecast["weather"][0].pop("icon", None)
        forecast["weather"][0].pop("id", None)
        forecast["weather"][0].pop("main", None)
        forecast.pop("wind_deg", None)

    # finally I merge all my data into one json that then I return
    weather_json = {
        "location_name": location_name,
        "temperature": temperature,
        "wind": wind,
        "cloudiness": cloudiness,
        "pressure": pressure,
        "humidity": humidity,
        "sunrise": sunrise,
        "sunset": sunset,
        "geo_coordinates": geo_coordinates,
        "requested_time": requested_time,
        "forecast": openweather_forecast["daily"]
    }

    return weather_json


# here I fetch the current weather using city and country passed as parameters and units obtained form
# environment configuration variables
# I fetch the data in XML mode as the JSON mode doesn't provide all the information I need.
# I then parse the XML to a dict
def fetch_openweather_weather(city, country, appid):

    # example for current weather
    # http://api.openweathermap.org/data/2.5/weather?q=Bogota,co&appid=1508a9a4840a5574c822d70ca2132032

    q = city + ", " + country
    params = {
        'appid': appid,
        'units': 'metric',
        'mode': 'xml',
        'q': q
    }
    r = requests.get(
        'http://api.openweathermap.org/data/2.5/weather', params=params)
    xml_response = xmltodict.parse(r.text)

    return xml_response


# here I fetch the forecast using latitude and longitude passed as parameters and units obtained form
# environment configuration variables. I exclude information I dont need
def fetch_openweather_forecast(lat, lon, appid):

    # example for daily forecast
    # https://api.openweathermap.org/data/2.5/onecall?lat=10.46&lon=-73.25&exclude=current,hourly,minutely,alerts&appid=1508a9a4840a5574c822d70ca2132032

    params = {
        'appid': appid,
        'exclude': 'current,hourly,minutely,alerts',
        'units': 'metric',
        'lat': lat,
        'lon': lon
    }
    r = requests.get(
        'http://api.openweathermap.org/data/2.5/onecall', params=params)

    return r.json()
