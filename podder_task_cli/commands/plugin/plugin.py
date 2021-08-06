from pathlib import Path


class Plugin(object):
    def __init__(self, path: Path):
        self._path = path
