from flask import Flask, render_template, request, url_for, flash, redirect, jsonify

from data_layer import get_weather

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

        if country and len(country) != 2:
            flash('Country should be a 2 character code')

        if country and not country.islower():
            flash('Country should be lowercase')

        return redirect(url_for('index'))

    return render_template('index.html')


@app.route("/weather", methods=['GET', 'POST'])
def weather():
    city = request.args.get('city', None)
    country = request.args.get('country', None)
    return jsonify(get_weather(city, country))
    # return render_template('weather.html', city=city, country=country)
