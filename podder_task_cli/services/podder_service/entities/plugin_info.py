from .entity import Entity


class PluginInfo(Entity):
    _properties = {
        "name": str,
        "source": str,
        "description": str,
        "branch": str
    }
