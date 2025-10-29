import asyncio
import httpx

async def getJoke(client, num, joke_url):
    query = await client.get(joke_url)
    response = query.json()
    print(f"{num} {response['value']} with wait time {query.elapsed.total_seconds()}")

async def main():
    async with httpx.AsyncClient() as client:
        joke_url = 'https://api.chucknorris.io/jokes/random'

        tasks = [getJoke(client, num, joke_url) for num in range(100)]
        await asyncio.gather(*tasks)

try:
    asyncio.run(main())
except:
    print('Async error')