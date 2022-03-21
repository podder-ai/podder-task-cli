from pathlib import Path
from typing import Optional

from ...services.podder_service.entities import Entity
from .sources import Source


class ImportBase(object):
    def __init__(self, source: Source, base_path: Path):
        self._source = source
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
