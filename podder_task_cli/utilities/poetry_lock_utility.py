import shutil
import subprocess
from pathlib import Path
from typing import Any, Optional

import toml


class PoetryLockUtility(object):
    def __init__(self, path: Path):
        self._path = path
        lock_file = self._path.joinpath("poetry.lock")
        if lock_file.exists():
            self._lock_file = toml.loads(lock_file.read_text())
        else:
            self._lock_file = None

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
