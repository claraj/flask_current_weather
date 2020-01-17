
""" Use NOAA to get weather. Defaults to Saint Paul. 
Use args to get weather for another location. Geocoding may work globally but NOAA only provides forecasts for the USA. """


import os 
import sys 
import requests

location_cache_file = 'location_cache.dat'
geocode_url = 'https://nominatim.openstreetmap.org/search/'
weather_point_url = 'https://api.weather.gov/points/{0},{1}'

st_paul_coord = (44.9537, -93.0900)
st_paul = 'Saint Paul, MN'

emojis = {
    'Snow': '❄️', 
    'Thunderstorm': '⚡',
    'Ice': '🌨',
    'Partly sunny': '🌤', 
    'Partly cloudy': '⛅️',
    'Sunny': '☀️', 
    'Clear': '🌃', 
    'Rain': '🌧',
    'Showers': '🌧',
    'Wind': '🍃',  
    'Cloudy': '☁️',
    'Mostly cloudy': '☁️',
    'Fog': '🌫',
    'Tornado': '🌪',
    }


def get_conditions(city, state):
    geocoded = get_lat_long(city, state)
    if (geocoded):
        all_weather, error = get_weather(geocoded[0])
        if all_weather:
            current = get_current(all_weather)
            return current 
        if error:
            return error 


def get_current(weather_list):
    if weather_list[0:1]:
        now = weather_list[0]
        period_name = now.get('name').title()
        temp_f = now.get('temperature')
        detail = now.get('detailedForecast')
        return f'{period_name}: {temp_f}F, {detail}'


    
def get_lat_long(city, state):

    place_query = f'{city},{state}'

    # cached = in_cache(place_query)
    # if cached:
    #     return cached, place_query

    print(f'geocoding place "{place_query}"...')
    
    data = { 'format': 'json', 'city': city, 'state': state}
    r = requests.get(geocode_url, params=data)
    response = r.json()
    print('done.')
    
    if response:
        first_result = response[0]
        coords = float(first_result['lat']), float(first_result['lon'])
        name = first_result['display_name']
        #cache(place_query, coords)  # what the user typed in 
        return coords, name  # Official name 


def get_weather(coord):
    try:
        url = weather_point_url.format(*coord)
        point_data_response = requests.get(url).json()
        forecast_url = point_data_response['properties']['forecast']
        forecast_response = requests.get(forecast_url).json()

        if 'properties' in forecast_response:
            return forecast_response['properties']['periods'], None

        if 'status' in forecast_response:
            return None, f'{forecast_response.get("status")}, {forecast_response.get("detail")} '
    
    except Exception as e:
        print(e)
        return None, 'Unable to get weather for this place. NOAA only has USA forecasts.'
        


def cache(place, coords):

    place = place.lower()
    
    if in_cache(place):
        return
    
    with open(location_cache_file, 'a') as f:
        f.write(f'{place}\t{coords[0]}\t{coords[1]}\n')


def in_cache(place):
    place = place.lower()
    try:
        with open(location_cache_file, 'r') as f:
            for line in f:
                parts = line.split('\t')
                if parts[0] == place:
                    print('using cached location.')
                    return (parts[1], parts[2].strip())
    except FileNotFoundError:
        pass 


def format_display(weather, name):

    print(f'\n{" Weather forecast for " + name +" ":*^90}\n')

    for period in weather:
        name = period['name']
        temp = f_to_c(period['temperature'])
        wind = period['windSpeed']
        detail = period['detailedForecast']
        emoji = emoji_icon(period['shortForecast'])
        print(f'{emoji}  {name.upper()} {temp:.1f}C, wind {wind}.\n{detail}\n')


def emoji_icon(forecast):
    for weather, emoji in emojis.items():
        if weather.upper() in forecast.upper():
            return emoji
    return '⚠️'  


def f_to_c(f):
    return (f - 32)  * 5 / 9   # ffs america 

# main()

