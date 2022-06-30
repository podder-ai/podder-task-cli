from pathlib import Path


class LibraryService(object):
    def __init__(self, path: Path):
        self._path = path
