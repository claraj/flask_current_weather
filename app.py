from flask import Flask, request, send_file
from weather import get_conditions

app = Flask(__name__)

@app.route('/')
def home():
    return 'Nothing here'


@app.route('/text')
def weather_string():
    city = request.args.get('city')
    state = request.args.get('state')
    if city is None or state is None:
        # abort(400, description='City and state must be provided')
        return 'City and state must be provided', 400

    conditions = get_conditions(city, state)

    if conditions is None:
        return 'Place not found', 404

    return f'{city.title()}, {state.upper()}. {conditions}'


@app.route('/photo')
def weather_photo():
    city = request.args.get('city')
    state = request.args.get('state')
    if city is None or state is None:
        # abort(400, description='City and state must be provided')
        return 'City and state must be provided', 400

    conditions = get_conditions(city, state)

    if conditions is None:
        return 'Place not found', 404

    photo = photo_path(conditions) 
    if photo:
        return send_file(photo)
    else:
        return 'No photo!' 



def photo_path(conditions):

    photo_map = {
        'Snow': 'snow.jpeg', 
        'Thunderstorm': 'thunderstorm.jpeg',
        'Ice': 'ice.jpeg',
        'Partly sunny': 'partly_cloudy.jpeg', 
        'Partly cloudy': 'partly_cloudy.jpeg',
        'Sunny': 'sun.jpeg', 
        'Clear': 'clear.jpeg', 
        'Rain': 'rain.jpeg',
        'Showers': 'rain.jpeg',
        'Wind': 'wind.jpeg',  
        'Cloudy': 'cloudy.jpeg',
        'Mostly cloudy': 'cloudy.jpef',
        'Fog': 'fog.jpeg',
        'Tornado': 'tornado.jpeg',
        }

    for con, photo in photo_map.items():
        if con.upper() in conditions.upper():
            return f'static/photos/{photo}'
            # return f'{request.url_root}static/photos/{photo}'
            