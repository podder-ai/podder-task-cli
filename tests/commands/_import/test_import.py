from pathlib import Path

from podder_task_cli.commands.import_ import Import


def test_instance_create():
    instance = Import(
        target_source="git@github.com:podder-ai/podder-task-base.git",
        base_path=Path(__file__).parent.joinpath("_data"),
        processes=[])
    assert instance is not None
