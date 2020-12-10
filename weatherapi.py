import json

from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
import requests
import xmltodict
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '=d8uE^cwQFSB46hx'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        country = request.form['country']
        city = request.form['city']

        if not city:
            flash('City is required')

        if not country:
            flash('Country is required')

        if len(country) != 2 and country:
            flash('Country should be a 2 character code')

        return redirect(url_for('index'))

    return render_template('index.html')


@app.route("/weather", methods=['GET', 'POST'])
def weather():
    city = request.args.get('city', None)
    country = request.args.get('country', None)
    return jsonify(get_weather(city, country))
    # return render_template('weather.html', city=city, country=country)


def get_weather(city, country):
    openweather_weather = fetch_openweather_weather(city, country)["current"]

    location_name = openweather_weather["city"]["@name"] + ", " + openweather_weather["city"]["country"]
    temperature = openweather_weather["temperature"]["@value"] + " " + openweather_weather["temperature"]["@unit"]

    wind_name = openweather_weather["wind"]["speed"]["@name"] + ", "
    wind_speed = openweather_weather["wind"]["speed"]["@value"] + openweather_weather["wind"]["speed"]["@unit"]
    wind_direction = ", " + openweather_weather["wind"]["direction"]["@name"]
    wind = wind_name + wind_speed + wind_direction

    cloudiness = openweather_weather["clouds"]["@name"]
    pressure = openweather_weather["pressure"]["@value"] + " " + openweather_weather["pressure"]["@unit"]
    humidity = openweather_weather["humidity"]["@value"] + openweather_weather["humidity"]["@unit"]

    sunrise = openweather_weather["city"]["sun"]["@rise"] + " " + openweather_weather["city"]["sun"]["@rise"]
    sunset = openweather_weather["city"]["sun"]["@set"] + " " + openweather_weather["city"]["sun"]["@set"]

    lat = openweather_weather["city"]["coord"]["@lat"]
    lon = openweather_weather["city"]["coord"]["@lon"]
    geo_coordinates = "[" + lat + ", " + lon + "]"

    requested_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    openweather_forecast = fetch_openweather_forecast(lat, lon)

    for forecast in openweather_forecast["daily"]:
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
        "requested_time": requested_time
                      # "forecast": {...}
    }
    # return weather_json
    return openweather_forecast


def fetch_openweather_weather(city, country):
    q = city + ", " + country
    params = {
        'appid': '1508a9a4840a5574c822d70ca2132032',
        'units': 'metric',
        'mode': 'xml',
        'q': q
    }
    r = requests.get(
        'http://api.openweathermap.org/data/2.5/weather', params=params)
    xml_response = xmltodict.parse(r.text)

    return xml_response


def fetch_openweather_forecast(lat, lon):
    params = {
        'appid': '1508a9a4840a5574c822d70ca2132032',
        'exclude': 'current,hourly,minutely,alerts',
        'units': 'metric',
        'lat': lat,
        'lon': lon
    }
    # example for daily forecast
    # https://api.openweathermap.org/data/2.5/onecall?lat=10.46&lon=-73.25&exclude=current,hourly,minutely,alerts&appid=1508a9a4840a5574c822d70ca2132032
    r = requests.get(
        'http://api.openweathermap.org/data/2.5/onecall', params=params)

    return r.json()


