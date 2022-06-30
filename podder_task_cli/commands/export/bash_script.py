import json
from pathlib import Path
from typing import Any, Dict, Optional

import click
from jinja2 import Template

from ...services import PodderService


class BashScript(object):
    def __init__(self, path: Path, output_path: Optional[Path] = None):
        self._path = path
        self._output_path = output_path or self._path.joinpath("Dockerfile")
        self._podder_service = PodderService(project_path=path)

    def export(self):
        pass
