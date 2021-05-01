from pathlib import Path

from rich.console import Console

from ..services import PackageService


class Inspect(object):
    def __init__(self, path: Path):
        self._path = path
        self._package_service = PackageService(self._path)

    def process(self):
        info = self._get_info()
        console = Console()
        console.print("\n------------------------------------", style="green")
        console.print("Podder Task Foundation", style="green")
        version = info["podder_task_foundation"]["version"] or "Not Found"
        console.print("Version:", version)
        console.print("\nProcesses", style="green")
        for process in info["processes"]:
            console.print(process)
        console.print("------------------------------------\n", style="green")

    def _get_info(self):
        return {
            "processes": self._get_all_process(),
            "podder_task_foundation": self._get_podder_task_foundation_info()
        }

    def _get_all_process(self) -> [str]:
        results = []
        process_path = self._path.joinpath("processes")
        if not process_path.is_dir():
            return []
        for process in process_path.iterdir():
            if not process.is_dir(
            ) or process.name[0] == "." or process.name[0] == "_":
                continue
            results.append(process.name)
        return results

    def _get_podder_task_foundation_info(self) -> dict:
        version = self._package_service.get_podder_task_foundation_version()
        return {"version": version}
