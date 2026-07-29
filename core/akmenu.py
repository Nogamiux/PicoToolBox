"""
Logica di download e installazione di AkMenuNext sulla SD del DSPico.

AkMenuNext:
  - akmenu-next-pico.zip → estratto nella root della SD
  - Pico_Loader_DSPICO.zip (dal repo pico-loader) → copiato in _pico/

nds-bootstrap (opzionale):
  - nds-bootstrap.zip → estratto nella cartella _nds/ della SD
"""
from __future__ import annotations

import os
import shutil
import tempfile
import zipfile
from dataclasses import dataclass
from typing import Callable, Optional

import requests

from .drives import DriveInfo

ProgressCB = Optional[Callable[[str], None]]

AKMENU_ZIP_URL = (
    "https://github.com/coderkei/akmenu-next/releases/latest/download/akmenu-next-pico.zip"
)
PICO_LOADER_ZIP_URL = (
    "https://github.com/LNH-team/pico-loader/releases/latest/download/Pico_Loader_DSPICO.zip"
)
NDS_BOOTSTRAP_ZIP_URL = (
    "https://github.com/DS-Homebrew/nds-bootstrap/releases/latest/download/nds-bootstrap.zip"
)


@dataclass
class AkMenuInstallResult:
    ok: bool
    message: str
    installed_files: list[str]


def _download(url: str, dest_path: str, progress: ProgressCB = None) -> None:
    filename = os.path.basename(url)
    if progress:
        progress(f"Scarico {filename}...")
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 16):
                if chunk:
                    f.write(chunk)


def _extract_to(zip_path: str, dest_dir: str, progress: ProgressCB = None) -> list[str]:
    """Estrae lo zip in dest_dir e restituisce la lista dei percorsi relativi estratti."""
    os.makedirs(dest_dir, exist_ok=True)
    if progress:
        progress(f"Estraggo in {dest_dir}...")
    extracted = []
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(dest_dir)
        extracted = zf.namelist()
    return extracted


def install_akmenu_next(drive: DriveInfo, progress: ProgressCB = None) -> AkMenuInstallResult:
    """
    Installa AkMenuNext sulla SD:
      1. akmenu-next-pico.zip → root della SD
      2. Pico_Loader_DSPICO.zip → _pico/
    """
    installed: list[str] = []

    with tempfile.TemporaryDirectory() as tmp:
                                          
        akmenu_zip = os.path.join(tmp, "akmenu-next-pico.zip")
        try:
            _download(AKMENU_ZIP_URL, akmenu_zip, progress)
        except Exception as exc:
            return AkMenuInstallResult(False, f"Errore download AkMenuNext: {exc}", [])

        akmenu_extract = os.path.join(tmp, "akmenu")
        try:
            names = _extract_to(akmenu_zip, akmenu_extract, progress)
        except Exception as exc:
            return AkMenuInstallResult(False, f"Errore estrazione AkMenuNext: {exc}", [])

        if progress:
            progress("Copio i file di AkMenuNext nella root della SD...")
        for root, _dirs, files in os.walk(akmenu_extract):
            for fname in files:
                src = os.path.join(root, fname)
                rel = os.path.relpath(src, akmenu_extract)
                dest = os.path.join(drive.mountpoint, rel)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copy2(src, dest)
                installed.append(rel)

                                          
        loader_zip = os.path.join(tmp, "Pico_Loader_DSPICO.zip")
        try:
            _download(PICO_LOADER_ZIP_URL, loader_zip, progress)
        except Exception as exc:
            return AkMenuInstallResult(
                False,
                f"AkMenuNext installato, ma errore download Pico Loader: {exc}",
                installed,
            )

        loader_extract = os.path.join(tmp, "loader")
        try:
            _extract_to(loader_zip, loader_extract, progress)
        except Exception as exc:
            return AkMenuInstallResult(
                False,
                f"AkMenuNext installato, ma errore estrazione Pico Loader: {exc}",
                installed,
            )

        if progress:
            progress("Copio Pico Loader in _pico/...")
        pico_folder = drive.pico_folder
        os.makedirs(pico_folder, exist_ok=True)
        for root, _dirs, files in os.walk(loader_extract):
            for fname in files:
                src = os.path.join(root, fname)
                dest = os.path.join(pico_folder, fname)
                shutil.copy2(src, dest)
                installed.append(f"_pico/{fname}")

    if not installed:
        return AkMenuInstallResult(False, "Nessun file installato.", [])

    return AkMenuInstallResult(
        True,
        "AkMenuNext installato con successo.",
        installed,
    )


def install_nds_bootstrap(drive: DriveInfo, progress: ProgressCB = None) -> AkMenuInstallResult:
    """
    Installa nds-bootstrap nella cartella _nds/ della SD.
    """
    installed: list[str] = []
    nds_folder = os.path.join(drive.mountpoint, "_nds")

    with tempfile.TemporaryDirectory() as tmp:
        nds_zip = os.path.join(tmp, "nds-bootstrap.zip")
        try:
            _download(NDS_BOOTSTRAP_ZIP_URL, nds_zip, progress)
        except Exception as exc:
            return AkMenuInstallResult(False, f"Errore download nds-bootstrap: {exc}", [])

        extract_dir = os.path.join(tmp, "nds")
        try:
            _extract_to(nds_zip, extract_dir, progress)
        except Exception as exc:
            return AkMenuInstallResult(False, f"Errore estrazione nds-bootstrap: {exc}", [])

        if progress:
            progress("Copio nds-bootstrap in _nds/...")
        os.makedirs(nds_folder, exist_ok=True)
        for root, _dirs, files in os.walk(extract_dir):
            for fname in files:
                src = os.path.join(root, fname)
                rel = os.path.relpath(src, extract_dir)
                dest = os.path.join(nds_folder, rel)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copy2(src, dest)
                installed.append(f"_nds/{rel}")

    if not installed:
        return AkMenuInstallResult(False, "Nessun file installato per nds-bootstrap.", [])

    return AkMenuInstallResult(
        True,
        "nds-bootstrap installato con successo in _nds/.",
        installed,
    )
TWLMENU_7Z_URL = "https://github.com/DS-Homebrew/TWiLightMenu/releases/latest/download/TWiLightMenu-Flashcard.7z"

def install_twlmenu(drive: DriveInfo, set_autoboot: bool, progress: ProgressCB = None) -> AkMenuInstallResult:
    try:
        import py7zr
    except ImportError:
        return AkMenuInstallResult(False, "Libreria py7zr mancante! Apri il terminale e lancia: pip install py7zr", [])

    installed = []
    with tempfile.TemporaryDirectory() as tmp:
        dl_path = os.path.join(tmp, "twlmenu.7z")
        
        try:
            _download(TWLMENU_7Z_URL, dl_path, progress)
        except Exception as exc:
            return AkMenuInstallResult(False, f"Errore download TWiLightMenu++: {exc}", [])
            
        extract_dir = os.path.join(tmp, "twlmenu_ext")
        os.makedirs(extract_dir, exist_ok=True)
        
        if progress:
            progress("Estraggo l'archivio 7z (potrebbe richiedere qualche istante)...")
            
        try:
            with py7zr.SevenZipFile(dl_path, mode='r') as z:
                z.extractall(path=extract_dir)
        except Exception as exc:
            return AkMenuInstallResult(False, f"Errore estrazione 7z: {exc}", [])
            
        if progress:
            progress("Copio i file sulla SD...")
            
                                                                      
        def copy_extracted(src_rel, dest_rel):
            src_full = os.path.join(extract_dir, src_rel)
            dest_full = os.path.join(drive.mountpoint, dest_rel)
            
            if os.path.isdir(src_full):
                shutil.copytree(src_full, dest_full, dirs_exist_ok=True)
                installed.append(dest_rel + "/")
            elif os.path.isfile(src_full):
                os.makedirs(os.path.dirname(dest_full), exist_ok=True)
                shutil.copy2(src_full, dest_full)
                installed.append(dest_rel)

        try:
            copy_extracted("_nds", "_nds")
            copy_extracted("roms", "roms")
            copy_extracted("BOOT_ALT.NDS", "BOOT_ALT.NDS")
            
            if set_autoboot:
                if progress:
                    progress("Imposto l'autoboot (kernel primario)...")
                copy_extracted(os.path.join("Autoboot", "DSpico", "_picoboot.nds"), "_picoboot.nds")
        except Exception as exc:
             return AkMenuInstallResult(False, f"Errore copia file: {exc}", installed)

    if not installed:
         return AkMenuInstallResult(False, "Nessun file copiato.", [])
         
    return AkMenuInstallResult(True, "TWiLightMenu++ installato con successo.", installed)
