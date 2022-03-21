from pathlib import Path

from podder_task_cli.services.podder_service.data_manager import DataManager


def test_instance_create():
    instance = DataManager(project_path=Path("./"))
    assert instance is not None
