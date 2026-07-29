from __future__ import annotations

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QTabWidget, QMessageBox,
)

from core import drives as drives_mod
from core import i18n
from core.i18n import t
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
from .tabs.extra_tab import ExtraTab


class MainWindow(QMainWindow):
    drive_changed = Signal()
    lang_changed = Signal()                                  

    def __init__(self):
        super().__init__()
        self.resize(760, 640)
        self.setStyleSheet(STYLESHEET)

        self.current_drives: list[drives_mod.DriveInfo] = []
        self.selected_drive: drives_mod.DriveInfo | None = None
        self._hw_scan_worker = None

        self._build_ui()
        self._retranslate()                                     
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

                                                       
        title_row = QHBoxLayout()
        self.title_label = QLabel()
        self.title_label.setObjectName("appTitle")
        title_row.addWidget(self.title_label)
        title_row.addStretch(1)

                                
        self.lang_btn = QPushButton()
        self.lang_btn.setObjectName("langBtn")
        self.lang_btn.setProperty("class", "pillButtonSecondary")
        self.lang_btn.setFixedWidth(80)
        self.lang_btn.setCursor(Qt.PointingHandCursor)
        self.lang_btn.clicked.connect(self._toggle_language)
        title_row.addWidget(self.lang_btn)

        top_layout.addLayout(title_row)

        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("appSubtitle")
        top_layout.addWidget(self.subtitle_label)

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

        drive_row = QHBoxLayout()
        self.sd_label = QLabel()
        drive_row.addWidget(self.sd_label)
        self.drive_combo = QComboBox()
        self.drive_combo.currentIndexChanged.connect(self._on_drive_selected)
        drive_row.addWidget(self.drive_combo, stretch=1)
        self.rescan_btn = QPushButton()
        self.rescan_btn.setProperty("class", "pillButtonSecondary")
        self.rescan_btn.clicked.connect(self._rescan_drives)
        drive_row.addWidget(self.rescan_btn)
        body_layout.addLayout(drive_row)

        self.tabs = QTabWidget()
        self._tab_setup   = SetupTab(self)
        self._tab_install = InstallUpdateTab(self)
        self._tab_emu     = EmulatorsTab(self)
        self._tab_covers  = CoversTab(self)
        self._tab_themes  = ThemesTab(self)
        self._tab_dsi     = DsiTab(self)
        self._tab_extra   = ExtraTab(self)
        self._tab_credits = CreditsTab(self)

        self.tabs.addTab(self._tab_setup,   "")
        self.tabs.addTab(self._tab_install, "")
        self.tabs.addTab(self._tab_emu,     "")
        self.tabs.addTab(self._tab_covers,  "")
        self.tabs.addTab(self._tab_themes,  "")
        self.tabs.addTab(self._tab_dsi,     "")
        self.tabs.addTab(self._tab_extra,   "")
        self.tabs.addTab(self._tab_credits, "")
        body_layout.addWidget(self.tabs, stretch=1)

        self.status_label = QLabel()
        self.status_label.setObjectName("statusBar")
        body_layout.addWidget(self.status_label)

                                                                          

    def _toggle_language(self):
        new_lang = "en" if i18n.current_lang == "it" else "it"
        i18n.set_lang(new_lang)
        self._retranslate()
        self.lang_changed.emit()

    def _retranslate(self):
        """Aggiorna tutti i testi della finestra principale."""
        self.setWindowTitle(t("app_title"))
        self.title_label.setText(t("app_title"))
        self.subtitle_label.setText(t("app_subtitle"))
        self.status_label.setText(t("status_ready"))
        self.sd_label.setText(t("sd_label"))
        self.rescan_btn.setText(t("rescan_btn"))

                                                             
        if i18n.current_lang == "it":
            self.lang_btn.setText("🇬🇧 English")
        else:
            self.lang_btn.setText("🇮🇹 Italiano")
        self.lang_btn.setToolTip(t("lang_switch_tooltip"))

                       
        tab_keys = [
            "tab_setup", "tab_install", "tab_emulators",
            "tab_covers", "tab_themes", "tab_dsi",
            "tab_extra", "tab_credits",
        ]
        for i, key in enumerate(tab_keys):
            self.tabs.setTabText(i, t(key))

                                                                          
        self.hw_chip.set_pills([(t("hw_searching"), "badgeUnknown")])
        self.storage_chip.set_pills([(t("hw_searching"), "badgeUnknown")])

                                                                          

    def _rescan_drives(self):
        self.set_status(t("status_scanning"))
        self._scan_worker = DriveScanWorker()
        self._scan_worker.finished_ok.connect(self._on_drives_found)
        self._scan_worker.failed.connect(
            lambda msg: self.set_status(t("status_error_drive", msg=msg))
        )
        self._scan_worker.start()

    def _on_drives_found(self, found: list):
        self.current_drives = found
        self.drive_combo.blockSignals(True)
        self.drive_combo.clear()
        if not found:
            self.drive_combo.addItem(t("drive_none"))
            self.drive_combo.blockSignals(False)
            self.selected_drive = None
            self.set_status(t("status_no_drive"))
            self._update_storage_chip()
            self.drive_changed.emit()
            return

        for d in found:
            marker = "[OK] " if d.is_dspico else "[!] "
            self.drive_combo.addItem(f"{marker}{d.label}")
        self.drive_combo.blockSignals(False)

        self.selected_drive = found[0]
        self.set_status(
            t("status_found_drives", count=len(found))
            + (t("status_dspico_ok") if self.selected_drive.is_dspico
               else t("status_dspico_no"))
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

                                                                          

    def closeEvent(self, event: QCloseEvent):
        box = QMessageBox(self)
        box.setWindowTitle(t("bye_title"))
        box.setText(t("bye_text"))
        box.setIcon(QMessageBox.Information)
        box.setStandardButtons(QMessageBox.Ok)
        box.exec()
        event.accept()

                                                                          

    def set_status(self, text: str):
        self.status_label.setText(text)

