import re
import shutil
from pathlib import Path

import click
from PyInquirer import prompt

from ..utilities import FileUtility, ProcessUtility


class Process(object):
    _copy_files = ["__init__.py", "process.py"]
    _directories = ["config", "processes", "data", "input", "output"]

    def __init__(self, name: str, base_directory: Path):
        self._name = name
        self._process_name = self._convert_kebab_to_snake(name)
        self._base_directory = base_directory
        self._template_directory = Path(__file__).parent.joinpath(
            "..", "templates")

    def process(self):
        data = {
            "input": self.ask_about_interface("input"),
            "output": self.ask_about_interface("output"),
        }
        self.prepare_directory()
        self.copy_files()
        self.update_files(data)

    def _get_process_path(self) -> Path:
        return self._base_directory.joinpath("processes", self._process_name)

    def prepare_directory(self):
        click.secho("Creating directory for your process named {}...".format(
            self._name),
                    fg="green")
        for directory in self._directories:
            original_path = self._base_directory.joinpath(directory).joinpath(
                "task_name")
            renamed_path = self._base_directory.joinpath(directory).joinpath(
                self._process_name)
            if original_path.exists():
                original_path.rename(renamed_path)
            else:
                renamed_path.mkdir(parents=True)

    def copy_files(self):
        click.secho("Copying template files for your process...", fg="green")
        target_directory = self._get_process_path()
        for file in self._copy_files:
            template = self._template_directory.joinpath(file + ".tmpl")
            target = target_directory.joinpath(file)
            shutil.copy(str(template), str(target))

    def update_files(self, data: dict):
        process_utility = ProcessUtility()
        input_codes = []
        output_codes = []
        if data["input"]["count"] > 0:
            for index in range(0, data["input"]["count"]):
                name_key = "name_{}".format(index + 1)
                type_key = "type_{}".format(index + 1)
                input_codes.extend(
                    process_utility.generate_input_code(
                        data["input"][name_key], data["input"][type_key]))

        if data["output"]["count"] > 0:
            for index in range(0, data["output"]["count"]):
                name_key = "name_{}".format(index + 1)
                type_key = "type_{}".format(index + 1)
                output_codes.extend(
                    process_utility.generate_output_code(
                        data["output"][name_key], data["output"][type_key]))

        data["input_code"] = "\n" + "\n".join(
            ["        " + line for line in input_codes])
        data["output_code"] = "\n" + "\n".join(
            ["        " + line for line in output_codes])
        process_file = self._get_process_path().joinpath("process.py")
        FileUtility().update_target_file(process_file, data)

    @staticmethod
    def ask_about_interface(interface_type: str) -> dict:
        count_key = 'count'
        answers = prompt([{
            'type':
            'input',
            'name':
            count_key,
            'message':
            'How many {} you want to take'.format(interface_type),
            'filter':
            lambda number: int(number),
            'default':
            "1",
            'validate':
            lambda number: bool(re.match('^[0-9]+$', number))
        }])
        if count_key not in answers:
            raise KeyboardInterrupt

        if answers[count_key] > 0:
            for index in range(0, answers[count_key]):
                name_key = "name_{}".format(index + 1)
                type_key = "type_{}".format(index + 1)
                index_answers = prompt([
                    {
                        'type':
                        'input',
                        'name':
                        name_key,
                        'message':
                        'Input the name of {} no.{}'.format(
                            interface_type, index + 1),
                        'filter':
                        lambda name: None if name == "" else name,
                        'default':
                        name_key,
                        'validate':
                        lambda name: " " not in name
                    },
                    {
                        'type':
                        'list',
                        'name':
                        type_key,
                        'message':
                        'Select the data type of {} no.{}'.format(
                            interface_type, index + 1),
                        'choices':
                        list(ProcessUtility.object_types.keys()),
                    },
                ])
                if name_key not in index_answers or type_key not in index_answers:
                    raise KeyboardInterrupt

                answers.update(index_answers)

        return answers

    @staticmethod
    def _convert_kebab_to_snake(name: str) -> str:
        return name.replace("-", "_")
