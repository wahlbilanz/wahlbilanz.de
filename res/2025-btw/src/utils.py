import os
from pathlib import Path
import subprocess
from typing import Mapping
import requests
import random, string


request_cookie = os.environ.get("COOKIE")
request_headers: Mapping[str, str] = {
    "User-Agent": "".join(
        random.choice(string.ascii_lowercase) for i in range(random.randint(7, 13))
    ),
    "referer": "https://www.bundestag.de/parlament/plenum/abstimmung/liste",
    "x-requested-with": "XMLHttpRequest",
    "cookie": request_cookie if request_cookie else "",
}


def get_headers() -> Mapping[str, str]:
    return request_headers


def download_file(url: str, target: Path) -> None:
    r = requests.get(url, stream=True, allow_redirects=False, headers=request_headers)
    # print(r.status_code)
    with open(target, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
