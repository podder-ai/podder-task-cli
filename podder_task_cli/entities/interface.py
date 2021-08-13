from .entity import Entity


class Interface(Entity):
    def __init__(self, data):
        super().__init__(data)

    @property
    def name(self) -> str:
        return self.get("name", "")

    @property
    def entry(self) -> dict:
        return self.get("entry", {})

    @property
    def config(self) -> dict:
        return self.get("config", {})

    @property
    def method(self) -> str:
        return self.get("entry.method", "")

    @property
    def object(self) -> str:
        return self.get("entry.object", "")
