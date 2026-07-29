from __future__ import annotations

from PySide6.QtCore import QThread, Signal

from core import drives as drives_mod
from core import github_api
from core import updater as updater_mod
from core import cheats as cheats_mod
from core import firmware as firmware_mod
from core import emulators as emulators_mod
from core import dsi as dsi_mod
from core import themes as themes_mod
from core import format_sd as format_sd_mod
from core import saves_manager


class DriveScanWorker(QThread):
    finished_ok = Signal(list)
    failed = Signal(str)

    def run(self):
        try:
            found = drives_mod.scan_drives()
            self.finished_ok.emit(found)
        except Exception as exc:
            self.failed.emit(str(exc))


class ReleaseCheckWorker(QThread):
    finished_ok = Signal(dict)
    failed = Signal(str)

    def __init__(self, keys: list[str] | None = None, parent=None):
        super().__init__(parent)
        self.keys = keys

    def run(self):
        try:
            releases = github_api.check_all_updates(self.keys)
            self.finished_ok.emit(releases)
        except Exception as exc:
            self.failed.emit(str(exc))


class InstallWorker(QThread):
    progress = Signal(str)
    finished_ok = Signal(object)
    failed = Signal(str)

    def __init__(self, kind: str, drive, release, parent=None):
        super().__init__(parent)
        self.kind = kind
        self.drive = drive
        self.release = release

    def run(self):
        try:
            if self.kind == "pico_loader":
                result = updater_mod.install_pico_loader(self.drive, self.release, self.progress.emit)
            elif self.kind == "pico_launcher":
                result = updater_mod.install_pico_launcher(self.drive, self.release, self.progress.emit)
            else:
                raise ValueError(f"Tipo componente sconosciuto: {self.kind}")
            self.finished_ok.emit(result)
        except Exception as exc:
            self.failed.emit(str(exc))


class CheatDownloadWorker(QThread):
    progress = Signal(str)
    finished_ok = Signal(str)
    failed = Signal(str)

    def __init__(self, url: str, pico_folder: str, parent=None):
        super().__init__(parent)
        self.url = url
        self.pico_folder = pico_folder

    def run(self):
        try:
            path = cheats_mod.download_cheat_db(self.url, self.pico_folder, self.progress.emit)
            self.finished_ok.emit(path)
        except Exception as exc:
            self.failed.emit(str(exc))


class Rp2ScanWorker(QThread):
    finished_ok = Signal(object)
    failed = Signal(str)

    def run(self):
        try:
            device = firmware_mod.find_rp2_bootloader()
            self.finished_ok.emit(device)
        except Exception as exc:
            self.failed.emit(str(exc))


class FirmwareFlashWorker(QThread):
    progress = Signal(str)
    finished_ok = Signal(object)
    failed = Signal(str)

    def __init__(self, device, parent=None):
        super().__init__(parent)
        self.device = device

    def run(self):
        try:
            release = firmware_mod.flash_hybrid_firmware(self.device, self.progress.emit)
            self.finished_ok.emit(release)
        except Exception as exc:
            self.failed.emit(str(exc))


class EmulatorInstallWorker(QThread):
    progress = Signal(str)
    finished_ok = Signal(str, list)
    failed = Signal(str, str)

    def __init__(self, spec, drive, parent=None):
        super().__init__(parent)
        self.spec = spec
        self.drive = drive

    def run(self):
        try:
            installed = emulators_mod.install_emulator(self.spec, self.drive, self.progress.emit)
            self.finished_ok.emit(self.spec.id, installed)
        except Exception as exc:
            self.failed.emit(self.spec.id, str(exc))


class ThemeSwitcherInstallWorker(QThread):
    progress = Signal(str)
    finished_ok = Signal(object)
    failed = Signal(str)

    def __init__(self, drive, parent=None):
        super().__init__(parent)
        self.drive = drive

    def run(self):
        try:
            release = themes_mod.install_theme_switcher(self.drive, self.progress.emit)
            self.finished_ok.emit(release)
        except Exception as exc:
            self.failed.emit(str(exc))


class PrepareSdWorker(QThread):
    progress = Signal(str)
    finished_ok = Signal(object)
    failed = Signal(str)

    def __init__(self, drive, parent=None):
        super().__init__(parent)
        self.drive = drive

    def run(self):
        try:
            new_mountpoint = format_sd_mod.format_fat32(self.drive.mountpoint, self.progress.emit)
            format_sd_mod.ensure_pico_structure(new_mountpoint)

            self.progress.emit("Cerco le ultime versioni di Pico Loader e Pico Launcher...")
            releases = github_api.check_all_updates(["pico_loader", "pico_launcher"])

            fresh_drives = drives_mod.scan_drives()
            drive = next(
                (d for d in fresh_drives if d.mountpoint == new_mountpoint),
                drives_mod.DriveInfo(mountpoint=new_mountpoint, label=new_mountpoint),
            )

            loader_result = updater_mod.install_pico_loader(
                drive, releases["pico_loader"], self.progress.emit
            )
            launcher_result = updater_mod.install_pico_launcher(
                drive, releases["pico_launcher"], self.progress.emit
            )

            self.finished_ok.emit({
                "drive": drive,
                "loader": loader_result,
                "launcher": launcher_result,
            })
        except Exception as exc:
            self.failed.emit(str(exc))


class DsiPrepWorker(QThread):
    progress = Signal(str)
    finished_ok = Signal(str)
    failed = Signal(str)

    def __init__(self, drive, parent=None):
        super().__init__(parent)
        self.drive = drive

    def run(self):
        try:
            path = dsi_mod.prepare_dsiware(self.drive, self.progress.emit)
            self.finished_ok.emit(path)
        except Exception as exc:
            self.failed.emit(str(exc))

from core import akmenu as akmenu_mod


class AkMenuInstallWorker(QThread):
    progress = Signal(str)
    finished_ok = Signal(object)
    failed = Signal(str)

    def __init__(self, drive, parent=None):
        super().__init__(parent)
        self.drive = drive

    def run(self):
        try:
            result = akmenu_mod.install_akmenu_next(self.drive, self.progress.emit)
            self.finished_ok.emit(result)
        except Exception as exc:
            self.failed.emit(str(exc))


class NdsBootstrapInstallWorker(QThread):
    progress = Signal(str)
    finished_ok = Signal(object)
    failed = Signal(str)

    def __init__(self, drive, parent=None):
        super().__init__(parent)
        self.drive = drive

    def run(self):
        try:
            result = akmenu_mod.install_nds_bootstrap(self.drive, self.progress.emit)
            self.finished_ok.emit(result)
        except Exception as exc:
            self.failed.emit(str(exc))
class TwlMenuInstallWorker(QThread):
    progress = Signal(str)
    finished_ok = Signal(object)
    failed = Signal(str)

    def __init__(self, drive, format_sd=False, set_autoboot=False, parent=None):
        super().__init__(parent)
        self.drive = drive
        self.format_sd = format_sd
        self.set_autoboot = set_autoboot

    def run(self):
        try:
            current_drive = self.drive
            if self.format_sd:
                new_mountpoint = format_sd_mod.format_fat32(current_drive.mountpoint, self.progress.emit)
                format_sd_mod.ensure_pico_structure(new_mountpoint)
                
                fresh_drives = drives_mod.scan_drives()
                current_drive = next(
                    (d for d in fresh_drives if d.mountpoint == new_mountpoint),
                    drives_mod.DriveInfo(mountpoint=new_mountpoint, label=new_mountpoint),
                )
            else:
                self.progress.emit("Preparo l'installazione di TWiLightMenu++...")
                
            result = akmenu_mod.install_twlmenu(current_drive, self.set_autoboot, self.progress.emit)
            self.finished_ok.emit(result)
        except Exception as exc:
            self.failed.emit(str(exc))
class BackupSavesWorker(QThread):
    progress = Signal(str)
    finished_ok = Signal(int)
    failed = Signal(str)

    def __init__(self, drive, zip_path, parent=None):
        super().__init__(parent)
        self.drive = drive
        self.zip_path = zip_path

    def run(self):
        try:
            count = saves_manager.backup_saves(self.drive.mountpoint, self.zip_path, self.progress.emit)
            self.finished_ok.emit(count)
        except Exception as exc:
            self.failed.emit(str(exc))


class RestoreSavesWorker(QThread):
    progress = Signal(str)
    finished_ok = Signal(int, int)
    failed = Signal(str)

    def __init__(self, drive, zip_path, is_twl, parent=None):
        super().__init__(parent)
        self.drive = drive
        self.zip_path = zip_path
        self.is_twl = is_twl

    def run(self):
        try:
            restored, orphaned = saves_manager.restore_saves(self.drive.mountpoint, self.zip_path, self.is_twl, self.progress.emit)
            self.finished_ok.emit(restored, orphaned)
        except Exception as exc:
            self.failed.emit(str(exc))

