from pathlib import Path

from podder_task_cli.services.podder_service.library_manager import LibraryManager


def test_instance_create():
    instance = LibraryManager(project_path=Path("./"))
    assert instance is not None
