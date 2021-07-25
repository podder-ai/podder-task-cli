from pathlib import Path
from typing import Optional

from .library import Library
from .project import Project
from .repository import Repository

_repositories: [Repository] = [Library, Project]


def get_repository(path: Path, url: str) -> Optional[Repository]:
    for candidate in _repositories:
        if candidate.detect_project_type(path):
            return candidate(path=path, url=url)
    return None
