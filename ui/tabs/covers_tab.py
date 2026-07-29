from __future__ import annotations

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QDialog, QMessageBox,
)

from core import links
from core.i18n import t
from ..widgets import open_external_link_with_disclaimer


class CoversTab(QWidget):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        self.main = main

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 18, 20, 18)
        root.setSpacing(14)

        title = QLabel("COVERS")
        title.setProperty("class", "sectionTitle")
        root.addWidget(title)

        panel = QFrame()
        panel.setProperty("class", "card")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(16, 14, 16, 14)

        self.text = QLabel()
        self.text.setWordWrap(True)
        self.text.setProperty("class", "bodyText")
        panel_layout.addWidget(self.text)

        self.open_btn = QPushButton()
        self.open_btn.setProperty("class", "pillButton")
        self.open_btn.clicked.connect(self._ask_launcher)
        panel_layout.addWidget(self.open_btn)

        root.addWidget(panel)
        root.addStretch(1)

        self.main.lang_changed.connect(self.retranslate_ui)
        self.retranslate_ui()

    def retranslate_ui(self):
        self.text.setText(t("covers_text"))
        self.open_btn.setText(t("btn_open_picocover"))

    def _ask_launcher(self):
        """Show a popup asking whether to open PicoCover or TwilightBoxart."""
        dialog = QDialog(self)
        dialog.setWindowTitle(t("covers_choose_title"))
        dialog.setModal(True)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        msg = QLabel(t("covers_choose_text"))
        msg.setWordWrap(True)
        layout.addWidget(msg)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        pico_btn = QPushButton(t("covers_btn_picolauncher"))
        pico_btn.setProperty("class", "pillButton")
        pico_btn.clicked.connect(lambda: (dialog.accept(), self._open_picocover()))
        btn_row.addWidget(pico_btn)

        twl_btn = QPushButton(t("covers_btn_twl"))
        twl_btn.setProperty("class", "pillButton")
        twl_btn.clicked.connect(lambda: (dialog.accept(), self._open_twl_boxart()))
        btn_row.addWidget(twl_btn)

        layout.addLayout(btn_row)
        dialog.exec()

    def _open_picocover(self):
        open_external_link_with_disclaimer(
            self, links.PICOCOVER_URL,
            t("covers_disclaimer_title"),
            t("covers_disclaimer_picocover"),
        )

    def _open_twl_boxart(self):
        open_external_link_with_disclaimer(
            self, links.TWL_BOXART_URL,
            t("covers_disclaimer_title"),
            t("covers_disclaimer_twl"),
        )