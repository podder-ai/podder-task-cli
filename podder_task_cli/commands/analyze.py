import json
from pathlib import Path
from typing import Any, Dict, Optional

import click

from ..services import PackageService, ProcessService


class Analyze(object):
    def __init__(self, path: Path):
        self._path = path
        self._package_service = PackageService(self._path)
        self._process_service = ProcessService(self._path)

    def process(self, json_output: bool = False):
        info = self._build_information()
        if json_output:
            self._output_json(info)
        else:
            self._output_human_readable(info)

    @staticmethod
    def _output_json(info: dict):
        click.echo(json.dumps(info))

    @staticmethod
    def _output_human_readable(info: dict):
        if info is None:
            click.secho('Could not find podder-task-foundation', fg='red')
            return

        click.secho('Podder Task Foundation', fg="green", bold=True)
        click.secho('    Version: {}'.format(
            info["podder-task-foundation"]["version"]))
        click.secho('    Plugins:')
        for plugin_type in info["podder-task-foundation"]["plugins"].keys():
            click.secho('        {}:'.format(plugin_type), bold=True)
            for plugin in info["podder-task-foundation"]["plugins"][
                    plugin_type].keys():
                plugin_info = info["podder-task-foundation"]["plugins"][
                    plugin_type][plugin]
                click.secho('            {}: {}'.format(
                    plugin, plugin_info["version"]))

        click.secho('\nProcesses', fg="green", bold=True)
        for process in info["processes"]:
            click.secho('    {}'.format(process))

    def _build_information(self) -> Optional[Dict[str, Any]]:
        version = self._package_service.get_podder_task_foundation_version()
        if version is None:
            return None
        plugins = self._package_service.get_all_plugins()
        processes = self._process_service.get_process_list()

        return {
            "podder-task-foundation": {
                "version": version,
                "plugins": plugins,
            },
            "processes": processes
        }
