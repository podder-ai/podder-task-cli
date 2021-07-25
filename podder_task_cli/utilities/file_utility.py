import shutil
import subprocess
from pathlib import Path
from typing import Optional, Tuple

from jinja2 import Template


class FileUtility(object):
    @staticmethod
    def find_command(name: str) -> bool:
        result = shutil.which(name)
        if result is None:
            return False

        return True

    @staticmethod
    def execute_command(name: str,
                        arguments: Optional[list] = None) -> Tuple[bool, str]:
        command = [name]
        if arguments is not None:
            command.extend(arguments)
        try:
            result = subprocess.check_output(command)
            return True, result.decode("utf-8")
        except subprocess.CalledProcessError as e:
            return False, e.output.decode("utf-8")

    @staticmethod
    def update_target_file(path: Path, data: dict):
        content = path.read_text()
        template = Template(content)
        data = template.render(data)
        path.write_text(data)
