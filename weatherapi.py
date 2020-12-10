from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
import os

from data_layer import get_weather

CITY_REQUIRED = "City is required"
COUNTRY_REQUIRED = "Country is required"
COUNTRY_CODE = "Country should be a 2 character code"
COUNTRY_LOWERCASE = "Country should be lowercase"
ENV_VAR_EXCEPTION = "Environment variable not found"

FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
OPENWEATHERMAP_APPID = os.environ.get("OPENWEATHERMAP_APPID")

app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY


# index route that allows me to have a landing page that also has a form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        country = request.form['country']
        city = request.form['city']

        if not city:
            flash(CITY_REQUIRED)

        if not country:
            flash(COUNTRY_REQUIRED)

        if country and len(country) != 2:
            flash(COUNTRY_CODE)

        if country and not country.islower():
            flash(COUNTRY_LOWERCASE)

        return redirect(url_for('index'))

    return render_template('index.html')


# the proper API route that allows me to fetch the weather and forecast information I need using city and country
# as parameters
# before anything I validate the parameters against the provided specifications
@app.route("/weather", methods=['GET', 'POST'])
def weather():
    city = request.args.get('city', None)
    country = request.args.get('country', None)

    error_message = None

    if not city.strip():
        error_message = {
            "cod": "400",
            "message": CITY_REQUIRED
        }
    if not country.strip():
        error_message = {
            "cod": "400",
            "message": COUNTRY_REQUIRED
        }
    elif not country.islower():
        error_message = {
            "cod": "400",
            "message": COUNTRY_LOWERCASE
        }
    elif len(country) != 2:
        error_message = {
            "cod": "400",
            "message": COUNTRY_CODE
        }

    if error_message is not None:
        return jsonify(error_message)

    return jsonify(get_weather(city, country, OPENWEATHERMAP_APPID))
    # return render_template('weather.html', city=city, country=country)
