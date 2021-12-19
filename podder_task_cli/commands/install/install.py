from pathlib import Path

from ...utilities import PoetryUtility


class Install(object):
    def __init__(self, path: Path):
        self._path = path
        self._podder_service = PoetryUtility

    def process(self):
        success = PoetryUtility().install(path=self._path)
