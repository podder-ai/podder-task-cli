from pathlib import Path

from ...services import PodderService
from ...utilities import PoetryUtility, TerminalUtility


class Install(object):
    def __init__(self, path: Path):
        self._path = path
        self._podder_service = PodderService(project_path=path)
        self._terminal_utility = TerminalUtility()

    def process(self):
        # check podder.yaml file
        if not self._podder_service.has_project_config_file():
            self._terminal_utility.warning(
                "podder.yaml file not found: {}".format(
                    self._podder_service.get_project_config_path()))

        # library install
        self._terminal_utility.info("Install external libraries...")
        self._podder_service.install_libraries()

        # poetry install
        self._terminal_utility.info("Execute poetry install...")
        success = PoetryUtility().install(path=self._path)

        # download files
        self._terminal_utility.info("Download files...")
        self._podder_service.download_files()

        # execute commands
        self._terminal_utility.info("Execute commands...")
        self._podder_service.execute_command()
