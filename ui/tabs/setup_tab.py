from __future__ import annotations

from PySide6.QtCore import QTimer, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QMessageBox,
)

from core import links
from ..workers import Rp2ScanWorker, FirmwareFlashWorker

INSTRUCTIONS = (
    "Se questa è la prima volta che usi la tua DSPico, devi prima flasharne il firmware.\n\n"
    "Con questo tool distribuiamo solo il firmware IBRIDO mantenuto dai ragazzi di Sanrax "
    "(il firmware WRFUxxed del LNH Team non può essere distribuito da noi).\n\n"
    "Il firmware ibrido funziona su DS e DS Lite senza bisogno di alcuna modifica, mentre su "
    "DSi e 3DS è richiesta una mod software: consulta le guide dedicate qui sotto."
)

DEFAULT_DETECT_TEXT = (
    "Rimuovi la DSPico dalla console (e ogni microSD inserita), collegala al PC via cavo USB, "
    "poi premi \"Cerca DSPico\"."
)


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
        info_label = QLabel(INSTRUCTIONS)
        info_label.setWordWrap(True)
        info_label.setProperty("class", "bodyText")
        info_layout.addWidget(info_label)

        links_row = QHBoxLayout()
        dsi_btn = QPushButton("Guida DSi")
        dsi_btn.setProperty("class", "pillButtonSecondary")
        dsi_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(links.DSI_CFW_GUIDE_URL)))
        links_row.addWidget(dsi_btn)
        threeds_btn = QPushButton("Guida 3DS")
        threeds_btn.setProperty("class", "pillButtonSecondary")
        threeds_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(links.THREEDS_HACKS_GUIDE_URL)))
        links_row.addWidget(threeds_btn)
        guide_btn = QPushButton("Guida completa firmware")
        guide_btn.setProperty("class", "pillButtonSecondary")
        guide_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(links.LNH_FIRMWARE_GUIDE_URL)))
        links_row.addWidget(guide_btn)
        links_row.addStretch(1)
        info_layout.addLayout(links_row)
        root.addWidget(info_panel)

        detect_panel = QFrame()
        detect_panel.setProperty("class", "card")
        detect_layout = QVBoxLayout(detect_panel)
        detect_layout.setContentsMargins(16, 14, 16, 14)

        detect_title = QLabel("Flash del firmware")
        detect_title.setProperty("class", "cardTitle")
        detect_layout.addWidget(detect_title)

        self.detect_status = QLabel(DEFAULT_DETECT_TEXT)
        self.detect_status.setWordWrap(True)
        self.detect_status.setProperty("class", "bodyText")
        detect_layout.addWidget(self.detect_status)

        btn_row = QHBoxLayout()
        self.scan_btn = QPushButton("Cerca DSPico")
        self.scan_btn.setProperty("class", "pillButtonSecondary")
        self.scan_btn.clicked.connect(self._scan)
        btn_row.addWidget(self.scan_btn)

        self.flash_btn = QPushButton("Flasha firmware ibrido")
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

    # ------------------------------------------------------------ ciclo vita
    def showEvent(self, event):
        super().showEvent(event)
        self._timer.start()
        self._scan_silent()

    def hideEvent(self, event):
        super().hideEvent(event)
        self._timer.stop()

    # ------------------------------------------------------------- ricerca
    def _scan(self):
        self.detect_status.setText("Cerco la DSPico in modalità bootloader...")
        self._run_scan()

    def _scan_silent(self):
        if self.device is not None:
            return
        self._run_scan()

    def _run_scan(self):
        self._scan_worker = Rp2ScanWorker()
        self._scan_worker.finished_ok.connect(self._on_scan_result)
        self._scan_worker.failed.connect(lambda msg: self.detect_status.setText(f"Errore ricerca: {msg}"))
        self._scan_worker.start()

    def _on_scan_result(self, device):
        self.device = device
        if device:
            self.detect_status.setText(
                f"DSPico trovata in modalità bootloader su {device.mountpoint} — pronta per il flash."
            )
            self.flash_btn.setEnabled(True)
        else:
            self.detect_status.setText(DEFAULT_DETECT_TEXT)
            self.flash_btn.setEnabled(False)

    # --------------------------------------------------------------- flash
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
        self.detect_status.setText(
            f"Firmware ibrido {release.tag_name} flashato con successo! La DSPico si è disconnessa da sola."
        )
        self.device = None
        self.scan_btn.setEnabled(True)
        QMessageBox.information(
            self, "Flash completato",
            f"Firmware ibrido {release.tag_name} installato con successo sulla DSPico.",
        )

    def _on_flash_failed(self, msg):
        self.scan_btn.setEnabled(True)
        self.flash_btn.setEnabled(True)
        self.detect_status.setText(f"Errore durante il flash: {msg}")
        QMessageBox.critical(self, "Errore flash", msg)
