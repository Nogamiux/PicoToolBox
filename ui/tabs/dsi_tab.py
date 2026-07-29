from __future__ import annotations

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QMessageBox

from core import links
from core.i18n import t
from ..workers import DsiPrepWorker


class DsiTab(QWidget):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        self.main = main
        self._worker = None

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 18, 20, 18)
        root.setSpacing(14)

        header_row = QHBoxLayout()
        title = QLabel("DSI")
        title.setProperty("class", "sectionTitle")
        header_row.addWidget(title)
        header_row.addStretch(1)
        self.guide_btn = QPushButton()
        self.guide_btn.setProperty("class", "pillButtonSecondary")
        self.guide_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(links.DSIWARE_GUIDE_URL)))
        header_row.addWidget(self.guide_btn)
        root.addLayout(header_row)

        panel = QFrame()
        panel.setProperty("class", "card")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(16, 14, 16, 14)

        self.instructions = QLabel()
        self.instructions.setWordWrap(True)
        self.instructions.setProperty("class", "bodyText")
        panel_layout.addWidget(self.instructions)

        btn_row = QHBoxLayout()
        self.prep_btn = QPushButton()
        self.prep_btn.setProperty("class", "pillButton")
        self.prep_btn.clicked.connect(self._prepare)
        btn_row.addWidget(self.prep_btn)
        btn_row.addStretch(1)
        panel_layout.addLayout(btn_row)

        self.status_label = QLabel("")
        self.status_label.setProperty("class", "mutedText")
        self.status_label.setWordWrap(True)
        panel_layout.addWidget(self.status_label)

        root.addWidget(panel)
        root.addStretch(1)

        self.main.lang_changed.connect(self.retranslate_ui)
        self.retranslate_ui()

    def retranslate_ui(self):
        self.guide_btn.setText(t("btn_dsi_guide_full"))
        self.instructions.setText(t("dsi_instructions"))
        self.prep_btn.setText(t("btn_prepare_dsi"))

    def _prepare(self):
        drive = self.main.selected_drive
        if not drive or not drive.is_dspico:
            QMessageBox.warning(self, "DSi", t("dsi_select_sd"))
            return

        self.prep_btn.setEnabled(False)
        self.status_label.setText(t("dsi_preparing"))
        self._worker = DsiPrepWorker(drive)
        self._worker.progress.connect(self.status_label.setText)
        self._worker.finished_ok.connect(self._on_done)
        self._worker.failed.connect(self._on_failed)
        self._worker.start()

    def _on_done(self, path: str):
        self.prep_btn.setEnabled(True)
        self.status_label.setText(t("dsi_done"))

    def _on_failed(self, msg: str):
        self.prep_btn.setEnabled(True)
        self.status_label.setText(t("dsi_failed"))
        QMessageBox.critical(self, "DSi", msg)