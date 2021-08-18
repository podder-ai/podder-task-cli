import click

from .library import Library


class Initialize(Library):
    def execute(self):
        directory_path = self.get_podder_directory_path()
        if directory_path.exists():
            click.secho(".podder directory exists.", fg="yellow")
            return

        directory_path.mkdir()
