from __future__ import annotations

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QMessageBox

from core import links
from ..workers import DsiPrepWorker

INSTRUCTIONS = (
    "La DSPico è una cartuccia in \"modalità DSi\", quindi può far girare DSiWare e ROM cifrate "
    "su console DSi/3DS — ma servono BIOS e file NAND estratti dalla console stessa.\n\n"
    "Questo tool prepara la SD scaricando pico_file_dump.nds e creando la cartella DSiWare/. "
    "Il dump vero e proprio va fatto sulla console: inserisci la SD nella DSPico, avvia la "
    "console, lancia pico_file_dump.nds dal menu e attendi che finisca.\n\n"
    "Funziona solo su console DSi o 3DS (modificati): la DS/DS Lite originale non ha l'hardware "
    "necessario per eseguire titoli in modalità DSi."
)


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
        guide_btn = QPushButton("Guida completa")
        guide_btn.setProperty("class", "pillButtonSecondary")
        guide_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(links.DSIWARE_GUIDE_URL)))
        header_row.addWidget(guide_btn)
        root.addLayout(header_row)

        panel = QFrame()
        panel.setProperty("class", "card")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(16, 14, 16, 14)

        text = QLabel(INSTRUCTIONS)
        text.setWordWrap(True)
        text.setProperty("class", "bodyText")
        panel_layout.addWidget(text)

        btn_row = QHBoxLayout()
        self.prep_btn = QPushButton("Prepara SD per DSiWare")
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

    def _prepare(self):
        drive = self.main.selected_drive
        if not drive or not drive.is_dspico:
            QMessageBox.warning(self, "DSi", "Seleziona prima una SD DSPico valida.")
            return

        self.prep_btn.setEnabled(False)
        self.status_label.setText("Preparazione in corso...")
        self._worker = DsiPrepWorker(drive)
        self._worker.progress.connect(self.status_label.setText)
        self._worker.finished_ok.connect(self._on_done)
        self._worker.failed.connect(self._on_failed)
        self._worker.start()

    def _on_done(self, path: str):
        self.prep_btn.setEnabled(True)
        self.status_label.setText(
            "Pronto! Inserisci la SD nella DSPico, avvia la console e lancia pico_file_dump.nds "
            "dal menu per completare il dump di BIOS/NAND."
        )

    def _on_failed(self, msg: str):
        self.prep_btn.setEnabled(True)
        self.status_label.setText("Preparazione fallita.")
        QMessageBox.critical(self, "DSi", f"Preparazione fallita:\n{msg}")
