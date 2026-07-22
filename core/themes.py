from __future__ import annotations

import os
import tempfile
from typing import Callable, Optional

import requests

from . import github_api

ProgressCB = Optional[Callable[[str], None]]

THEME_SWITCHER_REPO_KEY = "pico_theme_switcher"


class ThemesError(RuntimeError):
    pass


def get_latest_theme_switcher_release() -> github_api.ReleaseInfo:
    return github_api.get_latest_release(THEME_SWITCHER_REPO_KEY)


def install_theme_switcher(drive, progress: ProgressCB = None) -> github_api.ReleaseInfo:
    if progress:
        progress("Cerco l'ultima release di Pico Theme Switcher...")
    release = get_latest_theme_switcher_release()

    asset = next((a for a in release.assets if a.name.lower().endswith(".nds")), None)
    if not asset:
        raise ThemesError(
            f"Non ho trovato un file .nds nell'ultima release di Pico Theme Switcher ({release.tag_name})."
        )

    dest_path = os.path.join(drive.mountpoint, asset.name)
    if progress:
        progress(f"Scarico {asset.name}...")
    with requests.get(asset.download_url, stream=True, timeout=30) as r:
        r.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 16):
                if chunk:
                    f.write(chunk)

    if progress:
        progress(f"Pico Theme Switcher {release.tag_name} copiato nella root della SD.")
    return release