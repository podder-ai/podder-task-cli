from podder_task_cli.services.podder_service.entities import Interface


def test_interface_create():
    entity = Interface({
        "name": "deskew",
        "entry": {
            "object": "deskew.Deskew",
            "method": "deskew",
            "input": ["image"],
            "output": ["image", "dictionary"]
        },
        "config": {
            "path": ["deskew", "config.py"],
            "name": "Config"
        }
    })
    assert entity is not None


def test_get_interface_name():
    entity = Interface({
        "name": "deskew",
        "entry": {
            "object": "deskew.Deskew",
            "method": "deskew",
            "input": ["image"],
            "output": ["image", "dictionary"]
        },
        "config": {
            "path": ["deskew", "config.py"],
            "name": "Config"
        }
    })
    assert entity.name == "deskew"
