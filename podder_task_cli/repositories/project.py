from pathlib import Path

from .repository import Repository


class Project(Repository):
    _type = "other"

    def __init__(self, path: Path):
        super().__init__(path)
        self._process_list = None

    @classmethod
    def detect_project_type(cls, path: Path) -> bool:
        processes_exists = path.joinpath("processes").exists()
        config_exists = path.joinpath("config").exists()
        manage_exists = path.joinpath("manage.py").exists()
        if processes_exists and config_exists and manage_exists:
            return True

        return False

    def get_process_list(self) -> [str]:
        if self._process_list is not None:
            return self._process_list

        process_directory = self._path.joinpath("processes")
        if not process_directory.exists() or not process_directory.is_dir():
            return []
        processes = []
        for path in process_directory.iterdir():
            if not path.is_dir():
                continue
            if path.name.startswith("."):
                continue
            if path.name.startswith("_"):
                continue
            processes.append(path.name)
        self._process_list = processes

        return self._process_list
