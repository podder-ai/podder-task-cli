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
        if not Confirm.ask('Do you want to continue?'):
            return
        console = Console()
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
        lines = FileUtility().execute_command(
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
            if file.endswith(".py"):
                files.append(file)

        return Path(location), files

    def _copy_plugins(self):
        console = Console()
        plugins = self._package_service.get_all_plugins()
        if "objects" in plugins:
            for plugin_name in plugins["objects"].keys():
                console.print("Ejecting Plugin: {} ...".format(plugin_name))
                plugin = plugins["objects"][plugin_name]
                dependencies = plugin["dependencies"]
                filtered_dependencies = {}
                for name in dependencies.keys():
                    if not name.startswith("podder-task-foundation"):
                        filtered_dependencies[name] = dependencies[name]
                self._install_dependency(filtered_dependencies)

                location, files = self._get_plugin_files(plugin_name)
                for file in files:
                    if file != "__init__.py":
                        source_file = location.joinpath(file)
                        destination_file = self._path.joinpath(
                            "podder_task_foundation_plugins", "objects")
                        shutil.copy(source_file, destination_file)
