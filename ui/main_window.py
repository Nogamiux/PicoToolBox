from __future__ import annotations

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QTabWidget,
)

from core import drives as drives_mod
from .theme import STYLESHEET
from .widgets import StatusChip
from .workers import DriveScanWorker, Rp2ScanWorker
from .tabs.setup_tab import SetupTab
from .tabs.install_update_tab import InstallUpdateTab
from .tabs.emulators_tab import EmulatorsTab
from .tabs.covers_tab import CoversTab
from .tabs.themes_tab import ThemesTab
from .tabs.dsi_tab import DsiTab
from .tabs.credits_tab import CreditsTab

APP_TITLE = "DSPico Toolbox"


class MainWindow(QMainWindow):
    drive_changed = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.resize(760, 640)
        self.setStyleSheet(STYLESHEET)

        self.current_drives: list[drives_mod.DriveInfo] = []
        self.selected_drive: drives_mod.DriveInfo | None = None
        self._hw_scan_worker = None

        self._build_ui()
        self._rescan_drives()

        self._hw_timer = QTimer(self)
        self._hw_timer.setInterval(2500)
        self._hw_timer.timeout.connect(self._scan_hardware)
        self._hw_timer.start()
        self._scan_hardware()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        top_bar = QWidget()
        top_bar.setObjectName("topBar")
        top_layout = QVBoxLayout(top_bar)
        top_layout.setContentsMargins(0, 0, 0, 6)
        title = QLabel(APP_TITLE)
        title.setObjectName("appTitle")
        subtitle = QLabel("Un Tool All-in-one per la tua scheda DSPico")
        subtitle.setObjectName("appSubtitle")
        top_layout.addWidget(title)
        top_layout.addWidget(subtitle)
        root.addWidget(top_bar)

        body = QWidget()
        body.setObjectName("centralArea")
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(20, 14, 20, 14)
        body_layout.setSpacing(12)
        root.addWidget(body, stretch=1)

        status_row = QHBoxLayout()
        self.hw_chip = StatusChip("DSPico Hardware")
        self.storage_chip = StatusChip("DSPico Storage")
        status_row.addWidget(self.hw_chip)
        status_row.addWidget(self.storage_chip)
        status_row.addStretch(1)
        body_layout.addLayout(status_row)
        self.hw_chip.set_pills([("Ricerco...", "badgeUnknown")])
        self.storage_chip.set_pills([("Ricerco...", "badgeUnknown")])

        drive_row = QHBoxLayout()
        drive_row.addWidget(QLabel("Scheda SD:"))
        self.drive_combo = QComboBox()
        self.drive_combo.currentIndexChanged.connect(self._on_drive_selected)
        drive_row.addWidget(self.drive_combo, stretch=1)
        rescan_btn = QPushButton("Rileva di nuovo")
        rescan_btn.setProperty("class", "pillButtonSecondary")
        rescan_btn.clicked.connect(self._rescan_drives)
        drive_row.addWidget(rescan_btn)
        body_layout.addLayout(drive_row)

        self.tabs = QTabWidget()
        self.tabs.addTab(SetupTab(self), "Setup")
        self.tabs.addTab(InstallUpdateTab(self), "Install and Update")
        self.tabs.addTab(EmulatorsTab(self), "Setup Emulators")
        self.tabs.addTab(CoversTab(self), "Covers")
        self.tabs.addTab(ThemesTab(self), "Themes")
        self.tabs.addTab(DsiTab(self), "DSi")
        self.tabs.addTab(CreditsTab(self), "Credits")
        body_layout.addWidget(self.tabs, stretch=1)

        self.status_label = QLabel("Pronto.")
        self.status_label.setObjectName("statusBar")
        body_layout.addWidget(self.status_label)

    def _rescan_drives(self):
        self.set_status("Cerco unità collegate...")
        self._scan_worker = DriveScanWorker()
        self._scan_worker.finished_ok.connect(self._on_drives_found)
        self._scan_worker.failed.connect(lambda msg: self.set_status(f"Errore rilevamento unità: {msg}"))
        self._scan_worker.start()

    def _on_drives_found(self, found: list):
        self.current_drives = found
        self.drive_combo.blockSignals(True)
        self.drive_combo.clear()
        if not found:
            self.drive_combo.addItem("Nessuna unità trovata")
            self.drive_combo.blockSignals(False)
            self.selected_drive = None
            self.set_status("Nessuna unità esterna rilevata. Collega la SD e riprova.")
            self._update_storage_chip()
            self.drive_changed.emit()
            return

        for d in found:
            marker = "[OK] " if d.is_dspico else "[!] "
            self.drive_combo.addItem(f"{marker}{d.label}")
        self.drive_combo.blockSignals(False)

        self.selected_drive = found[0]
        self.set_status(
            f"Trovate {len(found)} unità. "
            + ("Scheda DSPico riconosciuta." if self.selected_drive.is_dspico
               else "Nessuna delle unità sembra una scheda DSPico valida.")
        )
        self._update_storage_chip()
        self.drive_changed.emit()

    def _on_drive_selected(self, index: int):
        if 0 <= index < len(self.current_drives):
            self.selected_drive = self.current_drives[index]
            self._update_storage_chip()
            self.drive_changed.emit()

    def refresh_drives(self):
        self._rescan_drives()

    def _update_storage_chip(self):
        drive = self.selected_drive
        if drive is None:
            self.storage_chip.set_pills([("Not Connected", "badgeMissing")])
        elif drive.is_dspico:
            self.storage_chip.set_pills([
                ("Connected", "badgeUpToDate"),
                ("Ready", "badgeUpToDate"),
            ])
        else:
            self.storage_chip.set_pills([
                ("Connected", "badgeUnknown"),
                ("Not Initialized", "badgeMissing"),
            ])

    def _scan_hardware(self):
        if self._hw_scan_worker is not None and self._hw_scan_worker.isRunning():
            return
        self._hw_scan_worker = Rp2ScanWorker()
        self._hw_scan_worker.finished_ok.connect(self._on_hardware_scanned)
        self._hw_scan_worker.failed.connect(lambda _msg: None)
        self._hw_scan_worker.start()

    def _on_hardware_scanned(self, device):
        if device:
            self.hw_chip.set_pills([("Connected", "badgeUpToDate")])
        else:
            self.hw_chip.set_pills([("Not Connected", "badgeUnknown")])

    def set_status(self, text: str):
        self.status_label.setText(text)