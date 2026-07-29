from __future__ import annotations

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QMessageBox, QDialog,
)

from core import links
from core.i18n import t
from ..widgets import open_external_link_with_disclaimer
from ..workers import ThemeSwitcherInstallWorker


class ThemesTab(QWidget):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        self.main = main
        self._worker = None

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 18, 20, 18)
        root.setSpacing(14)

        title = QLabel("THEMES")
        title.setProperty("class", "sectionTitle")
        root.addWidget(title)

        archive_panel = QFrame()
        archive_panel.setProperty("class", "card")
        archive_layout = QVBoxLayout(archive_panel)
        archive_layout.setContentsMargins(16, 14, 16, 14)
        self.archive_text = QLabel()
        self.archive_text.setWordWrap(True)
        self.archive_text.setProperty("class", "bodyText")
        archive_layout.addWidget(self.archive_text)
        self.archive_btn = QPushButton()
        self.archive_btn.setProperty("class", "pillButton")
        self.archive_btn.clicked.connect(self._ask_theme_launcher)
        archive_layout.addWidget(self.archive_btn)
        root.addWidget(archive_panel)

        switcher_panel = QFrame()
        switcher_panel.setProperty("class", "card")
        switcher_layout = QVBoxLayout(switcher_panel)
        switcher_layout.setContentsMargins(16, 14, 16, 14)
        self.switcher_text = QLabel()
        self.switcher_text.setWordWrap(True)
        self.switcher_text.setProperty("class", "bodyText")
        switcher_layout.addWidget(self.switcher_text)

        btn_row = QHBoxLayout()
        self.switcher_btn = QPushButton()
        self.switcher_btn.setProperty("class", "pillButton")
        self.switcher_btn.clicked.connect(self._install_switcher)
        btn_row.addWidget(self.switcher_btn)
        btn_row.addStretch(1)
        switcher_layout.addLayout(btn_row)

        self.switcher_status = QLabel("")
        self.switcher_status.setProperty("class", "mutedText")
        self.switcher_status.setWordWrap(True)
        switcher_layout.addWidget(self.switcher_status)

        root.addWidget(switcher_panel)
        root.addStretch(1)

        self.main.lang_changed.connect(self.retranslate_ui)
        self.retranslate_ui()

    def retranslate_ui(self):
        self.archive_text.setText(t("themes_archive_text"))
        self.archive_btn.setText(t("btn_themes_archive"))
        self.switcher_text.setText(t("themes_switcher_text"))
        self.switcher_btn.setText(t("btn_themes_switcher"))

    def _ask_theme_launcher(self):
        """Show a popup asking which launcher's theme archive to open."""
        dialog = QDialog(self)
        dialog.setWindowTitle(t("themes_choose_title"))
        dialog.setModal(True)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        msg = QLabel(t("themes_choose_text"))
        msg.setWordWrap(True)
        layout.addWidget(msg)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        pico_btn = QPushButton(t("themes_btn_picolauncher"))
        pico_btn.setProperty("class", "pillButton")
        pico_btn.clicked.connect(lambda: (dialog.accept(), self._open_pico_themes()))
        btn_row.addWidget(pico_btn)

        twl_btn = QPushButton(t("themes_btn_twl"))
        twl_btn.setProperty("class", "pillButton")
        twl_btn.clicked.connect(lambda: (dialog.accept(), self._open_twl_skins()))
        btn_row.addWidget(twl_btn)

        ak_btn = QPushButton(t("themes_btn_akmenu"))
        ak_btn.setProperty("class", "pillButton")
        ak_btn.clicked.connect(lambda: (dialog.accept(), self._open_ak_themes()))
        btn_row.addWidget(ak_btn)

        layout.addLayout(btn_row)
        dialog.exec()

    def _open_pico_themes(self):
        open_external_link_with_disclaimer(
            self, links.THEMES_ARCHIVE_URL,
            t("themes_disclaimer_title"),
            t("themes_disclaimer_pico"),
        )

    def _open_twl_skins(self):
        open_external_link_with_disclaimer(
            self, links.TWL_SKINS_URL,
            t("themes_disclaimer_title"),
            t("themes_disclaimer_twl"),
        )

    def _open_ak_themes(self):
        open_external_link_with_disclaimer(
            self, links.AKMENU_THEMES_URL,
            t("themes_disclaimer_title"),
            t("themes_disclaimer_ak"),
        )

    def _install_switcher(self):
        drive = self.main.selected_drive
        if not drive or not drive.is_dspico:
            QMessageBox.warning(self, "Themes", t("themes_select_sd"))
            return

        self.switcher_btn.setEnabled(False)
        self.switcher_status.setText(t("themes_installing"))
        self._worker = ThemeSwitcherInstallWorker(drive)
        self._worker.progress.connect(self.switcher_status.setText)
        self._worker.finished_ok.connect(self._on_installed)
        self._worker.failed.connect(self._on_failed)
        self._worker.start()

    def _on_installed(self, release):
        self.switcher_btn.setEnabled(True)
        self.switcher_status.setText(t("themes_installed", tag=release.tag_name))

    def _on_failed(self, msg: str):
        self.switcher_btn.setEnabled(True)
        self.switcher_status.setText(t("themes_failed"))
        QMessageBox.critical(self, "Themes", msg)