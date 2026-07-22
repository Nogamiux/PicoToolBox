from __future__ import annotations

import os
from typing import Callable, Optional

import requests

ProgressCB = Optional[Callable[[str], None]]

PICO_FILE_DUMP_URL = "https://files.deletecat.com/projects/pico_file_dump/current/pico_file_dump.nds"
PICO_FILE_DUMP_NAME = "pico_file_dump.nds"
DSIWARE_FOLDER = "DSiWare"


def prepare_dsiware(drive, progress: ProgressCB = None) -> str:
    sd_root = drive.mountpoint
    dest_path = os.path.join(sd_root, PICO_FILE_DUMP_NAME)

    if progress:
        progress("Scarico pico_file_dump.nds...")
    with requests.get(PICO_FILE_DUMP_URL, stream=True, timeout=30) as r:
        r.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 16):
                if chunk:
                    f.write(chunk)

    dsiware_dir = os.path.join(sd_root, DSIWARE_FOLDER)
    os.makedirs(dsiware_dir, exist_ok=True)

    if progress:
        progress("Pronto: pico_file_dump.nds è sulla SD e la cartella DSiWare/ è stata creata.")
    return dest_path