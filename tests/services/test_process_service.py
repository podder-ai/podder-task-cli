from pathlib import Path

from podder_task_cli.services import ProcessService


def test_instance_create():
    instance = ProcessService(path=Path("./"))
    assert instance is not None
