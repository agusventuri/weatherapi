from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from flask_caching import Cache
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
import os

from data_layer import get_weather

CITY_REQUIRED = "City is required"
COUNTRY_REQUIRED = "Country is required"
COUNTRY_CODE = "Country should be a 2 character code"
COUNTRY_LOWERCASE = "Country should be lowercase"
ENV_VAR_EXCEPTION = "Environment variable not found"

# I try to retrieve the environment variables needed to run the code
FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
OPENWEATHERMAP_APPID = os.environ.get("OPENWEATHERMAP_APPID")

config = {
    "DEBUG": True,
    "FLASK_SECRET_KEY": FLASK_SECRET_KEY,   # some Flask specific configs
    "CACHE_TYPE": "simple",             # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 120
}

# cofiguration variables so swagger can find our api definition
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'


def create_app():
    flask_app = Flask(__name__)
    cors = CORS(flask_app)
    flask_app.config.from_mapping(config)
    cache = Cache(flask_app)

    # initializing swagger config
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        API_URL,
        config={  # Swagger UI config overrides
            'app_name': "weatherapi"
        },
    )

    flask_app.register_blueprint(swaggerui_blueprint)

    # index route that allows me to have a landing page that also has a form
    @flask_app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            country = request.form['country']
            city = request.form['city']

            # first I validate the inputs and display error messages if needed
            error = False

            if not city:
                flash(CITY_REQUIRED)
                error = True

            if not country:
                flash(COUNTRY_REQUIRED)
                error = True

            if country and len(country) != 2:
                flash(COUNTRY_CODE)
                error = True

            if country and not country.islower():
                flash(COUNTRY_LOWERCASE)
                error = True

            if error:
                return redirect(url_for('index'))

            # then I request the actual information
            request_result = get_weather(city, country, OPENWEATHERMAP_APPID)

            # if there isn't any error code in the request, I display the information
            # otherwise I display the error message
            try:
                if request_result["cod"] is not None:
                    flash("Error " + request_result["cod"] + " - " + request_result["message"])
            except KeyError:
                return render_template('weather_card.html', weather=request_result)

        return render_template('index.html')

    # the proper API route that allows me to fetch the weather and forecast information I need using city and country
    # as parameters
    # before anything I validate the parameters against the provided specifications
    @flask_app.route("/weather", methods=['GET', 'POST'])
    def weather():
        city = request.args.get('city', None)
        country = request.args.get('country', None)

        error_message = None

        if city is None or country is None:
            error_message = {
                "cod": "400",
                "message": CITY_REQUIRED + "\n" + COUNTRY_REQUIRED
            }
            return jsonify(error_message), error_message["cod"]

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
            return jsonify(error_message), error_message["cod"]

        # here I check if I already have a cached response and return it if that's the case
        # otherwise, I fetch the data from openweathermap and cache it
        cached_response = cache.get(city + "," + country)
        if cached_response is not None:
            return jsonify(cached_response)

        fetch_weather = get_weather(city, country, OPENWEATHERMAP_APPID)
        cache.set(city + "," + country, fetch_weather)
        return jsonify(fetch_weather)

    return flask_app


if __name__ == "__main__":
    app = create_app()
    app.run()
