import shutil
from pathlib import Path

from ...utilities import HttpUtility
from .entities import Data, Package


class DataManager(object):
    def __init__(self, path: Path):
        self._path = path

    def create_absolute_path(self, data_path: Path):
        return self._path.joinpath("data").joinpath(data_path).absolute()

    def download(self, data: Data) -> int:
        source_url = data.source_url
        path = self.create_absolute_path(Path(data.destination_path))
        size = HttpUtility.download_file_from_uri(source_url, path)
        return size

    def download_all(self, package: Package):
        data = package.data
        if data is not None:
            downloaded = {}
            for datum in data:
                if datum.source_url in downloaded:
                    shutil.copy2(downloaded[datum.source_url],
                                 datum.destination_path)
                else:
                    size = self.download(datum)
                    downloaded[datum.source_url] = datum.destination_path
