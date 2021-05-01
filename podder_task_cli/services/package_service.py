from pathlib import Path
from typing import Any, Dict, List, Optional

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

    def get_package_info(self, name: str) -> Optional[dict]:
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
        package_info = self.get_package_info("podder-task-foundation")
        if package_info is None:
            return None
        if name in package_info:
            return package_info[name]

        return None

    def get_podder_task_foundation_version(self) -> Optional[str]:
        return self.get_podder_task_foundation_info("version")

    def get_podder_task_foundation_dependencies(self) -> Optional[dict]:
        return self.get_podder_task_foundation_info("dependencies")

    def get_all_plugins(self) -> Dict[str, Dict[str, Any]]:
        plugins = {}
        libraries = self._file_utility.execute_command(
            "poetry", ["run", "pip", "list"]).split("\n")
        for library in libraries:
            if library.startswith("podder-task-foundation-"):
                plugin_name = library.split(" ")[0]
                plugin_type = plugin_name.split("-")[3]
                plugin_info = self.get_package_info(plugin_name)

                if plugin_type in plugins:
                    plugins[plugin_type][plugin_name] = plugin_info
                else:
                    plugins[plugin_type] = {plugin_name: plugin_info}

        return plugins

    def install_package(self, name: str, version: str):
        self._file_utility.execute_command(
            "poetry", ["add", "{}@{}".format(name, version)])
