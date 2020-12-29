import subprocess


class GitUtility(object):
    @staticmethod
    def get_config(name: str, default: str = "") -> str:
        result = subprocess.getoutput("git config --get {}".format(name))
        if result.startswith("error"):
            return default
        return result
