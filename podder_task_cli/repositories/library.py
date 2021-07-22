import importlib
import json
from pathlib import Path
from typing import Optional

from .repository import Repository


class Library(Repository):
    _type = "library"

    def __init__(self, path: Path):
        super().__init__(path)
        self._interface = None

    @classmethod
    def detect_project_type(cls, path: Path) -> bool:
        podder_exists = path.joinpath(".podder", "interface.json").exists()
        if podder_exists:
            return True

        return False

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

        try:
            objects = importlib.import_module(interface["config"])
        except ModuleNotFoundError:
            return None
