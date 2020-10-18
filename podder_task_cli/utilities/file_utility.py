import shutil
import subprocess


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
