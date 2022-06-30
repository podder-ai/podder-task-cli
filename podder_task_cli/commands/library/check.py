import click

from ...services.podder_service.entities import Interface
from .library import Library


class Check(Library):
    def execute(self):
        is_podder_based_source = self._check_podder_based_source()
        if is_podder_based_source:
            click.secho(
                "This podder based project. No need to set up as a library",
                fg="yellow")
            click.secho(
                "You can import any of the process to other projects with `podder import` command."
            )
            return

        success = self._check_podder_directory()
        if not success:
            return

        interface_path = self._path.joinpath(".podder", "interface.json")
        interface = Interface(interface_path.read_text())
        if interface.object == "":
            click.secho("interface.json has no entry object name", fg="red")
            return
        if interface.method == "":
            click.secho("interface.json has no entry method name", fg="red")
            return

        click.secho("Interface File: {}".format(str(
            interface_path.absolute())))
        click.secho("Entry Point: {}.{}".format(interface.object,
                                                interface.method))

    def _check_podder_based_source(self) -> bool:
        processes_exists = self.get_path("processes").exists()
        config_exists = self.get_path("config").exists()
        manage_exists = self.get_path("manage.py").exists()
        if processes_exists and config_exists and manage_exists:
            return True

        return False

    def _check_podder_directory(self) -> bool:
        podder_path = self.get_podder_directory_path()
        if not podder_path.exists():
            click.secho("There is no .podder directory on this directory.",
                        fg="yellow")
            click.secho(
                "If you want to set up as an library, you may, use `podder library init` command."
            )
            return False

        if not podder_path.is_dir():
            click.secho("There is .podder file but it is not a directory.",
                        fg="red")
            return False

        interface_path = self._path.joinpath(".podder", "interface.json")
        if not interface_path.exists():
            click.secho("There is no interface.json in the .podder directory.",
                        fg="red")
            return False

        return True
