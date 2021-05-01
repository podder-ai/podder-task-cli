from pathlib import Path


class ProcessService(object):
    def __init__(self, path: Path):
        self._path = path

    def get_process_list(self) -> [str]:
        process_directory = self._path.joinpath("processes")
        if not process_directory.exists() or not process_directory.is_dir():
            return []
        processes = []
        for path in process_directory.iterdir():
            if not path.is_dir():
                continue
            if path.name.startswith("."):
                continue
            if path.name.startswith("_"):
                continue
            processes.append(path.name)

        return processes
