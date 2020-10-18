import os
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
        click.secho("Project and process has been prepared for you !",
                    fg="green")
        click.echo("")
        click.secho(
            "Open {}/processes/{}/process.py and start writing your awesome code."
            .format(self._name, self._name),
            fg="green")
        click.secho("🚃🚃🚃🚃🚃 Happy Hacking ! 🚃🚃🚃🚃🚃", fg="green")

    def check_environment(self) -> bool:
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

        path = self._path.joinpath(self._name)
        if path.exists():
            click.secho(
                "directory/file named {} exists already. You need to delete it first if you want to create new one.",
                fg="red")
            return False

        return True

    def prepare_directory(self):
        click.secho("Creating project directory named {}...".format(
            self._name),
                    fg="green")
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

    def exec_poetry(self):
        click.secho("Executing poetry install to install required packages...",
                    fg="green")
        os.chdir('./{}'.format(self._name))
        FileUtility().execute_command("poetry", ["install"])
        os.chdir('../')
