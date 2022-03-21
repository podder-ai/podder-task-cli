from .entity import Entity


class Command(Entity):
    _properties = {
        "command": str,
        "description": str,
    }
