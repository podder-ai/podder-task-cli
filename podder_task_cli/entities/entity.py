import json
from pathlib import Path


class Entity(object):
    def __init__(self, data):
        self._data = data

    def __getattr__(self, item):
        if item in self._data:
            return self._data[item]

    def save(self, path: Path):
        data = json.dumps(self._data)
        path.write_text(data)

    @classmethod
    def load(cls, path: Path):
        data = json.loads(path.read_text())
        return Entity(data)
