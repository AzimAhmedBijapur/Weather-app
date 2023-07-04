from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# get the params from config.json
with open('config.json') as c:
    params = json.load(c)["params"]

app.secret_key = params["secret_key"]
api_key = params["api_key"]

# index page shows weather of Mumbai by default


@app.route('/')
def index():
    city = 'Mumbai'
    try:
        # response from geocoding api
        # returns lat and lon
        resp = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}').json()
        lat = resp[0]['lat']
        lon = resp[0]['lon']
        # requests weather api
        weather = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}').json()
        name = resp[0]['name'].capitalize()
        climate = weather['weather'][0]['main']
        temp = weather['main']['temp']
        temp = round(temp - 273.15, 2)
        humid = weather['main']['humidity']
        wind = weather['wind']['speed']
        state = resp[0]['state']
        return render_template('index.html', climate=climate, temp=temp, humid=humid, wind=wind, state=state, name=name)
    except Exception as e:
        return render_template('error.html')


@app.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        city = request.form['city']
    try:
        city = city.capitalize()
        # response from geocoding api
        # returns lat and lon
        resp = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}').json()
        lat = resp[0]['lat']
        lon = resp[0]['lon']
        # requests weather api
        weather = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}').json()
        name = resp[0]['name'].capitalize()
        climate = weather['weather'][0]['main']
        temp = weather['main']['temp']
        temp = round(temp - 273.15, 2)
        humid = weather['main']['humidity']
        wind = weather['wind']['speed']
        state = resp[0]['state']
        return render_template('index.html', climate=climate, temp=temp, humid=humid, wind=wind, state=state, name=name)
    except Exception as e:
        return render_template('error.html')


app.run(port=8080)
