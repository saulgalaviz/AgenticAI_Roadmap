import asyncio
import httpx
import json

async def load_file(response, json_file_name):
    with open(json_file_name, "w") as json_file:
        json.dump(response, json_file, indent=4)

async def get_response(client, num, file_name, url):
    query = await client.get(url)
    response = query.json()
    await load_file(response, f'data/raw/{file_name}_{num}.json')
    #print(f"{num} {response['value']} with wait time {query.elapsed.total_seconds()}")

async def main(file_name, url, api_calls):
    async with httpx.AsyncClient() as client:
        tasks = [get_response(client, file_name, num, url) for num in range(api_calls)]
        await asyncio.gather(*tasks)