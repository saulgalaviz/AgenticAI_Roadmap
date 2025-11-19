import os

def get_and_delete_files(folder_path):
    try:
        items = os.listdir(folder_path)

        for item in items:
            item_path = os.path.join(folder_path, item)

            if os.path.isfile(item_path):
                os.remove(item_path)
                print(f'Deleted file: {item_path}')
            else:
                print(f'Skipping non-file item: {item_path}')
    except FileNotFoundError:
        print(f'Error: Folder not found at {folder_path}')
    except Exception as e:
        print(f'An error occurred: {e}')

get_and_delete_files('data/raw')
get_and_delete_files('data/processed')