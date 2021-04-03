from podder_task_cli.utilities import FileUtility


def test_instance_create():
    instance = FileUtility()
    assert instance is not None


def test_find_command():
    instance = FileUtility()
    result = instance.find_command("ls")
    assert result
