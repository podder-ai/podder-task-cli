from pathlib import Path

from podder_task_cli.services.podder_service.project_config_manager import ProjectConfigManager


def test_instance_create():
    instance = ProjectConfigManager(project_path=Path("./"))
    assert instance is not None
