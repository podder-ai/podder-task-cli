import shutil
from pathlib import Path

import click


class Process(object):
    _copy_files = ["__init__.py", "process.py"]
    _directories = ["config", "processes", "data", "input", "output"]

    def __init__(self, name: str, base_directory: Path):
        self._name = name
        self._base_directory = base_directory
        self._template_directory = Path(__file__).parent.joinpath(
            "..", "..", "templates")

    def process(self):
        self.prepare_directory()
        self.copy_files()

    def _get_process_path(self) -> Path:
        return self._base_directory.joinpath("processes", self._name)

    def prepare_directory(self):
        for directory in self._directories:
            original_path = self._base_directory.joinpath(directory).joinpath(
                "task_name")
            renamed_path = self._base_directory.joinpath(directory).joinpath(
                self._name)
            if original_path.exists():
                original_path.rename(renamed_path)
            else:
                renamed_path.mkdir(parents=True)

    def copy_files(self):
        target_directory = self._get_process_path()
        for file in self._copy_files:
            template = self._template_directory.joinpath(file)
            target = target_directory.joinpath(file)
            shutil.copy(str(template), str(target))
