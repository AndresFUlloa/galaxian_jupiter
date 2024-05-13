from src.utilities.config_loader import load_config_file


class JsonsService:
    def __init__(self):
        self._jsons = {}

    def get(self, path: str):
        if path not in self._jsons:
            self._jsons[path] = load_config_file(path)
        return self._jsons[path]