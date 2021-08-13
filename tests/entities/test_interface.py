from podder_task_cli.entities import Interface


def test_entity_create():
    entity = Interface({
        "name": "deskew",
        "entry": {
            "object": "deskew.Deskew",
            "method": "deskew",
            "input": [
                "image"
            ],
            "output": [
                "image",
                "dictionary"
            ]
        },
        "config": {
            "path": [
                "deskew",
                "config.py"
            ],
            "name": "Config"
        }
    })
    assert entity is not None
