import asyncio
import os
import re

from AsyncFileProcessingAPI import config
from AsyncFileProcessingAPI.file_operations import load_file, get_files
from AsyncFileProcessingAPI.file_operations import read_file

async def data_mapper(raw_data, key):
    keys = key.split('.')

    for k in keys:
        if type(raw_data) is not dict:
            raw_data = raw_data[0]

        raw_data = raw_data.get(k)

    return raw_data

async def normalize_data(raw_data, api_mapping, file_name, processed_data_path):
    processed_data = {}

    for src_key, tar_key in api_mapping.items():
         processed_data[src_key] = await data_mapper(raw_data, tar_key)

    file_path = os.path.join(processed_data_path, file_name)

    await load_file(processed_data, file_path)

async def merge_files(processed_data_path):
    file_names = await get_files(processed_data_path)

    read_tasks = [read_file(file_name, processed_data_path) for file_name in file_names]
    all_processed_data = await asyncio.gather(*read_tasks)

    file_data = []
    for data in all_processed_data:
        if type(data) != dict:
            for item in data:
                file_data.append({
                    'source': item.get('source'),
                    'response_value': item.get('response_value')
                })
        else:
            file_data.append({
                'source': data.get('source'),
                'response_value': data.get('response_value')
            })

    file_path = config.MERGED_DATA_FILE_PATH

    await load_file(file_data, file_path)

async def main(raw_data_path, processed_data_path, api_mappings):
    file_names = await get_files(raw_data_path)

    read_tasks = [read_file(file_name, raw_data_path) for file_name in file_names]
    all_raw_data = await asyncio.gather(*read_tasks)

    tasks = [
        normalize_data(raw_data, api_mappings[re.sub(r'_?\d+\.json$', '', file_name)], file_name, processed_data_path)
        for raw_data, file_name in zip(all_raw_data, file_names)
    ]

    await asyncio.gather(*tasks)

    await merge_files(processed_data_path)

