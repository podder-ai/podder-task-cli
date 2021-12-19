from pathlib import Path
from typing import Optional

import requests


class HttpUtility(object):
    @staticmethod
    def get_content_from_uri(uri: str) -> Optional[str]:
        response = requests.get(uri)
        if response.status_code != requests.codes.ok:
            return

    @staticmethod
    def download_file_from_uri(uri: str, path: Path) -> int:
        if path.is_dir():
            source_path = Path(uri)
            path = path.joinpath(source_path.name)

        size = 0
        with requests.get(uri, stream=True) as request:
            request.raise_for_status()
            with path.open(mode='wb') as handler:
                for chunk in request.iter_content(chunk_size=8192):
                    size += len(chunk)
                    handler.write(chunk)

        return size
