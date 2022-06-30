from pathlib import Path
from typing import Optional

from podder_task_cli.utilities import GitUtility

from .data_manager import DataManager
from .entities import Package, PluginInfo


class ProjectConfigManager(object):
    project_config_file_name = "podder.yaml"

    def __init__(self, project_path: Optional[Path] = None):
        self._project_path = project_path
        self._podder_config_path = self.get_project_config_path()
        self._project_config = self.load_project_config()

    def get_project_config_path(self) -> Path:
        return self._project_path.joinpath(self.project_config_file_name)

    def load_project_config(self) -> Optional[Package]:
        config_path = self._podder_config_path
        if not config_path.exists():
            return None

        package = Package(path=config_path)
        return package

    def project_config_file(self) -> Optional[Package]:
        return self._project_config
