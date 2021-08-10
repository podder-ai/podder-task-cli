from .entity import Entity


class PluginInfo(Entity):
    @property
    def name(self) -> str:
        return self.get("name", "")

    @property
    def repository(self) -> str:
        return self.get("repository", "")

    @property
    def description(self) -> str:
        return self.get("description", "")

    @property
    def branch(self) -> str:
        return self.get("branch", "")
