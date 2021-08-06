from .library import Library


class Initialize(Library):
    def execute(self):
        directory_path = self.get_podder_directory_path()
