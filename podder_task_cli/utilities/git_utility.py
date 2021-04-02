import subprocess
from pathlib import Path


class GitUtility(object):
    @staticmethod
    def execute_git_command(command: str, repository_directory: Path) -> str:
        result = subprocess.getoutput("git -C {} {}".format(
            repository_directory, command))
        return result

    @staticmethod
    def get_config(name: str, default: str = "") -> str:
        result = subprocess.getoutput("git config --get {}".format(name))
        if result.startswith("error"):
            return default
        return result

    @staticmethod
    def clone_repository(target_repository: str,
                         destination_directory: Path) -> bool:
        result = subprocess.getoutput("git clone {} {}".format(
            target_repository, destination_directory))
        if result.startswith("error"):
            return False
        return True

    def get_revision(self, repository_path: Path) -> str:
        result = self.execute_git_command("rev-parse HEAD", repository_path)
        return result
