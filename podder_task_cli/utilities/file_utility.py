import shutil
import subprocess
from pathlib import Path

from jinja2 import Template


class FileUtility(object):
    @staticmethod
    def find_command(name: str) -> bool:
        result = shutil.which(name)
        if result is None:
            return False

        return True

    @staticmethod
    def execute_command(name: str, arguments: list) -> str:
        output = subprocess.getoutput("{} {}".format(name,
                                                     " ".join(arguments)))
        return output

    @staticmethod
    def update_target_file(path: Path, data: dict):
        content = path.read_text()
        template = Template(content)
        data = template.render(data)
        path.write_text(data)
