import json
import random
from pathlib import Path
from tempfile import TemporaryDirectory

from podder_task_cli.entities import Entity


def test_entity_create():
    entity = Entity({"key": "value"})
    assert entity is not None


def test_entity_get_value():
    value = random.randint(1, 1000)
    entity = Entity({"key": value})
    assert entity.key == value


def test_entity_save_value():
    with TemporaryDirectory() as temp_directory:
        target_file = Path(temp_directory).joinpath("test.json")
        value = random.randint(1, 1000)
        entity = Entity({"key": value})
        entity.save(target_file)

        data = target_file.read_text()
        result = json.loads(data)

        assert "key" in result
        assert result["key"] == value


def test_entity_load_value():
    with TemporaryDirectory() as temp_directory:
        target_file = Path(temp_directory).joinpath("test.json")
        value = random.randint(1, 1000)
        test_data = json.dumps({"key": value})
        target_file.write_text(test_data)
        entity = Entity.load(target_file)

        assert entity.key == value
