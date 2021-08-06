import json
from pathlib import Path
from typing import Any


class Entity(object):
    def __init__(self, data):
        self._data = data

    def __getattr__(self, item):
        if item in self._data:
            return self._data[item]

    def get(self, key: str = None, default: Any = None) -> Any:
        if key is None:
            return self._data
        paths = key.split('.')
        data = self._data
        for path in paths:
            if path in data:
                data = data[path]
            else:
                return default

        return data

    def save(self, path: Path):
        data = json.dumps(self._data)
        path.write_text(data)

    @classmethod
    def load(cls, path: Path):
        data = json.loads(path.read_text())
        return cls(data)
