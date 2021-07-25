from pathlib import Path

from ..utilities import GitUtility


class Repository(object):
    _type = "other"

    def __init__(self, path: Path, url: str):
        self._url = Path(url)
        self._path = path

    @classmethod
    def detect_project_type(cls, path: Path) -> bool:
        return False

    @property
    def type(self) -> str:
        return self._type

    @property
    def name(self) -> str:
        return self._path.stem

    @property
    def path(self) -> Path:
        return self._path

    @property
    def schema(self) -> str:
        if str(self._url).startswith("http"):
            return "http"
        return "ssh"

    @property
    def url(self) -> str:
        return str(self._url)

    @property
    def revision(self) -> str:
        return GitUtility().get_revision(self._path)
