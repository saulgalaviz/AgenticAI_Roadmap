import asyncio
import datetime

import httpx
import json

async def load_file(response, json_file_name):
    with open(json_file_name, "w") as json_file:
        json.dump(response, json_file, indent=4)

async def get_response(client,source, num, url, raw_data_path):
    query = await client.get(url)
    fetched_at = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    data = query.json()
    file_data = {
        'source': source,
        'url': url,
        'fetched_at': fetched_at,
        'data': data
    }
    file_path = f'{raw_data_path}{source}_{num}.json'

    await load_file(file_data, file_path)

async def main(sources, urls, api_calls, raw_data_path):
    async with httpx.AsyncClient() as client:
        tasks = [
            get_response(client, sources[i], num, urls[i], raw_data_path)
            for num in range(api_calls)
            for i in range(len(sources))
        ]
        await asyncio.gather(*tasks)