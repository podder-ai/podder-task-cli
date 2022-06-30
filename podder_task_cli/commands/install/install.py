from pathlib import Path

import click

from ...services import PodderService
from ...utilities import PoetryUtility


class Install(object):
    def __init__(self, path: Path):
        self._path = path
        self._podder_service = PodderService(project_path=path)

    def process(self):
        # library install
        click.secho("Install external libraries...")
        self._podder_service.install_libraries()

        # poetry install
        click.secho("Execute poetry install...")
        success = PoetryUtility().install(path=self._path)

        # download files
        click.secho("Download files...")
        self._podder_service.download_files()

        # execute commands
        click.secho("Execute commands...")
        self._podder_service.execute_command()
