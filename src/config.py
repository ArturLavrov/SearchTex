import os
import json

class Config:
    _config_file = "config.json"
    try:
        with open(_config_file) as f:
            _file_config = json.load(f)
    except FileNotFoundError:
        _file_config = {}

    @staticmethod
    def get(key, default=None):
        return os.getenv(key) or Config._file_config.get(key, default)
