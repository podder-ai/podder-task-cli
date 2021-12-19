from .data import Data
from .dependency import Dependency
from .entity import Entity


class Package(Entity):
    _properties = {"name": str, "dependencies": [Dependency], "data": [Data]}
