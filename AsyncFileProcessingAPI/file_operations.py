import json
import os
import aiofiles

async def load_file(response, json_file_name):
    async with aiofiles.open(json_file_name, 'w') as f:
        await f.write(json.dumps(response, indent=4))

async def read_file(file_name, file_path):
    full_path = os.path.join(file_path, file_name)
    if os.path.isfile(full_path):
        async with aiofiles.open(full_path, 'r') as f:
            raw_data = await f.read()

            return json.loads(raw_data)

    else:
        raise FileNotFoundError(f'Item is not a file: {full_path}')


async def get_files(directory):
    try:
        item_names = os.listdir(directory)

        return item_names

    except FileNotFoundError:
        print(f'Error: Folder not found at {directory}')
    except Exception as e:
        print(f'An error occurred: {e}')