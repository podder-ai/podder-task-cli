import os
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional

import click

from ...entities import Entity
from ...repositories import Library, Project, Repository, get_repository
from ...services import PackageService
from ...utilities import GitUtility
from .import_library import ImportLibrary
from .import_project import ImportProject


class Import(object):
    _copy_files = ["__init__.py", "process.py"]
    _directories = ["config", "processes", "data", "input", "output"]

    def __init__(self, target_repository: str, processes: [str],
                 base_path: Path):
        self._target_repository = target_repository
        self._processes = list(processes)
        self._base_path = base_path
        self._template_directory = Path(__file__).parent.joinpath(
            "..", "templates")
        self._package_service = PackageService(self._base_path)

    def process(self):
        temporary_directory_object = TemporaryDirectory()
        destination_path = Path(
            str(temporary_directory_object.name) + os.sep + "repository")
        success = GitUtility().clone_repository(self._target_repository,
                                                destination_path)
        if not success:
            click.secho("Clone repository failed: {}".format(
                self._target_repository),
                        fg="red")
            return False
        repository = get_repository(path=destination_path,
                                    url=self._target_repository)

        if isinstance(repository, Project):
            importer = ImportProject(repository, base_path=self._base_path)
        elif isinstance(repository, Library):
            importer = ImportLibrary(repository, base_path=self._base_path)
        else:
            click.secho("Seems this repository is not supported: {}".format(
                self._target_repository),
                        fg="red")
            return False

        names = importer.execute()
        for name in names:
            self._set_metadata(name, repository)

    def _set_metadata(self, name: str, repository: Repository):
        revision = repository.revision
        entity = Entity({
            "base_repository": self._target_repository,
            "revision": revision,
        })
        path = self._base_path.joinpath("processes", name,
                                        ".podder.process.conf")
        entity.save(path)

    def _get_metadata(self, name: str) -> Optional[Entity]:
        path = self._base_path.joinpath("processes", name,
                                        ".podder.process.conf")
        if not path.exists():
            return None
        entity = Entity.load(path)
        return entity
