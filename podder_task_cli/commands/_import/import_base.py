from pathlib import Path
from typing import Optional

from podder_task_cli.repositories import Repository

from ...entities import Entity


class ImportBase(object):
    def __init__(self, repository: Repository, base_path: Path):
        self._repository = repository
        self._base_path = base_path

    def execute(self) -> [str]:
        raise NotImplementedError

    def _get_metadata(self, name: str) -> Optional[Entity]:
        path = self._base_path.joinpath("processes", name,
                                        ".podder.process.conf")
        if not path.exists():
            return None
        entity = Entity.load(path)
        return entity
