from pathlib import Path

from podder_task_cli.repositories import Library, Repository


class ImportBase(object):
    def __init__(self, repository: Repository, base_path: Path):
        self._repository = repository
        self._base_path = base_path

    def execute(self) -> [str]:
        raise NotImplementedError
