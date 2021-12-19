from .entity import Entity


class Dependency(Entity):
    _properties = {
        "name": str,
        "source_repository": str,
        "version": str,
        "source_process": str,
    }
