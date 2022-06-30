import json
import random
from pathlib import Path
from tempfile import TemporaryDirectory

from podder_task_cli.services.podder_service.entities import Entity


def test_entity_create():
    entity = Entity({"key": "value"})
    assert entity is not None
