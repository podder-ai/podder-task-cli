import configparser
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import toml

from ..utilities import FileUtility


class PackageService(object):
    _podder_task_foundation_url = "https://github.com/podder-ai/podder-task-foundation/archive/{}.zip"

    def __init__(self, path: Path):
        self._path = path
        lock_file = self._path.joinpath("poetry.lock")
        if lock_file.exists():
            self._lock_file = toml.loads(lock_file.read_text())
        else:
            self._lock_file = None
        self._file_utility = FileUtility()

    def has_lock_file(self) -> bool:
        return self._lock_file is not None

    def get_package_lockfile_info(self, name: str) -> Optional[dict]:
        if not self.has_lock_file():
            return None
        if "package" not in self._lock_file:
            return None
        for package in self._lock_file["package"]:
            if "name" in package and package["name"] == name:
                return package

        return None

    def get_podder_task_foundation_download_url(self, version: str):
        url = self._podder_task_foundation_url.format(version)
        return url

    def get_podder_task_foundation_info(self, name: str) -> Any:
        package_info = self.get_package_lockfile_info("podder-task-foundation")
        if package_info is None:
            return None
        if name in package_info:
            return package_info[name]

        return None

    def get_podder_task_foundation_version(self) -> Optional[str]:
        return self.get_podder_task_foundation_info("version")

    def get_podder_task_foundation_dependencies(self) -> Optional[dict]:
        return self.get_podder_task_foundation_info("dependencies")

    def get_package_info(
            self, package_name: str) -> Dict[str, Union[str, List[str]]]:
        success, lines = FileUtility().execute_command(
            "poetry", ["run", "pip", "show", "-f", package_name])
        result = {}
        last_key = None
        for line in lines.split("\n"):
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

        lock_file_info = self.get_package_lockfile_info(package_name)
        if lock_file_info is None:
            return result

        for lock_file_key in lock_file_info.keys():
            key = lock_file_key.title()
            if key not in result:
                result[key] = lock_file_info[lock_file_key]

        return result

    def get_package_files(self, package_name: str) -> Tuple[Path, List[str]]:
        info = self.get_package_info(package_name)
        location = info["location"]
        files = []
        for file in info["files"]:
            path_object = Path(file)
            directory_tree = list(path_object.parents)
            if len(directory_tree) == 0:
                continue
            if path_object.suffix == ".pyc":
                continue
            if str(file).startswith("../"):
                continue
            files.append(file)

        return Path(location), files

    def install_package(self,
                        name: str,
                        version: Optional[str] = None) -> bool:
        if version is None:
            success, result = self._file_utility.execute_command(
                "poetry", ["add", name])
        else:
            success, result = self._file_utility.execute_command(
                "poetry", ["add", "{}@{}".format(name, version)])

        return success

    def update_package(self, name: str, version: Optional[str] = None) -> bool:
        if version is None:
            success, result = self._file_utility.execute_command(
                "poetry", ["update", name])
        else:
            success, result = self._file_utility.execute_command(
                "poetry", ["update", "{}@{}".format(name, version)])

        return success

    def get_installed_packages(self) -> Optional[List[Dict[str, str]]]:
        success, libraries = self._file_utility.execute_command(
            "poetry", ["run", "pip", "list", "--format", "json"])
        if not success:
            return None
        try:
            return json.loads(libraries)
        except json.JSONDecodeError:
            return None

    def get_installed_plugins(self) -> Dict[str, Dict[str, Any]]:
        plugins = {}

        libraries = self.get_installed_packages()
        for library in libraries:
            library_name = library["name"]
            package_directory, package_files = self.get_package_files(
                library_name)
            for package_file in package_files:
                full_path = package_directory.joinpath(package_file)
                if full_path.name == "entry_points.txt":
                    config = configparser.ConfigParser()
                    config.read(full_path)
                    for section in config.sections():
                        if section.startswith("podder_task_foundation."):
                            plugin_type = section.split(".")[1]
                            plugin_info = self.get_package_lockfile_info(
                                library_name)
                            if plugin_type in plugins:
                                plugins[plugin_type][
                                    library_name] = plugin_info
                            else:
                                plugins[plugin_type] = {
                                    library_name: plugin_info
                                }

        return plugins
