from __future__ import annotations

import os
import platform
import re
import subprocess
from typing import Callable, Optional

import psutil

ProgressCB = Optional[Callable[[str], None]]

VOLUME_LABEL = "DSPICO"


class FormatError(RuntimeError):
    pass


def _run(cmd: list[str]) -> None:
    is_windows = platform.system() == "Windows"
    
    result = subprocess.run(cmd, capture_output=True, text=True, shell=is_windows)
    
    if result.returncode != 0:
        raise FormatError(
            f"Comando fallito ({' '.join(cmd)}): "
            f"{(result.stderr or result.stdout).strip() or 'errore sconosciuto'}"
        )

def _device_for_mountpoint(mountpoint: str) -> Optional[str]:
    try:
        for p in psutil.disk_partitions(all=False):
            if p.mountpoint == mountpoint:
                return p.device
    except Exception:
        pass
    return None


def format_fat32(mountpoint: str, progress: ProgressCB = None) -> str:
    system = platform.system()

    if system == "Windows":
        drive_letter = mountpoint.rstrip("\\")
        if not re.match(r"^[A-Za-z]:$", drive_letter):
            raise FormatError(f"Percorso non valido per la formattazione Windows: {mountpoint}")
        if progress:
            progress(f"Formatto {drive_letter} in FAT32 (potrebbe richiedere qualche minuto)...")
        
        _run(["format", drive_letter, "/FS:FAT32", f"/V:{VOLUME_LABEL}", "/Q", "/X", "/Y"])
        
        return f"{drive_letter}\\"

    if system == "Darwin":
        if progress:
            progress(f"Formatto {mountpoint} in FAT32...")
        
        result = subprocess.run(
            ["diskutil", "eraseVolume", "FAT32", VOLUME_LABEL, mountpoint],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            raise FormatError(f"Formattazione macOS fallita: {result.stderr or result.stdout}")
        
        match = re.search(r"Mounted at (.*)", result.stdout)
        if match:
            return match.group(1).strip()
        return f"/Volumes/{VOLUME_LABEL}"

    device = _device_for_mountpoint(mountpoint)
    if not device:
        raise FormatError(f"Non trovo il device corrispondente a {mountpoint}.")

    if progress:
        progress(f"Smonto {device}...")
    
    umount_result = subprocess.run(["umount", mountpoint], capture_output=True, text=True)
    if umount_result.returncode != 0:
        if "not mounted" not in umount_result.stderr.lower():
            raise FormatError(f"Impossibile smontare {mountpoint}. L'unità è in uso?")

    if progress:
        progress(f"Formatto {device} in FAT32...")
    
    try:
        _run(["mkfs.vfat", "-F", "32", "-n", VOLUME_LABEL, device])
    except FormatError as e:
        if "Permission denied" in str(e):
            raise FormatError("Permessi insufficienti per formattare. Su Linux potrebbe essere necessario lanciare il tool con privilegi di root/sudo.")
        raise e

    if progress:
        progress("Rimonto l'unità...")
    result = subprocess.run(["udisksctl", "mount", "-b", device], capture_output=True, text=True)

    match = re.search(r"\bat (\S+)", result.stdout or "")
    if match:
        return match.group(1)
    return mountpoint


def ensure_pico_structure(mountpoint: str) -> str:
    pico_folder = os.path.join(mountpoint, "_pico")
    os.makedirs(pico_folder, exist_ok=True)
    return pico_folder