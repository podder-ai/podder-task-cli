from pathlib import Path
from typing import Optional

import requests
from tqdm import tqdm


class HttpUtility(object):
    @staticmethod
    def get_content_from_uri(uri: str) -> Optional[str]:
        response = requests.get(uri)
        if response.status_code != requests.codes.ok:
            return None

        return response.text

    @staticmethod
    def get_download_file_size(url: str) -> Optional[int]:
        response = requests.head(url)
        if not response.ok:
            return None
        try:
            file_size = int(response.headers["content-length"])
        except KeyError:
            return 0

        return file_size

    @staticmethod
    def download_file_from_uri(uri: str, path: Path,
                               progress_bar: Optional[tqdm]) -> Path:
        if path.is_dir():
            source_path = Path(uri)
            path = path.joinpath(source_path.name)

        with requests.get(uri, stream=True) as request:
            request.raise_for_status()
            with path.open(mode='wb') as handler:
                for chunk in request.iter_content(chunk_size=2048):
                    if progress_bar is not None:
                        progress_bar.update(len(chunk))
                    handler.write(chunk)

        return path
