from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/<int:post_id>')
# @app.route('/weather?city=<city>&country=<country>&')
# @app.route('/weather/<city>/<country>')
@app.route("/weather", methods=['GET'])
def weather():
    city = request.args.get('city', None)
    country = request.args.get('country', None)
    return render_template('weather.html', city=city, country=country)
