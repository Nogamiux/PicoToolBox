"""
Logica di download e installazione dei componenti sulla SD del DSpico.

Pico Loader pubblica, per ogni release, uno zip separato per ciascuna
piattaforma supportata (Pico_Loader_DSPICO.zip, Pico_Loader_AK2.zip, ecc).
Lo zip per DSpico contiene i file già pronti per `_pico/` (aplist.bin,
patchlist.bin, picoLoader7.bin, picoLoader9.bin, savelist.bin), senza
sottocartelle.

Pico Launcher pubblica un unico "Pico_Launcher.zip" contenente
`LAUNCHER.nds` (da rinominare `_picoboot.nds` in root SD) e una
sottocartella `_pico/themes/...` da unire dentro `_pico/`.

Prima di sovrascrivere qualunque file esistente, ne viene salvata una
copia di backup in `_pico/.backup/<data>/`.
"""
from __future__ import annotations

import datetime
import os
import shutil
import tempfile
import zipfile
from dataclasses import dataclass
from typing import Callable, Optional

import requests

from . import state as state_mod
from .github_api import ReleaseInfo
from .drives import DriveInfo

ProgressCB = Optional[Callable[[str], None]]

# Nome (case-insensitive, senza estensione) dell'asset specifico per DSpico
# nelle release di Pico Loader, es. "Pico_Loader_DSPICO.zip".
LOADER_PLATFORM_TAG = "dspico"


@dataclass
class InstallResult:
    ok: bool
    message: str
    installed_files: list[str]


def _download(url: str, dest_path: str, progress: ProgressCB = None) -> None:
    if progress:
        progress(f"Scarico {os.path.basename(dest_path)}...")
    with requests.get(url, stream=True, timeout=30) as r:
        r.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 16):
                if chunk:
                    f.write(chunk)


def _backup(existing_path: str, backup_root: str) -> None:
    if not os.path.isfile(existing_path):
        return
    os.makedirs(backup_root, exist_ok=True)
    dest = os.path.join(backup_root, os.path.basename(existing_path))
    try:
        shutil.copy2(existing_path, dest)
    except OSError:
        pass


def _backup_root(drive: DriveInfo) -> str:
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(drive.pico_folder, ".backup", stamp)


def install_pico_loader(drive: DriveInfo, release: ReleaseInfo, progress: ProgressCB = None) -> InstallResult:
    zip_asset = next(
        (a for a in release.assets
         if LOADER_PLATFORM_TAG in a.name.lower() and a.name.lower().endswith(".zip")),
        None,
    )
    if not zip_asset:
        return InstallResult(
            False,
            "Non ho trovato l'asset per DSpico nella release di Pico Loader "
            "(cercavo uno zip con 'dspico' nel nome).",
            [],
        )

    os.makedirs(drive.pico_folder, exist_ok=True)
    backup_root = _backup_root(drive)
    installed = []

    with tempfile.TemporaryDirectory() as tmp:
        zip_path = os.path.join(tmp, zip_asset.name)
        _download(zip_asset.download_url, zip_path, progress)

        extract_dir = os.path.join(tmp, "extracted")
        os.makedirs(extract_dir, exist_ok=True)
        if progress:
            progress("Estraggo l'archivio...")
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(extract_dir)

        # I file di questo zip sono piatti (nessuna sottocartella): vanno
        # tutti dentro _pico/ sulla SD.
        for root, _dirs, files in os.walk(extract_dir):
            for fname in files:
                src = os.path.join(root, fname)
                final_path = os.path.join(drive.pico_folder, fname)
                _backup(final_path, backup_root)
                shutil.copy2(src, final_path)
                installed.append(f"_pico/{fname}")

    if not installed:
        return InstallResult(False, "Lo zip di Pico Loader per DSpico era vuoto.", [])

    state_mod.set_component_version(drive.pico_folder, "pico_loader", release.tag_name)
    if progress:
        progress("Pico Loader aggiornato.")
    return InstallResult(True, f"Pico Loader aggiornato a {release.tag_name}.", installed)


def install_pico_launcher(drive: DriveInfo, release: ReleaseInfo, progress: ProgressCB = None) -> InstallResult:
    zip_asset = next((a for a in release.assets if a.name.lower().endswith(".zip")), None)
    if not zip_asset:
        return InstallResult(False, "Nessuno zip trovato negli asset della release di Pico Launcher.", [])

    backup_root = _backup_root(drive)
    installed = []

    with tempfile.TemporaryDirectory() as tmp:
        zip_path = os.path.join(tmp, zip_asset.name)
        _download(zip_asset.download_url, zip_path, progress)

        extract_dir = os.path.join(tmp, "extracted")
        os.makedirs(extract_dir, exist_ok=True)
        if progress:
            progress("Estraggo l'archivio...")
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(extract_dir)

        # Cerchiamo il launcher: puo' chiamarsi _picoboot.nds o LAUNCHER.nds
        launcher_src = None
        for root, _dirs, files in os.walk(extract_dir):
            for fname in files:
                if fname.lower() in ("_picoboot.nds", "launcher.nds"):
                    launcher_src = os.path.join(root, fname)
                    break
            if launcher_src:
                break

        if launcher_src:
            _backup(drive.launcher_path, backup_root)
            shutil.copy2(launcher_src, drive.launcher_path)
            installed.append("_picoboot.nds")

        # Se lo zip contiene anche una cartella _pico/ (temi, config), la
        # fondiamo dentro _pico/ sulla SD, ricorsivamente (i temi vivono
        # in sottocartelle come _pico/themes/<nome>/*.bin).
        pico_src_root = None
        for root, dirs, _files in os.walk(extract_dir):
            if os.path.basename(root).lower() == "_pico":
                pico_src_root = root
                break

        if pico_src_root:
            for root, _dirs, files in os.walk(pico_src_root):
                for fname in files:
                    src = os.path.join(root, fname)
                    rel = os.path.relpath(src, pico_src_root)
                    dest = os.path.join(drive.pico_folder, rel)
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    _backup(dest, backup_root)
                    shutil.copy2(src, dest)
                    installed.append(f"_pico/{rel}")

    if not installed:
        return InstallResult(False, "Non ho trovato file installabili nello zip del launcher.", [])

    state_mod.set_component_version(drive.pico_folder, "pico_launcher", release.tag_name)
    if progress:
        progress("Pico Launcher aggiornato.")
    return InstallResult(True, f"Pico Launcher aggiornato a {release.tag_name}.", installed)
