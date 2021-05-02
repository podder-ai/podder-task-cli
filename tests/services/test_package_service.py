from pathlib import Path

from podder_task_cli.services import PackageService


def test_instance_create():
    instance = PackageService(path=Path("./"))
    assert instance is not None
