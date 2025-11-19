import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw')
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')

MERGED_DATA_FILE_PATH =  os.path.join(PROCESSED_DATA_DIR, 'merged_data.json')

SOURCES = ['chuck_norris_facts', 'dog_facts', 'fact_random']

URLS = ['https://api.chucknorris.io/jokes/random',
        'https://dogapi.dog/api/v2/facts?limit=1',
        'https://uselessfacts.jsph.pl/api/v2/facts/random']

API_MAPPINGS = {
    'chuck_norris_facts':{
        'source': 'source',
        'url': 'url',
        'fetched_at': 'fetched_at',
        'response_value': 'data.value',
    },
    'dog_facts':{
        'source': 'source',
        'url': 'url',
        'fetched_at': 'fetched_at',
        'response_value': 'data.data.attributes.body',
    },
    'fact_random':{
        'source': 'source',
        'url': 'url',
        'fetched_at': 'fetched_at',
        'response_value': 'data.text',
    }
}


