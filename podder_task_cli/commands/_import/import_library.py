import json
import shutil
from collections import OrderedDict
from pathlib import Path
from typing import Optional, Tuple

import click

from ...repositories import Library
from ...services import PackageService
from ...utilities import FileUtility
from .import_base import ImportBase


class ImportLibrary(ImportBase):
    _copy_files = {
        "__init__.py": "__init__.py.tmpl",
        "process.py": "process_for_library.py.tmpl"
    }

    def __init__(self, repository: Library, base_path: Path):
        super().__init__(repository, base_path)
        self._repository = repository
        self._template_directory = Path(__file__).parent.joinpath(
            "..", "..", "templates")
        self._package_service = PackageService(self._base_path)

    def execute(self) -> [str]:
        self._copy_config()
        self._create_process()
        self._update_process_file()
        self._install_library()
        return [self._repository.name]

    def _copy_config(self):
        config = self._repository.get_config()
        if config is None:
            click.secho("This library has no default config.", fg="yellow")
            return

        config_path = self._base_path.joinpath("config", self._repository.name)
        if not config_path.exists():
            config_path.mkdir(parents=True)

        for file_name in config.keys():
            file_path = config_path.joinpath(file_name + ".json")
            file_path.write_text(
                json.dumps(config[file_name], ensure_ascii=False, indent=4))

    def _create_process(self):
        process_path = self._base_path.joinpath("processes",
                                                self._repository.name)
        process_path.mkdir(parents=True)
        for file in self._copy_files.keys():
            template = self._template_directory.joinpath(
                self._copy_files[file])
            target = process_path.joinpath(file)
            shutil.copy(str(template), str(target))

    def _update_process_file(self):
        process_file_path = self._base_path.joinpath("processes",
                                                     self._repository.name,
                                                     "process.py")
        _object = self._repository.get_entry("object")
        object_list = _object.split(".")
        library_module = ".".join(object_list[:-1])
        library_name = object_list[-1]
        build_input, inputs = self._build_input()
        outputs, build_payload = self._build_output()

        data = {
            "library_module": library_module,
            "library_name": library_name,
            "library_method": self._repository.get_entry("method"),
            "build_input": build_input,
            "inputs": inputs,
            "outputs": outputs,
            "build_payload": build_payload,
        }
        FileUtility().update_target_file(process_file_path, data)

    def _build_input(self) -> Tuple[str, str]:
        raw_inputs = self._repository.get_entry("input")
        if raw_inputs is None:
            return "", ""

        build_input = []
        inputs = []

        for name, data_type in self._decide_data_name(raw_inputs).items():
            build_input.append(
                "        input_{} = input_payload.get(object_type=\"{}\")".
                format(name, data_type))
            inputs.append("input_{}.data".format(name))

        return "\n".join(build_input), " ,".join(inputs)

    def _build_output(self) -> Tuple[str, str]:
        raw_outputs = self._repository.get_entry("output")
        outputs = []
        build_payload = []

        for name, data_type in self._decide_data_name(raw_outputs).items():
            outputs.append("output_{}".format(name))
            build_payload.append(
                "        output_payload.add_{}(output_{}, name=\"{}\")".format(
                    data_type, name, name))

        return ", ".join(outputs), "\n".join(build_payload)

    def _install_library(self):
        url = self._repository.url
        if self._repository.schema == "ssh":
            url = "ssh://" + url
        self._package_service.install_package("git+" + url)

    @staticmethod
    def _decide_data_name(data_list: [str]) -> OrderedDict:
        counter = {}
        index = {}
        result = OrderedDict()
        for data_type in data_list:
            if data_type in counter:
                counter[data_type] += 1
            else:
                counter[data_type] = 1
        for data_type in data_list:
            if counter[data_type] == 1:
                result[data_type] = data_type
            else:
                if data_type in index:
                    index[data_type] += 1
                else:
                    index[data_type] = 1
                result["{}_{}".format(data_type, index[data_type])] = data_type

        return result
