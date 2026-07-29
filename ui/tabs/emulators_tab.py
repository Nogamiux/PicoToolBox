from __future__ import annotations

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea, QMessageBox,
)

from core import links
from core.emulators import CATALOG
from core.i18n import t
from ..workers import EmulatorInstallWorker


class EmulatorRow(QFrame):
    def __init__(self, spec, on_install, parent=None):
        super().__init__(parent)
        self.spec = spec
        self._on_install = on_install
        self.setProperty("class", "card")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)

        text_col = QVBoxLayout()
        name_label = QLabel(spec.name)
        name_label.setProperty("class", "cardTitle")
        console_label = QLabel(spec.console)
        console_label.setProperty("class", "cardSubtitle")
        text_col.addWidget(name_label)
        text_col.addWidget(console_label)
        if spec.bios_note:
            bios_label = QLabel(spec.bios_note)
            bios_label.setProperty("class", "mutedText")
            bios_label.setWordWrap(True)
            text_col.addWidget(bios_label)
        self.status_label = QLabel("")
        self.status_label.setProperty("class", "mutedText")
        text_col.addWidget(self.status_label)
        layout.addLayout(text_col, stretch=1)

        self.install_btn = QPushButton(t("btn_emu_install"))
        self.install_btn.setProperty("class", "pillButton")
        self.install_btn.clicked.connect(lambda: self._on_install(self))
        layout.addWidget(self.install_btn)

    def set_status(self, text: str):
        self.status_label.setText(text)

    def set_busy(self, busy: bool):
        self.install_btn.setEnabled(not busy)

    def retranslate_ui(self):
        if self.install_btn.isEnabled():
            self.install_btn.setText(t("btn_emu_install"))


class EmulatorsTab(QWidget):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        self.main = main
        self._workers: dict[str, EmulatorInstallWorker] = {}
        self._rows: dict[str, EmulatorRow] = {}

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 18, 20, 12)
        root.setSpacing(10)

        header_row = QHBoxLayout()
        title = QLabel("SETUP EMULATORS")
        title.setProperty("class", "sectionTitle")
        header_row.addWidget(title)
        header_row.addStretch(1)
        self.guide_btn = QPushButton()
        self.guide_btn.setProperty("class", "pillButtonSecondary")
        self.guide_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(links.EMULATORS_GUIDE_URL)))
        header_row.addWidget(self.guide_btn)
        root.addLayout(header_row)

        self.subtitle = QLabel()
        self.subtitle.setWordWrap(True)
        self.subtitle.setProperty("class", "mutedText")
        root.addWidget(self.subtitle)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(8)

        for spec in CATALOG:
            row = EmulatorRow(spec, self._install)
            self._rows[spec.id] = row
            content_layout.addWidget(row)
        content_layout.addStretch(1)

        scroll.setWidget(content)
        root.addWidget(scroll, stretch=1)

        self.main.lang_changed.connect(self.retranslate_ui)
        self.retranslate_ui()

    def retranslate_ui(self):
        self.guide_btn.setText(t("btn_emu_guide"))
        self.subtitle.setText(t("emu_subtitle"))
        for row in self._rows.values():
            row.retranslate_ui()

    def _install(self, row: EmulatorRow):
        drive = self.main.selected_drive
        if not drive or not drive.is_dspico:
            QMessageBox.warning(self, "Setup Emulators", t("emu_select_sd"))
            return

        row.set_busy(True)
        row.set_status(t("emu_installing"))
        worker = EmulatorInstallWorker(row.spec, drive)
        worker.progress.connect(row.set_status)
        worker.finished_ok.connect(lambda emu_id, installed: self._on_finished(row, installed))
        worker.failed.connect(lambda emu_id, msg: self._on_failed(row, row.spec.name, msg))
        self._workers[row.spec.id] = worker
        worker.start()

    def _on_finished(self, row: EmulatorRow, installed: list[str]):
        row.set_busy(False)
        row.set_status(t("emu_installed", count=len(installed)))

    def _on_failed(self, row: EmulatorRow, name: str, msg: str):
        row.set_busy(False)
        row.set_status(t("emu_failed"))
        QMessageBox.critical(self, "Setup Emulators", t("emu_failed_msg", name=name, msg=msg))