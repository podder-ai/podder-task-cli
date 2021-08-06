from pathlib import Path

import click

from ...services import PackageService, PodderService
from .plugin import Plugin


class List(Plugin):
    def process(self):
        podder_service = PodderService()
        package_service = PackageService(Path(self._path))

        registered_plugins = podder_service.get_registered_plugin_info()
        installed_plugins = package_service.get_installed_plugins()

        click.secho('Installed Plugins', fg="green", bold=True)
        for plugin_type in installed_plugins.keys():
            for plugin_name in installed_plugins[plugin_type].keys():
                plugin_info = installed_plugins[plugin_type][plugin_name]
                click.secho('* {}: {}'.format(plugin_info["name"],
                                              plugin_info["version"]))

        click.secho('Available Plugins', fg="green", bold=True)
        for plugin_type in registered_plugins.keys():
            for plugin_name in registered_plugins[plugin_type].keys():
                plugin_info = registered_plugins[plugin_type][plugin_name]
                click.secho('* {}: {}'.format(plugin_info.name,
                                              plugin_info.description))
