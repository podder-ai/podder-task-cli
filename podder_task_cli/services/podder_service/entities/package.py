from ._import import Import
from .command import Command
from .data import Data
from .entity import Entity


class Package(Entity):
    _properties = {
        "name": str,
        "imports": [Import],
        "data": [Data],
        "external_libraries": [str],
        "commands": [Command]
    }
