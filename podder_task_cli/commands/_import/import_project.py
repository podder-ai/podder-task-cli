import shutil
from pathlib import Path

import click
from PyInquirer import prompt

from podder_task_cli.repositories import Project

from .import_base import ImportBase


class ImportProject(ImportBase):
    def __init__(self, repository: Project, base_path: Path):
        super().__init__(repository, base_path)
        self._repository = repository
        self._processes = []

    def execute(self) -> [str]:
        processes = self._repository.get_process_list()
        if self._processes is None or len(self._processes) == 0:
            self._processes = self._select_processes(processes)
        else:
            for process in self._processes:
                if process not in processes:
                    click.secho(
                        "Cannot find process {} in the repository".format(
                            self._repository.url),
                        fg="red")
                    return False

        for process in self._processes:
            self._import_process(process, self._repository.path)

        return self._processes

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
        path = self._base_path.joinpath("processes", process_name)
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

    def _copy_process(self, name: str, source_directory: Path):
        shutil.copytree(source_directory.joinpath("processes", name),
                        self._base_path.joinpath("processes", name))
        for directory_name in ["config", "data", "input", "output"]:
            if source_directory.joinpath(directory_name, name).exists():
                shutil.copytree(
                    source_directory.joinpath(directory_name, name),
                    self._base_path.joinpath(directory_name, name))
            else:
                self._base_path.joinpath(directory_name, name).mkdir()
