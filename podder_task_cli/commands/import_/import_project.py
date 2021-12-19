import shutil
from pathlib import Path

import click
from PyInquirer import prompt

from ...services import PackageService
from .import_base import ImportBase
from .sources import Project


class ImportProject(ImportBase):
    def __init__(self, source: Project, base_path: Path):
        super().__init__(source, base_path)
        self._source = source
        self._processes = []
        self._package_service = PackageService(base_path)

    def execute(self) -> [str]:
        imported_processes = []
        processes = self._source.get_process_list()
        if self._processes is None or len(self._processes) == 0:
            self._processes = self._select_processes(processes)
        else:
            for process in self._processes:
                if process not in processes:
                    click.secho("Cannot find process {} in the source".format(
                        self._source.url),
                                fg="red")
                    return False

        for process in self._processes:
            can_continue = self._check_exisiting_process(
                process, self._source.path)
            if not can_continue:
                continue
            self._import_process(process, self._source.path)
            imported_processes.append(process)

        self._processes = imported_processes
        if len(imported_processes) > 0:
            self._add_required_libraries()

        return self._processes

    @staticmethod
    def _select_processes(processes: [str]) -> [str]:
        choices = []
        for process in processes:
            choices.append({
                "name": process,
            })
        questions = [{
            'type':
            'checkbox',
            'qmark':
            '>',
            'message':
            'Select processes which you want to import to your project',
            'name':
            'processes',
            'choices':
            choices,
            'validate':
            lambda answer: 'You must select at least one process.'
            if len(answer) == 0 else True
        }]
        answers = prompt(questions)
        return answers["processes"]

    def _import_process(self, process_name: str, source_directory: Path):
        click.secho("Importing process: {} ...".format(process_name),
                    fg="green")
        self._copy_process(process_name, source_directory)

    def _get_process_directory(self, process_name: str) -> Path:
        return self._base_path.joinpath("processes", process_name)

    def _get_config_directory(self, process_name: str) -> Path:
        return self._base_path.joinpath("config", process_name)

    def _check_exisiting_process(self, process_name: str,
                                 source_directory: Path) -> bool:
        process_directory = self._get_process_directory(process_name)
        if process_directory.exists():

            entity = self._get_metadata(process_name)
            message = 'Process [{}] already exists. Do yo want to overwrite?'.format(
                process_name)
            if entity:
                if entity.base_source != self._source.url:
                    message = 'Process [{}] already exists but came from different source. Do yo want to overwrite?'.format(
                        process_name)

            questions = [{
                'type': 'confirm',
                'message': message,
                'name': 'overwrite',
                'default': False,
            }]
            answers = prompt(questions)
            return answers["overwrite"]

        config_directory = self._get_config_directory(process_name)
        if config_directory.exists():
            questions = [{
                'type':
                'confirm',
                'message':
                'Process [{}] config directory already exists ( process directory does not exist ). Do yo want to overwrite?'
                .format(process_name),
                'name':
                'overwrite',
                'default':
                False,
            }]
            answers = prompt(questions)
            return answers["overwrite"]

        return True

    def _copy_process(self, name: str, source_directory: Path):
        process_path = self._get_process_directory(name)
        if process_path.exists():
            shutil.rmtree(process_path)
        shutil.copytree(source_directory.joinpath("processes", name),
                        process_path)
        for directory_name in ["config", "data", "input", "output"]:
            target_path = self._base_path.joinpath(directory_name, name)
            if target_path.exists():
                shutil.rmtree(target_path)

            if source_directory.joinpath(directory_name, name).exists():
                shutil.copytree(
                    source_directory.joinpath(directory_name, name),
                    self._base_path.joinpath(directory_name, name))
            else:
                self._base_path.joinpath(directory_name, name).mkdir()

    def _add_required_libraries(self):
        for process in self._processes:
            process_path = self._base_path.joinpath("processes", process,
                                                    "process.py")
            libraries = self._package_service.get_all_used_packages(
                process_path)
