from pathlib import Path

from podder_task_cli.services import PodderService


def test_instance_create():
    instance = PodderService(path=Path("./"))
    assert instance is not None
