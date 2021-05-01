from podder_task_cli.services import PackageService
from pathlib import Path


def test_instance_create():
    instance = PackageService(path=Path("./"))
    assert instance is not None
