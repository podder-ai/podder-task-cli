from pathlib import Path
from typing import Optional

import click
from rich.prompt import Confirm, Console

from ...entities import PluginInfo
from ...services import PackageService, PodderService
from .plugin import Plugin


class Install(Plugin):
    def __init__(self, path: Path):
        super().__init__(path)
        self._package_service = PackageService(self._path)
        self._podder_service = PodderService()

    def process(self, plugin_name: str, version: Optional[str] = None):
        if plugin_name.endswith(".git"):
            success = self._install_plugin_by_git(plugin_name, version)
        else:
            plugin_info = self._find_plugin_from_registry(plugin_name)
            if plugin_info is None:
                click.secho(
                    "Plugin {} is not registered in the registry".format(
                        plugin_name),
                    fg="red")
                return

            print(plugin_info.repository)
            current_version = self._find_plugin_from_installed_plugins(
                plugin_name)
            if current_version is None:
                success = self._install_plugin_by_git(plugin_info.repository,
                                                      plugin_info.branch)
            else:
                console = Console()
                console.print(
                    "\n{} is already installed ( Installed version: {} ).".
                    format(plugin_name, current_version))
                if not Confirm.ask('Do you want to update to new version?'):
                    return
                success = self._update_plugin_by_git(plugin_info.repository,
                                                     plugin_info.branch)

        if not success:
            click.secho("Failed to install plugin {}".format(plugin_name),
                        fg="red")

    def _find_plugin_from_registry(self,
                                   plugin_name: str) -> Optional[PluginInfo]:
        registered_plugins = self._podder_service.get_registered_plugin_info()
        for plugin_type in registered_plugins.keys():
            if plugin_name in registered_plugins[plugin_type]:
                return registered_plugins[plugin_type][plugin_name]

        return None

    def _find_plugin_from_installed_plugins(self,
                                            plugin_name: str) -> Optional[str]:
        installed_plugins = self._package_service.get_installed_plugins()
        for plugin_type in installed_plugins.keys():
            if plugin_name in installed_plugins[plugin_type]:
                return installed_plugins[plugin_type][plugin_name]["version"]

        return None

    @staticmethod
    def _get_url_for_poetry(git_url: str, version: Optional[str]) -> str:
        if not git_url.startswith("https://"):
            git_url = "git+ssh://" + git_url
        if version is not None:
            git_url = "{}#{}".format(git_url, version)

        return git_url

    def _install_plugin_by_git(self, git_url: str,
                               version: Optional[str]) -> bool:
        click.secho("Installing plugin...", fg="green")
        git_url = self._get_url_for_poetry(git_url, version)
        return self._package_service.install_package(git_url)

    def _update_plugin_by_git(self, git_url: str,
                              version: Optional[str]) -> bool:
        click.secho("Updating plugin...", fg="green")
        git_url = self._get_url_for_poetry(git_url, version)
        return self._package_service.update_package(git_url)
