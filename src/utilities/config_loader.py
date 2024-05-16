import json
import os


def load_config_file(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data = json.loads(file.read())
    return data
