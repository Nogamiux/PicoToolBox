from __future__ import annotations

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QMessageBox

from core import links
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
        archive_text = QLabel(
            "Vuoi personalizzare l'interfaccia della tua DSPico? Scarica un tema pronto "
            "dall'archivio temi ufficiale e copialo in _pico/themes/ sulla tua SD."
        )
        archive_text.setWordWrap(True)
        archive_text.setProperty("class", "bodyText")
        archive_layout.addWidget(archive_text)
        archive_btn = QPushButton("Themes Archive")
        archive_btn.setProperty("class", "pillButton")
        archive_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(links.THEMES_ARCHIVE_URL)))
        archive_layout.addWidget(archive_btn)
        root.addWidget(archive_panel)

        switcher_panel = QFrame()
        switcher_panel.setProperty("class", "card")
        switcher_layout = QVBoxLayout(switcher_panel)
        switcher_layout.setContentsMargins(16, 14, 16, 14)
        switcher_text = QLabel(
            "Pico Theme Switcher è un semplice homebrew che ti permette di cambiare tema "
            "direttamente dalla console, scegliendo tra quelli presenti in _pico/themes/."
        )
        switcher_text.setWordWrap(True)
        switcher_text.setProperty("class", "bodyText")
        switcher_layout.addWidget(switcher_text)

        btn_row = QHBoxLayout()
        self.switcher_btn = QPushButton("Installa Pico Theme Switcher")
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

    def _install_switcher(self):
        drive = self.main.selected_drive
        if not drive or not drive.is_dspico:
            QMessageBox.warning(self, "Themes", "Seleziona prima una SD DSPico valida.")
            return

        self.switcher_btn.setEnabled(False)
        self.switcher_status.setText("Installazione in corso...")
        self._worker = ThemeSwitcherInstallWorker(drive)
        self._worker.progress.connect(self.switcher_status.setText)
        self._worker.finished_ok.connect(self._on_installed)
        self._worker.failed.connect(self._on_failed)
        self._worker.start()

    def _on_installed(self, release):
        self.switcher_btn.setEnabled(True)
        self.switcher_status.setText(f"Pico Theme Switcher {release.tag_name} installato sulla SD.")

    def _on_failed(self, msg: str):
        self.switcher_btn.setEnabled(True)
        self.switcher_status.setText("Installazione fallita.")
        QMessageBox.critical(self, "Themes", f"Installazione fallita:\n{msg}")
