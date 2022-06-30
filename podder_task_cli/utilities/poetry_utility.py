from pathlib import Path
from typing import List, Tuple, Union

import click

from .external_command_utility import ExternalCommandUtility
from .terminal_utility import TerminalUtility


class PoetryUtility(ExternalCommandUtility):
    def execute_poetry_command(self, commands: Union[str, List[str]],
                               path: Path) -> Tuple[str, str]:
        if isinstance(commands, str):
            commands = [commands]
        poetry_commands = ["poetry"]
        poetry_commands.extend(commands)
        return self.execute_command(poetry_commands, working_directory=path)

    def install(self, path: Path) -> bool:
        result, error = self.execute_command("install",
                                             working_directory=path,
                                             show_loading_animation=True)
        return error is None

    def add(self, package_name: str, path: Path) -> bool:
        result, error = self.execute_command(["add", package_name],
                                             working_directory=path)
        if error is not None:
            TerminalUtility.print(error, style=TerminalUtility.Style.Error)
        return error is None
