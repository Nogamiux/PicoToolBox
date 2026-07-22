from __future__ import annotations

import os
import shutil
import tempfile
from dataclasses import dataclass
from typing import Callable, Optional

import requests

from . import github_api
from .drives import _candidate_mountpoints

ProgressCB = Optional[Callable[[str], None]]

RP2_INFO_FILE = "INFO_UF2.TXT"
HYBRID_FW_REPO_KEY = "dspico_hybrid_fw"
HYBRID_ASSET_HINT = "hybrid"


@dataclass
class Rp2Device:
    mountpoint: str
    label: str


class FirmwareError(RuntimeError):
    pass


def find_rp2_bootloader() -> Optional[Rp2Device]:
    for mp in _candidate_mountpoints():
        info_path = os.path.join(mp, RP2_INFO_FILE)
        if os.path.isfile(info_path):
            label = os.path.basename(mp.rstrip("/\\")) or mp
            return Rp2Device(mountpoint=mp, label=label)
    return None


def get_latest_hybrid_release() -> github_api.ReleaseInfo:
    return github_api.get_latest_release(HYBRID_FW_REPO_KEY)


def find_hybrid_asset(release: github_api.ReleaseInfo) -> Optional[github_api.ReleaseAsset]:
    for asset in release.assets:
        name = asset.name.lower()
        if name.endswith(".uf2") and HYBRID_ASSET_HINT in name:
            return asset
    return None


def flash_hybrid_firmware(device: Rp2Device, progress: ProgressCB = None) -> github_api.ReleaseInfo:
    if progress:
        progress("Cerco l'ultima release del firmware ibrido...")
    release = get_latest_hybrid_release()

    asset = find_hybrid_asset(release)
    if not asset:
        raise FirmwareError(
            "Non ho trovato l'asset del firmware ibrido (.uf2 con 'hybrid' nel nome) "
            f"nell'ultima release di coderkei/dspico-hybrid-fw ({release.tag_name})."
        )

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = os.path.join(tmp, asset.name)
        if progress:
            progress(f"Scarico {asset.name} ({release.tag_name})...")
        with requests.get(asset.download_url, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(tmp_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1 << 16):
                    if chunk:
                        f.write(chunk)

        dest_path = os.path.join(device.mountpoint, asset.name)
        if progress:
            progress("Copio il firmware sulla DSpico...")
        try:
            shutil.copy2(tmp_path, dest_path)
        except OSError:
            pass

    if progress:
        progress(
            f"Firmware ibrido {release.tag_name} inviato. "
            "La DSpico si disconnetterà da sola: è normale, significa che ha finito."
        )
    return release