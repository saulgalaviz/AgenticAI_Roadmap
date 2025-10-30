import asyncio
from AsyncFileProcessingAPI import fetcher, data_processor

def main():
    sources = ['chuck_norris_facts', 'dog_facts']
    urls = ['https://api.chucknorris.io/jokes/random', 'https://dogapi.dog/api/v2/facts?limit=1']
    api_mappings = {
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
            'response_value': 'data.data.attributed.body',
        }
    }
    api_calls = 3

    raw_data_path = 'data/raw/'
    processed_data_path = 'data/processed/'

    asyncio.run(fetcher.main(sources, urls, api_calls, raw_data_path))
    asyncio.run(data_processor.main(raw_data_path, processed_data_path, api_mappings))




