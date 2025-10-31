import asyncio
import re
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

    file_path = f'{processed_data_path}{file_name}'

    await load_file(processed_data, file_path)

async def merge_files(processed_data_path):
    file_names = await get_files(processed_data_path)

    read_tasks = [read_file(file_name, processed_data_path) for file_name in file_names]
    all_processed_data = await asyncio.gather(*read_tasks)

    file_data = []
    for i in range(len(all_processed_data)):

        final_data = {
            'source' : all_processed_data[i]['source'],
            'response_value' : all_processed_data[i]['response_value']
        }
        file_data.append(final_data)

    file_path = f'{processed_data_path}merged_data.json'
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

