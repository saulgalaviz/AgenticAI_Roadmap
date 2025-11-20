import requests
import os
import math
from langchain_core.tools import Tool
from dotenv import load_dotenv

load_dotenv(dotenv_path='../../reference/.env')

OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')

def get_lat_lon(city: str, api_key: str) -> tuple[float, float] | None:
    geocode_url = 'http://api.openweathermap.org/geo/1.0/direct'
    params = {'q': city, 'limit': 1, 'appid': api_key}
    try:
        response = requests.get(geocode_url, params=params)
        response.raise_for_status()
        data = response.json()
        if data: return data[0]['lat'], data[0]['lon']
        return None
    except:
        return None


def get_weather(city: str) -> str:
    if not OPENWEATHERMAP_API_KEY: return 'Error: OpenWeatherMap API key not configured.'
    if not city: return 'Error: Please provide a city name.'

    coords = get_lat_lon(city, OPENWEATHERMAP_API_KEY)
    if coords is None: return f'Could not find coordinates for city: {city}.'

    lat, lon = coords
    base_url = 'https://api.openweathermap.org/data/3.0/onecall'
    params = {
        'lat': lat, 'lon': lon, 'appid': OPENWEATHERMAP_API_KEY,
        'units': 'imperial', 'exclude': 'minutely,hourly,alerts'
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        output = [f'--- Weather Forecast for {city.title()} ---']

        curr = data.get('current', {})
        output.append(f'Current: {curr.get('temp')}°F, {curr.get('weather', [{}])[0].get('description')}.')

        daily = data.get('daily', [])
        if len(daily) >= 3:
            import datetime
            for i in range(1, 3):
                d = daily[i]
                day_name = datetime.datetime.fromtimestamp(d.get('dt')).strftime('%A')
                output.append(
                    f'{day_name}: {d.get('temp', {}).get('day')}°F, {d.get('weather', [{}])[0].get('description')}.')

        return '\n'.join(output)
    except Exception as e:
        return f'Weather tool error: {e}'


def calculate_expression(query: str) -> str:
    try:
        clean_query = query.lower().replace('what is', '').replace('?', '').strip()

        allowed_names = {'math': math, '__builtins__': {}}

        result = eval(clean_query, allowed_names)
        return f'Calculated locally: {result}'
    except (SyntaxError, NameError, TypeError, ZeroDivisionError):
        pass

    base_url = 'https://api.duckduckgo.com/'
    params = {'q': query, 'format': 'json', 't': 'LangChainAgent'}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        answer = data.get('Answer')
        abstract_text = data.get('AbstractText')

        if answer:
            if isinstance(answer, str) and answer.strip():
                return f'API Answer: {answer.strip()}'
            elif isinstance(answer, dict) and 'text' in answer:
                return f'API Answer: {answer['text']}'

        if abstract_text and isinstance(abstract_text, str) and abstract_text.strip():
            return f'API Answer: {abstract_text.strip()}'

        return f'Could not find an answer for \'{query}\'.'

    except Exception as e:
        return f'Calculation error: {type(e).__name__}: {str(e)}'


AGENT_TOOLS = [
    Tool(
        name='Calculator',
        func=calculate_expression,
        description='Useful for calculating math expressions (e.g. \'9*9\', \'sqrt(25)\') OR asking for specific numbers/conversions (e.g. \'100 km to miles\').'
    ),
    Tool(
        name='Weather',
        func=get_weather,
        description=(
            'A comprehensive tool to get the **current weather and the next two days of forecast** '
            'for any recognized city worldwide. This tool uses a robust geo-location system. '

            '**CRITICAL REASONING INSTRUCTION:** '
            'If the user asks for the weather for a **known event, venue, or famous landmark** '
            '(e.g., \'Camp Flog Gnaw\', \'Dodger Stadium\', \'Times Square\'), the input **MUST** be the '
            'nearest major city and state/country (e.g., use \'Los Angeles, CA\' for \'Camp Flog Gnaw\'). '

            'The input must always be a clean, geographical location (e.g., \'New York, NY\' or \'Paris, FR\').'
        )
    )
]