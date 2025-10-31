import asyncio
from AsyncFileProcessingAPI import fetcher, data_processor, config

async def main(api_calls: int = 5):
    await fetcher.main(config.SOURCES, config.URLS, api_calls, config.RAW_DATA_DIR)
    await data_processor.main(config.RAW_DATA_DIR, config.PROCESSED_DATA_DIR, config.API_MAPPINGS)

if __name__ == '__main__':
    asyncio.run(main())