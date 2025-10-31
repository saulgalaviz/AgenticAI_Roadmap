import json
from fastapi import FastAPI
from starlette.responses import Response
import asyncio

from AsyncFileProcessingAPI import delete_files, config, file_operations, fetcher, data_processor

app = FastAPI()

@app.get('/')
async def read_root():
    return {'message': 'Hello, welcome to my async file processing application with all sorts of facts!'}

@app.get('/files')
async def get_files():
    files = await file_operations.get_files(config.PROCESSED_DATA_DIR)
    files = files[:-1]

    return Response(
        content=json.dumps({"files": files}, indent=4),
        media_type="application/json"
    )

@app.get('/summary')
async def get_summary():
    summary = await file_operations.read_file(config.MERGED_DATA_FILE_PATH, config.PROCESSED_DATA_DIR)

    return Response(
        content=json.dumps({"summary": summary}, indent=4),
        media_type="application/json"
    )

@app.get('/data')
async def get_data():
    file_names = await file_operations.get_files(config.PROCESSED_DATA_DIR)
    read_tasks = [file_operations.read_file(file_name, config.PROCESSED_DATA_DIR) for file_name in file_names]
    all_processed_data = await asyncio.gather(*read_tasks)
    all_processed_data = all_processed_data[:-1]

    return Response(
        content=json.dumps({"all_processed_data": all_processed_data}, indent=4),
        media_type="application/json"
    )

@app.post('/sync')
async def sync(api_calls: int = 5):
    await fetcher.main(config.SOURCES, config.URLS, api_calls, config.RAW_DATA_DIR)
    await data_processor.main(config.RAW_DATA_DIR, config.PROCESSED_DATA_DIR, config.API_MAPPINGS)
    return {'status': 'OK'}

@app.delete('/delete_data')
async def delete_data():
    delete_files.get_and_delete_files(config.RAW_DATA_DIR)
    delete_files.get_and_delete_files(config.PROCESSED_DATA_DIR)
    return {'status': 'OK'}