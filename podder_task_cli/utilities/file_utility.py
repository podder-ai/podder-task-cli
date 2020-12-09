import shutil
import subprocess
import tempfile
import urllib
import urllib.request
import zipfile
from pathlib import Path


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
