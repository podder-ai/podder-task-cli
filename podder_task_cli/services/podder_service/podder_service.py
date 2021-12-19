from pathlib import Path
from typing import Optional

from ...utilities import TerminalUtility
from .global_config_manager import GlobalConfigManager
from .project_config_manager import ProjectConfigManager


class PodderService(object):
    project_config_file_name = "podder.yaml"

    def __init__(self, project_path: Optional[Path] = None):
        self._project_path = project_path
        self._project_config_manager = ProjectConfigManager(
            project_path=self._project_path)
        self._global_config_manager = GlobalConfigManager(
            project_path=self._project_path)

    def check_cli_version(self):
        latest_version = self._global_config_manager.check_cli_version()
        if latest_version:
            TerminalUtility().print(
                "Podder Task CLI new version is now available: Latest version: {}"
                .format(latest_version), TerminalUtility.Color.Warning)

    def get_registered_plugin_info(self):
        return self._global_config_manager.get_registered_plugin_info()
