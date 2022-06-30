import os
from pathlib import Path
from tempfile import TemporaryDirectory

import click

from ...services import PackageService
from ...services.podder_service.entities import Entity
from ...utilities import GitUtility
from .import_library import ImportLibrary
from .import_project import ImportProject
from .sources import Library, Project, Source, get_source


class Import(object):
    _copy_files = ["__init__.py", "process.py"]
    _directories = ["config", "processes", "data", "input", "output"]

    def __init__(self, target_source: str, processes: [str], base_path: Path):
        self._target_source = target_source
        self._processes = list(processes)
        self._base_path = base_path

        self._template_directory = Path(__file__).parent.joinpath(
            "..", "templates")
        self._package_service = PackageService(self._base_path)

    def _is_source_local(self) -> bool:
        target_path = Path(self._target_source)
        if target_path.suffix == ".git":
            return False

        return True

    def process(self):
        temporary_directory_object = TemporaryDirectory()
        if self._is_source_local():
            destination_path = Path(self._target_source).resolve().absolute()
            if not destination_path.exists():
                click.secho("Source directory did not found: {}".format(
                    str(destination_path)),
                            fg="red")
                return False
        else:
            destination_path = Path(
                str(temporary_directory_object.name) + os.sep + "source")
            success = GitUtility().clone_source(self._target_source,
                                                destination_path)
            if not success:
                click.secho("Clone source failed: {}".format(
                    self._target_source),
                            fg="red")
                return False

        source = get_source(path=destination_path, url=self._target_source)

        if isinstance(source, Project):
            importer = ImportProject(source,
                                     base_path=self._base_path,
                                     processes=self._processes)
        elif isinstance(source, Library):
            importer = ImportLibrary(source,
                                     base_path=self._base_path,
                                     processes=self._processes)
        else:
            click.secho("Seems this source is not supported: {}".format(
                self._target_source),
                        fg="red")
            return False

        names = importer.execute()
        for name in names:
            self._set_metadata(name, source)

    def _set_metadata(self, name: str, source: Source):
        revision = source.revision
        target_source = self._target_source
        if self._is_source_local():
            target_source = "local"
        entity = Entity({
            "base_source": target_source,
            "revision": revision,
        })
        path = self._base_path.joinpath("processes", name,
                                        ".podder.process.conf")
        entity.save(path)
