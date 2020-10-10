import tempfile
import urllib.request
import zipfile
from pathlib import Path


class New(object):
    _podder_task = "https://github.com/podder-ai/podder-task-base/archive/main.zip"

    def __init__(self, name: str):
        self._name = name

    def process(self):
        self.prepare_directory()
        self.rename_directories()

    def prepare_directory(self):
        with tempfile.TemporaryDirectory() as temp_path:
            write_path = Path(temp_path).joinpath('podder-task-base.zip')
            urllib.request.urlretrieve(self._podder_task, str(write_path))
            with zipfile.ZipFile(str(write_path)) as zip_package:
                zip_package.extractall(self._name)

    def rename_directories(self):
        directories = ["config", "processes", "data", "input", "output"]
        for directory in directories:
            original_path = Path(
                self._name).joinpath(directory).joinpath("task_name")
            renamed_path = Path(self._name).joinpath(directory).joinpath(
                self._name)
            if original_path.exists():
                original_path.rename(renamed_path)
            else:
                renamed_path.mkdir(parents=True)
