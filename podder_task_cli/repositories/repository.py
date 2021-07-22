from pathlib import Path


class Repository(object):
    _type = "other"

    def __init__(self, path: Path):
        self._path = path

    @classmethod
    def detect_project_type(cls, path: Path) -> bool:
        return False

    @property
    def type(self) -> str:
        return self._type
