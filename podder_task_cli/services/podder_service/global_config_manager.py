import time
from pathlib import Path
from typing import Optional, Tuple

import requests
import toml
import yaml
from packaging import version

from podder_task_cli.utilities import GitUtility

from .entities import PluginInfo


class GlobalConfigManager(object):
    version_uri = "https://raw.githubusercontent.com/podder-ai/podder-task-cli/main/pyproject.toml"
    plugin_repository = "git@github.com:podder-ai/podder-task-foundation-plugin-registry.git"

    def __init__(self, project_path: Optional[Path] = None):
        self._project_path = project_path
        self._podder_config_path = self.get_default_directory()

    @staticmethod
    def get_default_directory() -> Path:
        return Path.home().joinpath(".podder")

    def get_target_file_path(self, name: str):
        if not self._podder_config_path.exists():
            self._podder_config_path.mkdir()
        return self._podder_config_path.joinpath(name)

    def get_plugin_info_path(self) -> Path:
        return self._podder_config_path.joinpath("plugins")

    def get_cli_version_info_path(self) -> Path:
        return self._podder_config_path.joinpath("version.yaml")

    def download_plugin_information(self) -> bool:
        checkout_path = self.get_plugin_info_path()
        if checkout_path.exists():
            success = GitUtility().update_repository(checkout_path)
        else:
            success = GitUtility.clone_repository(self.plugin_repository,
                                                  checkout_path)
        return success

    def get_registered_plugin_info(self) -> Optional[dict]:
        checkout_path = self.get_plugin_info_path()
        success = self.download_plugin_information()
        if not success:
            return None
        results = {}
        for directory in checkout_path.glob("*"):
            if not directory.name.startswith(".") and directory.is_dir():
                results[directory.name] = {}
                for plugin in directory.glob("**/*.json"):
                    plugin_info = PluginInfo.load(plugin)
                    results[directory.name][plugin_info.name] = plugin_info

        return results

    def check_cli_version(self) -> Optional[str]:
        current_version = version.parse(self.get_current_cli_version())
        latest_version, latest_update = self.get_current_cli_version()
        if latest_version is None:
            self.download_latest_cli_version()
            return None

        latest_version = version.parse(latest_version)
        if latest_update + 86400 < int(time.time()):
            self.download_latest_cli_version()

        if current_version < latest_version:
            return str(latest_version)

        return None

    @staticmethod
    def get_current_cli_version():
        from podder_task_cli import __version__
        return __version__

    def get_stored_cli_version(self) -> Optional[Tuple[str, int]]:
        version_path = self.get_cli_version_info_path()
        if not version_path.exists():
            return None
        with version_path.open(encoding="utf-8") as file:
            data = yaml.safe_load(file)
            if "version" not in data:
                return None

            version = data["version"]
            if "last_update_time" in data and isinstance(
                    data["last_update_time"], int):
                last_update_time = data["last_update_time"]
            else:
                last_update_time = int(time.time())

            return version, last_update_time

    async def download_latest_cli_version(self) -> Optional[Tuple[str, int]]:
        response = requests.get(self.version_uri)
        if response.status_code != 200:
            return None

        data = toml.loads(response.text)
        if "tool.poetry" in data and "version" in data["tool.poetry"]:
            return data["tool.poetry"]["version"], int(time.time())

        return None
