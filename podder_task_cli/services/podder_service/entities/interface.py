from .entity import Entity


class Interface(Entity):
    _properties = {
        "name": str,
        "entry": dict,
        "config": dict,
        "method": str,
        "object": str
    }
