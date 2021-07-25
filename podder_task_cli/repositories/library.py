import json
import os
from pathlib import Path
from typing import Any, Optional

from ..utilities import ModuleUtility
from .repository import Repository


class Library(Repository):
    _type = "library"

    def __init__(self, path: Path, url: str):
        super().__init__(path, url)
        self._interface = None

    @classmethod
    def detect_project_type(cls, path: Path) -> bool:
        podder_exists = path.joinpath(".podder", "interface.json").exists()
        if podder_exists:
            return True

        return False

    @property
    def name(self) -> str:
        if "name" in self._interface:
            return self._interface["name"]
        return self._url.stem

    def get_entry(self, name: str, default: Any = None) -> Optional[str]:
        interface = self.get_interface()

        if not isinstance(interface, dict) or "entry" not in interface:
            return default

        if name in interface["entry"]:
            return interface["entry"][name]

        return default

    def get_interface(self) -> dict:
        if self._interface is not None:
            return self._interface

        interface = self._path.joinpath(".podder", "interface.json")
        self._interface = json.loads(interface.read_text())

        return self._interface

    def get_config(self) -> Optional[dict]:
        interface = self.get_interface()
        if not isinstance(interface, dict) or "config" not in interface:
            return None

        config = interface["config"]
        if "path" not in config or "name" not in config:
            return None

        config_file_path = self._path.joinpath(os.sep.join(config["path"]))

        config_object = ModuleUtility().import_class_from_file_location(
            config_file_path, config["name"])
        if config_object is None:
            return None

        if hasattr(config_object, "default"):
            return config_object.default()

        return None
