import asyncio
from AsyncFileProcessingAPI import fetcher

file_names = ['Chuck_Norris', 'Dog_Facts']
urls = ['https://api.chucknorris.io/jokes/random', 'https://dogapi.dog/api/v2/facts?limit=1']
api_calls = 3

for i in range(len(file_names)):
    asyncio.run(fetcher.main(file_names[i], urls[i], api_calls))



