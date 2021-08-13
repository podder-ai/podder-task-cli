from pathlib import Path
from typing import Optional

from ..entities import PluginInfo
from ..utilities import GitUtility


class PodderService(object):
    def __init__(self, path: Optional[Path] = None):
        self._podder_config_path = path
        if self._podder_config_path is None:
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

    def download_plugin_information(self) -> bool:
        checkout_path = self.get_plugin_info_path()
        if checkout_path.exists():
            success = GitUtility().update_repository(checkout_path)
        else:
            success = GitUtility.clone_repository(
                "git@github.com:podder-ai/podder-task-foundation-plugin-registry.git",
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
