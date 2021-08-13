import shutil
import tempfile
import urllib.request
import zipfile
from pathlib import Path
from typing import List, Tuple

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

    def _get_plugin_files(self, package_name: str) -> Tuple[Path, List[str]]:
        base_path, all_files = self._package_service.get_package_files(
            package_name)
        files = []
        for file in all_files:
            path_object = Path(file)
            directory_tree = list(path_object.parents)
            if directory_tree[0].name.endswith(".dist-info"):
                continue
            files.append(file)

        return base_path, files

    def _copy_plugins(self):
        console = Console()
        plugins = self._package_service.get_installed_plugins()
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

                    success, result = FileUtility().execute_command(
                        "poetry", ["remove", plugin_name])
                    if not success:
                        console.print("Failed to remove plugin: {}\n{}".format(
                            plugin_name, result))

                self._path.joinpath("podder_task_foundation_plugins",
                                    "__init__.py").touch()
                self._path.joinpath("podder_task_foundation_plugins",
                                    plugin_type, "__init__.py").touch()
