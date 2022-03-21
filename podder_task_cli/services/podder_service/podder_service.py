import subprocess
from pathlib import Path
from typing import Optional, Tuple

from ...utilities import TerminalUtility
from .data_manager import DataManager
from .entities import Command
from .global_config_manager import GlobalConfigManager
from .library_manager import LibraryManager
from .project_config_manager import ProjectConfigManager


class PodderService(object):
    project_config_file_name = "podder.yaml"

    def __init__(self, project_path: Optional[Path] = None):
        self._project_path = project_path
        self._project_config_manager = ProjectConfigManager(
            project_path=self._project_path)
        self._global_config_manager = GlobalConfigManager(
            project_path=self._project_path)
        self._data_manager = DataManager(project_path=self._project_path)
        self._library_manager = LibraryManager(project_path=self._project_path)

    def check_cli_version(self):
        latest_version = self._global_config_manager.check_cli_version()
        if latest_version:
            TerminalUtility().print(
                "Podder Task CLI new version is now available: Latest version: {}"
                .format(latest_version),
                style=TerminalUtility.Style.Warning)

    def get_registered_plugin_info(self):
        return self._global_config_manager.get_registered_plugin_info()

    def install_libraries(self):
        self._library_manager.install_all(
            package=self._project_config_manager.project_config_file())

    def download_files(self):
        self._data_manager.download_all(
            package=self._project_config_manager.project_config_file())

    def execute_command(self) -> Tuple[bool, Optional[str]]:
        package = self._project_config_manager.project_config_file()
        commands: [Command] = package.commands
        if commands is None:
            return True, None

        for command in commands:
            if command.description is not None and command.description != "":
                TerminalUtility().print("[Execute Command] {}".format(
                    command.description))
            TerminalUtility().print("[Execute Command] {}".format(
                command.command))
            result = subprocess.run(command.command,
                                    shell=True,
                                    capture_output=True)
            if result.stderr != "":
                return False, result.stderr.decode(encoding="utf-8")

        return True, None
