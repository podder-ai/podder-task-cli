import os
import shutil
import tempfile
import urllib.request
import zipfile
from pathlib import Path
from typing import Dict, List, Tuple, Union

from rich.prompt import Confirm, Console

from ..services import PackageService
from ..utilities import FileUtility


class Eject(object):
    def __init__(self, path: Path):
        self._path = path
        self._package_service = PackageService(self._path)

    def process(self):
        console = Console()
        console.print(
            "\nEject command copy all podder task foundation related files to this directory and remove dependency.\n"
        )
        if not Confirm.ask('Do you want to continue?'):
            return
        console.print("Installing Dependency...")
        dependencies = self._package_service.get_podder_task_foundation_dependencies(
        )
        self._install_dependency(dependencies)
        console.print("Copy podder-task-foundation...")
        self._copy_podder_task_foundation()
        console.print("Remove podder-task-foundation from library...")
        self._remove_podder_task_foundation()
        console.print("Import plugins...")
        self._copy_plugins()

    def _install_dependency(self, dependencies: dict):
        console = Console()
        for name in dependencies.keys():
            version = dependencies[name]
            console.print("Installing {}@{}".format(name, version))
            self._package_service.install_package(name, version)

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
        version = self._package_service.get_podder_task_foundation_version()
        url = self._package_service.get_podder_task_foundation_download_url(
            version)
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

    @staticmethod
    def _get_package_info(
            package_name: str) -> Dict[str, Union[str, List[str]]]:
        err, lines = FileUtility().execute_command(
            "poetry", ["run", "pip", "show", "-f", package_name]).split("\n")
        result = {}
        last_key = None
        for line in lines:
            pair = line.split(": ", maxsplit=1)
            if len(pair) == 1:
                if line.endswith(":"):
                    key = line[:-1].strip().lower()
                    result[key] = []
                    last_key = key
                elif last_key is not None:
                    result[last_key].append(line.strip())
            else:
                result[pair[0].lower()] = pair[1]

        return result

    def _get_plugin_files(self, package_name: str) -> Tuple[Path, List[str]]:

        info = self._get_package_info(package_name)
        location = info["location"]
        files = []
        for file in info["files"]:
            path_object = Path(file)
            directory_tree = list(path_object.parents)
            if len(directory_tree) == 0:
                continue
            if directory_tree[0].name.endswith(".dist-info"):
                continue
            if path_object.suffix == ".pyc":
                continue
            if str(file).startswith("../"):
                continue
            files.append(file)

        return Path(location), files

    def _copy_plugins(self):
        console = Console()
        plugins = self._package_service.get_all_plugins()
        plugin_types = ["objects", "commands"]
        for plugin_type in plugin_types:
            if plugin_type in plugins:
                for plugin_name in plugins[plugin_type].keys():
                    console.print(
                        "Ejecting Plugin: {} ...".format(plugin_name))
                    plugin = plugins[plugin_type][plugin_name]
                    dependencies = plugin["dependencies"]
                    filtered_dependencies = {}
                    for name in dependencies.keys():
                        if not name.startswith("podder-task-foundation"):
                            filtered_dependencies[name] = dependencies[name]
                    self._install_dependency(filtered_dependencies)

                    location, files = self._get_plugin_files(plugin_name)
                    for file in files:
                        console.print("    ... Copy: {}".format(str(file)))
                        source_file = location.joinpath(file)
                        destination_directory = self._path.joinpath(
                            "podder_task_foundation_plugins", plugin_type)
                        destination_file = destination_directory.joinpath(file)
                        if not destination_file.parent.exists():
                            destination_file.parent.mkdir(parents=True)
                        shutil.copy(source_file, destination_file)

                    FileUtility().execute_command("poetry",
                                                  ["remove", plugin_name])

                self._path.joinpath("podder_task_foundation_plugins",
                                    "__init__.py").touch()
                self._path.joinpath("podder_task_foundation_plugins",
                                    plugin_type, "__init__.py").touch()
