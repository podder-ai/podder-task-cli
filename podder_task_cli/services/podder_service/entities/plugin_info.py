from .entity import Entity


class PluginInfo(Entity):
    _properties = {
        "name": str,
        "repository": str,
        "description": str,
        "branch": str
    }
