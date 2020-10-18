import shutil
import tempfile
import urllib.request
import zipfile
from pathlib import Path

from .process import Process


class New(object):
    _podder_task = "https://github.com/podder-ai/podder-task-base/archive/main.zip"

    def __init__(self, name: str, path: Path):
        self._name = name
        self._path = path

    def process(self):
        self.prepare_directory()
        self.create_process()

    def prepare_directory(self):
        with tempfile.TemporaryDirectory() as temp_path:
            write_path = Path(temp_path).joinpath('podder-task-base.zip')
            urllib.request.urlretrieve(self._podder_task, str(write_path))
            with zipfile.ZipFile(str(write_path)) as zip_package:
                zip_package.extractall(temp_path)
            shutil.move(str(Path(temp_path).joinpath("podder-task-base-main")),
                        str(self._path.joinpath(self._name)))

    def create_process(self):
        Process(name=self._name,
                base_directory=self._path.joinpath(self._name)).process()
