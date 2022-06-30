import shutil
from pathlib import Path
from typing import List, Optional

from tqdm import tqdm

from ...utilities import HttpUtility
from .entities import Data, Package


class DataManager(object):
    def __init__(self, project_path: Path):
        self._project_path = project_path

    def create_absolute_path(self, data_path: Path):
        return self._project_path.joinpath("data").joinpath(
            data_path).absolute()

    def download(self, data: Data,
                 progress_bar: Optional[tqdm]) -> Optional[Path]:
        source_url = data.source_url
        primary_destination = data.destination_path[0] if isinstance(
            data.destination_path, list) else data.destination_path
        path = self.create_absolute_path(Path(primary_destination))
        if not path.exists():
            path.mkdir(parents=True)
        downloaded_path = HttpUtility().download_file_from_uri(
            source_url, path, progress_bar)
        return downloaded_path

    def copy(self, source_path: Path, destination_path: str):
        destination_absolute_path = self.create_absolute_path(
            Path(destination_path)).joinpath(source_path.name)
        shutil.copy2(source_path, destination_absolute_path)

    def download_all(self, package: Package):
        if package is None:
            return
        data = package.data
        if data is not None:
            downloaded = {}
            progress_bars = []

            for datum in data:
                if datum.source_url in downloaded:
                    for destination_path in data.destination_path:
                        self.copy(downloaded[datum.source_url],
                                  destination_path)
                else:
                    file_size = HttpUtility.get_download_file_size(
                        datum.source_url)
                    if file_size is None:
                        continue
                    progress_bar = tqdm(total=file_size,
                                        unit="B",
                                        unit_scale=True)
                    progress_bars.append(progress_bar)
                    downloaded_path = self.download(datum, progress_bar)
                    downloaded[datum.source_url] = downloaded_path
                    if len(datum.destination_path) > 1:
                        copy_destination = datum.destination_path[1:]
                        for destination_path in copy_destination:
                            self.copy(downloaded_path, destination_path)

            for progress_bar in progress_bars:
                progress_bar.close()

    def export(self, data: Data) -> Optional[List[str]]:
        source_url = data.source_url
        primary_destination = data.destination_path[0] if isinstance(
            data.destination_path, list) else data.destination_path
        path = self.create_absolute_path(Path(primary_destination))
