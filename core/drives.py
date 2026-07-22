from __future__ import annotations

import os
import platform
import re
from dataclasses import dataclass, field

import psutil


_SYSTEM_MOUNT_BLOCKLIST = {
    "/", "/boot", "/boot/efi", "/System", "/System/Volumes/Data",
    "C:\\", "C:\\Windows",
}

_DEVICE_BASE_RE = re.compile(r"^/dev/(mmcblk\d+|nvme\d+n\d+)p\d+$|^/dev/([a-zA-Z]+)\d*$")


def _is_removable(partition) -> bool:
    system = platform.system()
    opts = (partition.opts or "").lower()

    if system == "Windows":
        return "removable" in opts

    if system == "Darwin":
        mp = partition.mountpoint
        return mp.startswith("/Volumes/") and mp not in ("/Volumes/Macintosh HD",)

    match = _DEVICE_BASE_RE.match(partition.device or "")
    base = None
    if match:
        base = match.group(1) or match.group(2)
    if base:
        try:
            with open(f"/sys/block/{base}/removable") as f:
                if f.read().strip() == "1":
                    return True
        except OSError:
            pass

    mp = partition.mountpoint or ""
    return mp.startswith(("/media/", "/run/media/"))


@dataclass
class DriveInfo:
    mountpoint: str
    label: str
    is_dspico: bool = False
    has_launcher: bool = False
    has_loader_folder: bool = False
    missing_files: list[str] = field(default_factory=list)
    size_gb: float = 0.0

    @property
    def pico_folder(self) -> str:
        return os.path.join(self.mountpoint, "_pico")

    @property
    def launcher_path(self) -> str:
        return os.path.join(self.mountpoint, "_picoboot.nds")


def _candidate_mountpoints() -> list[str]:
    mounts = []
    try:
        partitions = psutil.disk_partitions(all=False)
    except Exception:
        partitions = []

    for p in partitions:
        mp = p.mountpoint
        if not mp or mp in _SYSTEM_MOUNT_BLOCKLIST:
            continue
        if platform.system() == "Windows" and mp.rstrip("\\") in ("C:",):
            continue
        if mp.startswith(("/proc", "/sys", "/dev", "/run/lock", "/snap")):
            continue
        if not _is_removable(p):
            continue
        mounts.append(mp)

    return mounts


def _label_for(mountpoint: str) -> tuple[str, float]:
    try:
        usage = psutil.disk_usage(mountpoint)
        size_gb = usage.total / (1024 ** 3)
        return f"{mountpoint} ({size_gb:.1f} GB)", size_gb
    except Exception:
        return mountpoint, 0.0


def scan_drives() -> list[DriveInfo]:
    results: list[DriveInfo] = []

    for mp in _candidate_mountpoints():
        label, size_gb = _label_for(mp)
        info = DriveInfo(mountpoint=mp, label=label, size_gb=size_gb)

        launcher_path = os.path.join(mp, "_picoboot.nds")
        pico_folder = os.path.join(mp, "_pico")

        info.has_launcher = os.path.isfile(launcher_path)
        info.has_loader_folder = os.path.isdir(pico_folder)

        if not info.has_loader_folder:
            info.missing_files.append("_pico/")
        if not info.has_launcher:
            info.missing_files.append("_picoboot.nds")

        loader_bins_present = False
        if info.has_loader_folder:
            try:
                names = {n.lower() for n in os.listdir(pico_folder)}
                loader_bins_present = any(
                    n in names for n in ("picoloader7.bin", "picoloader9.bin")
                )
            except OSError:
                pass

        info.is_dspico = info.has_launcher or loader_bins_present

        if info.is_dspico or info.has_loader_folder or info.has_launcher:
            results.append(info)
        else:
            results.append(info)

    results.sort(key=lambda d: (not d.is_dspico, d.mountpoint))
    return results


def installed_component_files(drive: DriveInfo) -> dict:
    files = {}
    candidates = [
        ("_picoboot.nds", drive.launcher_path),
        ("_pico/picoLoader7.bin", os.path.join(drive.pico_folder, "picoLoader7.bin")),
        ("_pico/picoLoader9.bin", os.path.join(drive.pico_folder, "picoLoader9.bin")),
        ("_pico/patchlist.bin", os.path.join(drive.pico_folder, "patchlist.bin")),
        ("_pico/usrcheat.dat", os.path.join(drive.pico_folder, "usrcheat.dat")),
    ]
    for name, path in candidates:
        if os.path.isfile(path):
            stat = os.stat(path)
            files[name] = {
                "path": path,
                "size": stat.st_size,
                "mtime": stat.st_mtime,
            }
    return files