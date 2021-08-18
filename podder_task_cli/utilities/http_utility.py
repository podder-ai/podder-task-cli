import subprocess
from pathlib import Path
from typing import Optional

import requests


class HttpUtility(object):
    @staticmethod
    def get_content_from_uri(uri: str) -> Optional[str]:
        response = requests.get(uri)
        if response.status_code != requests.codes.ok:
            return
