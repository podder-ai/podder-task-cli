from .entity import Entity


class Data(Entity):
    _properties = {
        "source_url": str,
        "destination_path": list,
    }
