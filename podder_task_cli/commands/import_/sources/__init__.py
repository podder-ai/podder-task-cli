from pathlib import Path
from typing import Optional

from .library import Library
from .project import Project
from .source import Source

_sources: [Source] = [Library, Project]


def get_source(path: Path, url: str) -> Optional[Source]:
    for candidate in _sources:
        if candidate.detect_project_type(path):
            return candidate(path=path, url=url)
    return None
