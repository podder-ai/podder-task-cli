import os
import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

from rich.prompt import Confirm, Console, Prompt

from ..utilities import FileUtility, PoetryLockUtility


class Eject(object):
    _podder_task_foundation_url = "https://github.com/podder-ai/podder-task-foundation/archive/{}.zip"

    def __init__(self, path: Path):
        self._path = path
        self._utility = PoetryLockUtility(self._path)

    def process(self):
        if not Confirm.ask('Do you want to continue?'):
            return
        console = Console()
        console.print("Installing Dependency...")
        self._install_dependency()
        console.print("Copy podder-task-foundation...")
        self._copy_podder_task_foundation()
        console.print("Remove podder-task-foundation from library...")
        self._remove_podder_task_foundation()

    def _install_dependency(self):
        dependencies = self._utility.get_podder_task_foundation_dependencies()
        for name in dependencies.keys():
            self._install_package(name, dependencies[name])

    @staticmethod
    def _install_package(name: str, version: str):
        console = Console()
        console.print("Installing {}@{}".format(name, version))
        FileUtility().execute_command("poetry",
                                      ["add", "{}@{}".format(name, version)])

    @staticmethod
    def _remove_podder_task_foundation():
        FileUtility().execute_command("poetry",
                                      ["remove", "podder-task-foundation"])

    def _copy_podder_task_foundation(self):
        version = self._utility.get_podder_task_foundation_version()
        url = self._podder_task_foundation_url.format(version)
        console = Console()
        console.print("Version: {}".format(version))
        console.print("URL: {}".format(url))
        file_name = url[url.rfind('/') + 1:]
        with tempfile.TemporaryDirectory() as temp_path:
            write_path = Path(temp_path).joinpath(file_name)
            urllib.request.urlretrieve(url, str(write_path))
            with zipfile.ZipFile(str(write_path)) as zip_package:
                zip_package.extractall(temp_path)
            shutil.move(
                str(
                    Path(temp_path).joinpath(
                        "podder-task-foundation-{}".format(version)).joinpath(
                            "podder_task_foundation")), str(self._path))
