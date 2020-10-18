from pathlib import Path

import click


class Inspect(object):
    def __init__(self, path: Path):
        self._path = path

    def process(self):
        processes = self.get_all_process()
        click.secho("Currently this project has {} process(es).".format(
            len(processes)),
                    fg="green")
        for process in processes:
            click.secho("  * {}".format(process), fg="green")

    def get_all_process(self) -> [str]:
        results = []
        process_path = self._path.joinpath("processes")
        if not process_path.is_dir():
            return []
        for process in process_path.iterdir():
            if not process.is_dir() or process.name[0] == ".":
                continue
            results.append(process.name)
        return results
