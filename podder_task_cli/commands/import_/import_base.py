from pathlib import Path
from typing import List, Optional

from ...services.podder_service.entities import Entity
from .sources import Source


class ImportBase(object):
    def __init__(self, source: Source, base_path: Path,
                 processes: Optional[List[str]]):
        self._source = source
        self._base_path = base_path
        self._processes = []

    def execute(self) -> [str]:
        raise NotImplementedError

    def _get_metadata(self, name: str) -> Optional[Entity]:
        path = self._base_path.joinpath("processes", name,
                                        ".podder.process.conf")
        if not path.exists():
            return None
        entity = Entity.load(path)
        return entity
