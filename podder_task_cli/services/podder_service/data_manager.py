import shutil
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse

import boto3
from tqdm import tqdm

from ...utilities import HttpUtility, TerminalUtility
from .entities import Data, Package


class DataManager(object):
    def __init__(self, project_path: Path):
        self._project_path = project_path

    def create_absolute_path(self, data_path: Path) -> Path:
        return self._project_path.joinpath("data").joinpath(
            data_path).absolute()

    def download(self, data: Data,
                 progress_bar: Optional[tqdm]) -> Optional[Path]:
        source_url = data.source_url
        parsed = urlparse(source_url)

        if parsed.scheme == "s3":
            return self.download_from_s3(data, progress_bar)

        return self.download_from_http(data, progress_bar)

    def download_from_http(self, data: Data,
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

    def download_from_s3(self, data: Data,
                         progress_bar: Optional[tqdm]) -> Optional[Path]:
        source_url = data.source_url
        parsed = urlparse(source_url)
        bucket = parsed.hostname
        key = parsed.path
        s3 = boto3.resource('s3')

        primary_destination = data.destination_path[0] if isinstance(
            data.destination_path, list) else data.destination_path
        path = self.create_absolute_path(Path(primary_destination))

        try:
            if progress_bar is None:
                s3.meta.client.download_file(bucket, key, path)
            else:

                def hook(progress):
                    def inner(bytes_amount):
                        progress.update(bytes_amount)

                    return inner

                file_object = s3.Object(bucket, key)
                filesize = file_object.content_length
                with tqdm(total=filesize, unit='B', unit_scale=True,
                          desc=path) as t:
                    s3.meta.client.download_file(path, Callback=hook(t))
        except Exception as e:
            TerminalUtility().error(str(e))
            return None

        return path

    def copy(self, source_path: Path, destination_path: str):
        destination_absolute_path = self.create_absolute_path(
            Path(destination_path)).joinpath(source_path.name)
        shutil.copy2(source_path, destination_absolute_path)

    @staticmethod
    def get_file_size(source_url) -> int:
        parsed = urlparse(source_url)

        if parsed.scheme == "s3":
            bucket = parsed.hostname
            key = parsed.path
            s3 = boto3.resource('s3')
            file_object = s3.Object(bucket, key)
            return file_object.content_length

        return HttpUtility.get_download_file_size(source_url)

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
                    file_size = self.get_file_size(datum.source_url)
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
