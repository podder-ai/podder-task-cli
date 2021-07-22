import os
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional

import click
from PyInquirer import prompt

from ..entities import Entity
from ..repositories import Repository
from ..utilities import GitUtility


class Import(object):
    _copy_files = ["__init__.py", "process.py"]
    _directories = ["config", "processes", "data", "input", "output"]

    def __init__(self, target_repository: str, processes: [str],
                 base_directory: Path):
        self._target_repository = target_repository
        self._processes = list(processes)
        self._base_directory = base_directory
        self._template_directory = Path(__file__).parent.joinpath(
            "..", "templates")

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
        repository = Repository(destination_path)
        if repository.type == Repository.TYPE.PROJECT:
            self._import_from_project(repository, destination_path)
        elif repository.type == Repository.TYPE.LIBRARY:
            self._import_from_library(repository, destination_path)
        else:
            click.secho("Seems this repository is not supported: {}".format(
                self._target_repository),
                        fg="red")
            return False

    def _import_from_library(self, repository: Repository,
                             destination_path: Path):
        pass

    def _import_from_project(self, repository: Repository,
                             destination_path: Path):
        processes = repository.get_process_list()
        if self._processes is None or len(self._processes) == 0:
            self._processes = self._select_processes(processes)
        else:
            for process in self._processes:
                if process not in processes:
                    click.secho(
                        "Cannot find process {} in the repository".format(
                            self._target_repository),
                        fg="red")
                    return False

        for process in self._processes:
            self._import_process(process, destination_path)

    @staticmethod
    def _select_processes(processes: [str]) -> [str]:
        choices = []
        for process in processes:
            choices.append({
                "name": process,
            })
        questions = [
            {
                'type': 'checkbox',
                'qmark': '>',
                'message': 'Select processes which you want to import to your project',
                'name': 'processes',
                'choices': choices,
                'validate': lambda answer: 'You must select at least one process.' \
                    if len(answer) == 0 else True
            }
        ]
        answers = prompt(questions)
        return answers["processes"]

    def _check_process(self, process_name):
        path = self._base_directory.joinpath("processes", process_name)
        if not path.exists():
            return True
        entity = self._get_metadata(process_name)
        if entity is None:
            click.secho("Process {} already exists.".format(process_name),
                        fg="red")
            return False
        if entity.base_repository != self._target_repository:
            click.secho(
                "Process {} already exists and imported from different repository {}."
                .format(process_name, entity.base_repository),
                fg="red")
            return False

        click.secho(
            "Process {} already exists and imported from the same repository.".
            format(process_name, entity.base_repository),
            fg="red")
        return False

    def _import_process(self, process_name: str, source_directory: Path):
        click.secho("Importing process: {} ...".format(process_name),
                    fg="green")
        result = self._check_process(process_name)
        if result:
            self._copy_process(process_name, source_directory)
            self._set_metadata(process_name, source_directory)

    def _copy_process(self, name: str, source_directory: Path):
        shutil.copytree(source_directory.joinpath("processes", name),
                        self._base_directory.joinpath("processes", name))
        for directory_name in ["config", "data", "input", "output"]:
            if source_directory.joinpath(directory_name, name).exists():
                shutil.copytree(
                    source_directory.joinpath(directory_name, name),
                    self._base_directory.joinpath(directory_name, name))
            else:
                self._base_directory.joinpath(directory_name, name).mkdir()

    def _set_metadata(self, name: str, repository_path: Path):
        revision = GitUtility().get_revision(repository_path)
        entity = Entity({
            "base_repository": self._target_repository,
            "revision": revision,
        })
        path = self._base_directory.joinpath("processes", name,
                                             ".podder.process.conf")
        entity.save(path)

    def _get_metadata(self, name: str) -> Optional[Entity]:
        path = self._base_directory.joinpath("processes", name,
                                             ".podder.process.conf")
        if not path.exists():
            return None
        entity = Entity.load(path)
        return entity
