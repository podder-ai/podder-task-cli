import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

import click

from ..utilities import FileUtility
from .process import Process


class New(object):
    _podder_task = "https://github.com/podder-ai/podder-task-base/archive/main.zip"

    def __init__(self, name: str, path: Path):
        self._name = name
        self._path = path

    def process(self):
        if not self.check_environment():
            return
        self.prepare_directory()
        self.create_process()
        self.exec_poetry()

    @staticmethod
    def check_environment() -> bool:
        python_version = sys.version_info
        if python_version.major < 3 or (python_version.major == 3
                                        and python_version.minor < 6):
            click.secho("Podder Task requires python version 3.6 or higher.",
                        fg="red")
            return False

        if not FileUtility().find_command("poetry"):
            click.secho(
                "Podder Task requires poetry for package management. `pip install poetry` to install poetry.",
                fg="red")
            return False

        return True

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

    @staticmethod
    def exec_poetry():
        FileUtility().execute_command("poetry", ["init"])
