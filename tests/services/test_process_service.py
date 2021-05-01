from podder_task_cli.services import ProcessService
from pathlib import Path


def test_instance_create():
    instance = ProcessService(path=Path("./"))
    assert instance is not None
