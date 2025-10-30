import json
import os
import re

async def load_file(response, json_file_name):
    with open(json_file_name, "w") as json_file:
        json.dump(response, json_file, indent=4)

async def merge_files():
    pass

async def data_mapper(raw_data, key):
    pass

async def normalize_data(raw_data, api_mapping, file_name):
    processed_data = {}


    return processed_data



async def main(raw_data_path, processed_data_path, api_mappings):
    try:
        items = os.listdir(raw_data_path)

        for item_name in items:
            item_path = os.path.join(raw_data_path, item_name)

            if os.path.isfile(item_path):
                with open(item_path, 'r') as file:
                    raw_data = json.load(file)

                source_name = re.sub('\d', '', item_name)
                source_name = source_name[:-6]

                processed_data = await normalize_data(raw_data, api_mappings[source_name], item_name)
                file_path = f'{processed_data_path}{item_name}'

                await load_file(processed_data, file_path)

            else:
                print(f'Skipping non-file item: {item_path}')
    except FileNotFoundError:
        print(f'Error: Folder not found at {raw_data_path}')
    except Exception as e:
        print(f'An error occurred: {e}')

    merge_files()

