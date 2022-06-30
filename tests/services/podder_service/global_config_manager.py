from pathlib import Path

from podder_task_cli.services.podder_service.global_config_manager import GlobalConfigManager


def test_instance_create():
    instance = GlobalConfigManager(project_path=Path("./"))
    assert instance is not None
