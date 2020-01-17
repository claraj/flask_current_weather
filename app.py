from flask import Flask, request, abort
from weather import get_conditions

app = Flask(__name__)


@app.route('/')
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