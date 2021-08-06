from pathlib import Path


class Library(object):
    def __init__(self, path: Path):
        self._path = path

    def get_podder_directory_path(self) -> Path:
        return self._path.joinpath(".podder")

    def get_interface_file_path(self) -> Path:
        return self.get_podder_directory_path().joinpath("interface.json")
