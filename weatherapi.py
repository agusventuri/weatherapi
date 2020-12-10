import json

from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
import requests
import xmltodict

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
    openweather_json = fetch_openweather_json(city, country)["current"]
    location_name = openweather_json["city"]["@name"] + ", " + openweather_json["city"]["country"]
    temperature = openweather_json["temperature"]["@value"] + " " + openweather_json["temperature"]["@unit"]
    # wind_name = openweather_json["wind"]["speed"]["name"] + ","
    wind_name = ""
    # wind_speed = openweather_json["wind"]["speed"]["value"] + openweather_json["wind"]["speed"]["unit"]
    # wind_direction = "," + openweather_json["wind"]["direction"]["name"]
    wind_direction = ","
    # wind = wind_name + wind_speed + wind_direction
    # wind = openweather_json["wind"]

    weather_json = {
        "location_name": location_name,
        "temperature": temperature,
        # "wind": openweather_json
        # "cloudiness": "Scattered clouds",
        # "pressure": "1027 hpa",
        # "humidity": "63%",
        # "sunrise": "06:07",
        # "sunset": "18:00",
        # "geo_coordinates": "[4.61, -74.08]",
        # "requested_time": "2018-01-09 11:57:00"
                      # "forecast": {...}
    }
    return weather_json
    # return openweather_json


def fetch_openweather_json(city, country):
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


