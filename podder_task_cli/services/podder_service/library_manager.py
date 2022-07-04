import subprocess
from pathlib import Path
from typing import Dict, Optional

import click
import yaml

from ...utilities import ExternalCommandUtility, PlatformUtility, TerminalUtility
from .entities import Package


class LibraryManager(object):
    def __init__(self, project_path: Path):
        self._project_path = project_path
        self._platform = PlatformUtility().get_platform()
        self._terminal_utility = TerminalUtility()

    def install(self, name: str) -> bool:
        if self._platform == PlatformUtility.Platform.Unknown:
            return False
        formula = self._get_formula(name)
        if formula is None:
            self._terminal_utility.warning(
                "library {} is not supported in PodderTaskCLI, please make sure it is installed"
                .format(name))
            return False

        if self._platform not in formula:
            self._terminal_utility.warning(
                "PodderTaskCLI can not install library {} automatically on this platform,"
                + " please make sure it is installed".format(name))
            return False

        platform_formula = formula[self._platform]

        # check if the library already been installed or not
        if "check" in platform_formula:
            if ExternalCommandUtility.check_command(platform_formula["check"]):
                self._terminal_utility.info("{} exists already".format(name))
                return True

        if "command" in platform_formula:
            self._terminal_utility.info("Installing {} ...".format(name))
            for command in platform_formula["command"]:
                command = command.strip()
                self._terminal_utility.print(command)
                result = subprocess.run(command,
                                        shell=True,
                                        capture_output=True)
                if result.stderr != "":
                    click.secho(result.stderr.decode(encoding="utf-8"),
                                fg="red")
                    return False
            return True
        elif "message" in platform_formula:
            self._terminal_utility.warning(
                "PodderTaskCLI can not install library {} automatically on this platform."
                + " Refer this message: {}".format(
                    name, platform_formula["message"]))
            return False

    def install_all(self, package: Package):
        if package is None:
            return
        libraries = package.external_libraries
        if libraries is not None:
            for library in libraries:
                self.install(library)

    @staticmethod
    def _get_formula(name: str) -> Optional[Dict]:
        formulae_path = Path(__file__).parent.parent.parent.joinpath(
            "formulae")
        if not formulae_path.exists():
            return None
        formula_path = formulae_path.joinpath("{}.yaml".format(name))
        if not formula_path.exists():
            return None

        return yaml.load(formula_path.read_text(encoding="utf-8"),
                         Loader=yaml.SafeLoader)
