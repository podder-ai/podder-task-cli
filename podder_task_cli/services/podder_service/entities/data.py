from .entity import Entity


class Data(Entity):
    _properties = {
        "type": str,
        "source_url": str,
        "destination_path": list,
    }
