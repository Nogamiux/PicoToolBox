from __future__ import annotations

from PySide6.QtCore import QTimer, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QMessageBox,
)

from core import links
from core.i18n import t
from ..workers import Rp2ScanWorker, FirmwareFlashWorker


class SetupTab(QWidget):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        self.main = main
        self.device = None
        self._scan_worker = None
        self._flash_worker = None

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 18, 20, 18)
        root.setSpacing(14)

        title = QLabel("SETUP")
        title.setProperty("class", "sectionTitle")
        root.addWidget(title)

        info_panel = QFrame()
        info_panel.setProperty("class", "panel")
        info_layout = QVBoxLayout(info_panel)
        info_layout.setContentsMargins(16, 14, 16, 14)
        self.info_label = QLabel()
        self.info_label.setWordWrap(True)
        self.info_label.setProperty("class", "bodyText")
        info_layout.addWidget(self.info_label)

        links_row = QHBoxLayout()
        self.dsi_btn = QPushButton()
        self.dsi_btn.setProperty("class", "pillButtonSecondary")
        self.dsi_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(links.DSI_CFW_GUIDE_URL)))
        links_row.addWidget(self.dsi_btn)
        self.threeds_btn = QPushButton()
        self.threeds_btn.setProperty("class", "pillButtonSecondary")
        self.threeds_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(links.THREEDS_HACKS_GUIDE_URL)))
        links_row.addWidget(self.threeds_btn)
        self.guide_btn = QPushButton()
        self.guide_btn.setProperty("class", "pillButtonSecondary")
        self.guide_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(links.LNH_FIRMWARE_GUIDE_URL)))
        links_row.addWidget(self.guide_btn)
        links_row.addStretch(1)
        info_layout.addLayout(links_row)
        root.addWidget(info_panel)

        detect_panel = QFrame()
        detect_panel.setProperty("class", "card")
        detect_layout = QVBoxLayout(detect_panel)
        detect_layout.setContentsMargins(16, 14, 16, 14)

        self.detect_title_label = QLabel()
        self.detect_title_label.setProperty("class", "cardTitle")
        detect_layout.addWidget(self.detect_title_label)

        self.detect_status = QLabel()
        self.detect_status.setWordWrap(True)
        self.detect_status.setProperty("class", "bodyText")
        detect_layout.addWidget(self.detect_status)

        btn_row = QHBoxLayout()
        self.scan_btn = QPushButton()
        self.scan_btn.setProperty("class", "pillButtonSecondary")
        self.scan_btn.clicked.connect(self._scan)
        btn_row.addWidget(self.scan_btn)

        self.flash_btn = QPushButton()
        self.flash_btn.setProperty("class", "pillButton")
        self.flash_btn.setEnabled(False)
        self.flash_btn.clicked.connect(self._flash)
        btn_row.addWidget(self.flash_btn)
        btn_row.addStretch(1)
        detect_layout.addLayout(btn_row)

        root.addWidget(detect_panel)
        root.addStretch(1)

        self._timer = QTimer(self)
        self._timer.setInterval(2500)
        self._timer.timeout.connect(self._scan_silent)

        self.main.lang_changed.connect(self.retranslate_ui)
        self.retranslate_ui()

    def retranslate_ui(self):
        self.info_label.setText(t("setup_instructions"))
        self.dsi_btn.setText(t("btn_dsi_guide"))
        self.threeds_btn.setText(t("btn_3ds_guide"))
        self.guide_btn.setText(t("btn_fw_guide"))
        self.detect_title_label.setText(t("setup_flash_title"))
        self.scan_btn.setText(t("btn_scan_dspico"))
        self.flash_btn.setText(t("btn_flash_fw"))
                                                                      
        if not self.device:
            self.detect_status.setText(t("setup_detect_default"))

    def showEvent(self, event):
        super().showEvent(event)
        self._timer.start()
        self._scan_silent()

    def hideEvent(self, event):
        super().hideEvent(event)
        self._timer.stop()

    def _scan(self):
        self.detect_status.setText(t("setup_scanning"))
        self._run_scan()

    def _scan_silent(self):
        if self.device is not None:
            return
        self._run_scan()

    def _run_scan(self):
        self._scan_worker = Rp2ScanWorker()
        self._scan_worker.finished_ok.connect(self._on_scan_result)
        self._scan_worker.failed.connect(
            lambda msg: self.detect_status.setText(t("setup_scan_error", msg=msg))
        )
        self._scan_worker.start()

    def _on_scan_result(self, device):
        self.device = device
        if device:
            self.detect_status.setText(t("setup_found", mp=device.mountpoint))
            self.flash_btn.setEnabled(True)
        else:
            self.detect_status.setText(t("setup_detect_default"))
            self.flash_btn.setEnabled(False)

    def _flash(self):
        if not self.device:
            return
        self.flash_btn.setEnabled(False)
        self.scan_btn.setEnabled(False)
        self._flash_worker = FirmwareFlashWorker(self.device)
        self._flash_worker.progress.connect(self.detect_status.setText)
        self._flash_worker.finished_ok.connect(self._on_flash_ok)
        self._flash_worker.failed.connect(self._on_flash_failed)
        self._flash_worker.start()

    def _on_flash_ok(self, release):
        self.detect_status.setText(t("setup_flash_ok", tag=release.tag_name))
        self.device = None
        self.scan_btn.setEnabled(True)
        QMessageBox.information(
            self, t("setup_flash_done_title"),
            t("setup_flash_done_text", tag=release.tag_name),
        )

    def _on_flash_failed(self, msg):
        self.scan_btn.setEnabled(True)
        self.flash_btn.setEnabled(True)
        self.detect_status.setText(t("setup_flash_error", msg=msg))
        QMessageBox.critical(self, t("setup_flash_err_title"), msg)