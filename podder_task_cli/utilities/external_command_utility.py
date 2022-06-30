import itertools
import subprocess
import time
from pathlib import Path
from typing import List, Optional, Tuple, Union

import click

from .terminal_utility import TerminalUtility


class ExternalCommandUtility(object):
    @staticmethod
    def execute_command(
        commands: Union[List[str], str],
        working_directory: Optional[Path] = None,
        show_loading_animation: bool = False
    ) -> Tuple[Optional[str], Optional[str]]:
        if isinstance(commands, str):
            commands = [commands]
        process = subprocess.Popen(commands, cwd=working_directory)
        terminal_utility = TerminalUtility()

        for c in itertools.cycle(['|', '/', '-', '\\']):
            if process.poll():
                break
            terminal_utility.print(
                "\r Executing external commands ... {}".format(c),
                new_line=False)
            time.sleep(0.1)
        terminal_utility.print("\r")

        return process.stdout, process.stderr
