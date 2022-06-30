import json
from pathlib import Path
from typing import Any, Dict, Optional

import click
from jinja2 import Template

from ...services import PodderService


class Docker(object):
    class DockerType:
        CLI = "cli"
        HTTP = "http"

    def __init__(self,
                 path: Path,
                 output_path: Optional[Path] = None,
                 docker_type: str = DockerType.CLI):
        self._path = path
        self._output_path = output_path or self._path.joinpath("Dockerfile")
        self._docker_type = docker_type
        self._podder_service = PodderService(project_path=path)

    def export(self):
        pass
