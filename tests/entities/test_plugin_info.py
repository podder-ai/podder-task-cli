from podder_task_cli.entities import PluginInfo


def test_entity_create():
    entity = PluginInfo({
        "name": "podder-task-foundation-objects-image",
        "repository":
        "git@github.com:podder-ai/podder-task-foundation-objects-image.git",
        "branch": "main",
        "description": "Image ( PNG, JPEG, GIF ) support"
    })
    assert entity is not None
