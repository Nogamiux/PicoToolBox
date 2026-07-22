from __future__ import annotations

import os
import re
import shutil
import datetime
import tempfile
from dataclasses import dataclass
from typing import Optional, Callable

import requests

ProgressCB = Optional[Callable[[str], None]]

_MIN_STRING_LEN = 4
_STRING_RE = re.compile(rb"[\x20-\x7E]{%d,}" % _MIN_STRING_LEN)


def preview_entries(usrcheat_path: str, limit: int = 500) -> list[str]:
    if not os.path.isfile(usrcheat_path):
        return []

    with open(usrcheat_path, "rb") as f:
        data = f.read()

    found = []
    seen = set()
    for match in _STRING_RE.finditer(data):
        text = match.group().decode("ascii", errors="ignore").strip()
        if re.fullmatch(r"[0-9A-Fa-f ]{8,}", text):
            continue
        if text.lower() in seen:
            continue
        seen.add(text.lower())
        found.append(text)
        if len(found) >= limit:
            break

    return found


def download_cheat_db(url: str, dest_pico_folder: str, progress: ProgressCB = None) -> str:
    os.makedirs(dest_pico_folder, exist_ok=True)
    final_path = os.path.join(dest_pico_folder, "usrcheat.dat")

    if progress:
        progress("Downloading cheat database...")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = os.path.join(tmp, "usrcheat.dat")
        with requests.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(tmp_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1 << 16):
                    if chunk:
                        f.write(chunk)

        if os.path.isfile(final_path):
            stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = os.path.join(dest_pico_folder, ".backup", stamp)
            os.makedirs(backup_dir, exist_ok=True)
            shutil.copy2(final_path, os.path.join(backup_dir, "usrcheat.dat"))

        shutil.copy2(tmp_path, final_path)

    if progress:
        progress("Cheat database updated.")
    return final_path