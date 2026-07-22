from __future__ import annotations

import datetime

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QFrame,
)

from core import state as state_mod
from ..widgets import ComponentCard
from ..workers import ReleaseCheckWorker, InstallWorker, PrepareSdWorker


def _fmt_date(iso_str: str) -> str:
    if not iso_str:
        return "?"
    try:
        dt = datetime.datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y")
    except ValueError:
        return iso_str


class InstallUpdateTab(QWidget):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        self.main = main
        self.latest_releases: dict = {}

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 18, 20, 18)
        root.setSpacing(14)

        title = QLabel("INSTALL AND UPDATE")
        title.setProperty("class", "sectionTitle")
        root.addWidget(title)

        subtitle = QLabel("Aggiorna Pico Loader e Pico Launcher sulla SD selezionata.")
        subtitle.setProperty("class", "mutedText")
        root.addWidget(subtitle)

        init_panel = QFrame()
        init_panel.setProperty("class", "card")
        init_layout = QVBoxLayout(init_panel)
        init_layout.setContentsMargins(16, 14, 16, 14)

        init_title = QLabel("Inizializza SD")
        init_title.setProperty("class", "cardTitle")
        init_layout.addWidget(init_title)

        init_desc = QLabel(
            "Questa Opzione Prepara la SD per essere utilizzata su DSPico. \n" 
            "ATTENZIONE Questa operazione cancellerà tutti i dati dalla SD!"
        )
        init_desc.setWordWrap(True)
        init_desc.setProperty("class", "bodyText")
        init_layout.addWidget(init_desc)

        init_row = QHBoxLayout()
        self.init_sd_btn = QPushButton("Inizializza SD")
        self.init_sd_btn.setProperty("class", "pillButton")
        self.init_sd_btn.clicked.connect(self._init_sd)
        init_row.addWidget(self.init_sd_btn)
        init_row.addStretch(1)
        init_layout.addLayout(init_row)

        root.addWidget(init_panel)

        self.loader_card = ComponentCard(
            "Pico Loader", self._loader_status, lambda: self._update_component("pico_loader")
        )
        self.launcher_card = ComponentCard(
            "Pico Launcher", self._launcher_status, lambda: self._update_component("pico_launcher")
        )
        root.addWidget(self.loader_card)
        root.addWidget(self.launcher_card)

        check_row = QHBoxLayout()
        check_row.addStretch(1)
        check_btn = QPushButton("Controlla aggiornamenti")
        check_btn.setProperty("class", "pillButton")
        check_btn.clicked.connect(self._check_updates)
        check_row.addWidget(check_btn)
        root.addLayout(check_row)

        root.addStretch(1)

        self.main.drive_changed.connect(self.refresh_cards)

    # ------------------------------------------------------ release check
    def _check_updates(self):
        self.main.set_status("Controllo le ultime versioni su GitHub...")
        self._release_worker = ReleaseCheckWorker(keys=["pico_loader", "pico_launcher"])
        self._release_worker.finished_ok.connect(self._on_releases_checked)
        self._release_worker.failed.connect(
            lambda msg: self.main.set_status(f"Errore controllo aggiornamenti: {msg}")
        )
        self._release_worker.start()

    def _on_releases_checked(self, releases: dict):
        self.latest_releases = releases
        self.main.set_status("Controllo completato.")
        self.refresh_cards()

    # ------------------------------------------------------- card content
    def _installed_version(self, component_key: str):
        drive = self.main.selected_drive
        if not drive or not drive.is_dspico:
            return None
        return state_mod.get_component_version(drive.pico_folder, component_key)

    def _status_tuple(self, component_key: str):
        drive = self.main.selected_drive
        if not drive or not drive.is_dspico:
            return ("Nessuna SD DSPico selezionata", "N/D", "badgeMissing", False, "Aggiorna")

        installed = self._installed_version(component_key)
        latest = self.latest_releases.get(component_key)

        installed_txt = installed or "sconosciuta"
        if latest is None:
            return (f"Versione installata: {installed_txt}", "?", "badgeUnknown", False, "Controlla prima")

        if installed == latest.tag_name:
            return (
                f"Versione installata: {installed_txt} (pubblicata {_fmt_date(latest.published_at)})",
                "Aggiornato", "badgeUpToDate", False, "Aggiornato",
            )

        return (
            f"Installata: {installed_txt} → disponibile: {latest.tag_name}",
            "Aggiornamento", "badgeUpdate", True, "Aggiorna",
        )

    def _loader_status(self):
        return self._status_tuple("pico_loader")

    def _launcher_status(self):
        return self._status_tuple("pico_launcher")

    def refresh_cards(self):
        self.loader_card.refresh()
        self.launcher_card.refresh()

    # --------------------------------------------------------- init sd
    def _init_sd(self):
        drive = self.main.selected_drive
        if not drive:
            QMessageBox.warning(self, "Inizializza SD", "Seleziona prima un'unità dall'elenco in alto.")
            return

        reply = QMessageBox.warning(
            self, "Inizializza SD",
            f"Stai per formattare in FAT32 \"{drive.label}\".\n\n"
            "TUTTI I DATI presenti sull'unità andranno persi in modo IRREVERSIBILE.\n\n"
            "Vuoi continuare?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return

        self.init_sd_btn.setEnabled(False)
        self.main.drive_combo.setEnabled(False)
        self.main.set_status(f"Inizializzo {drive.label}...")

        self._init_worker = PrepareSdWorker(drive)
        self._init_worker.progress.connect(self.main.set_status)
        self._init_worker.finished_ok.connect(self._on_init_sd_ok)
        self._init_worker.failed.connect(self._on_init_sd_failed)
        self._init_worker.start()

    def _on_init_sd_ok(self, result: dict):
        self.init_sd_btn.setEnabled(True)
        self.main.drive_combo.setEnabled(True)
        loader = result["loader"]
        launcher = result["launcher"]
        self.main.set_status("SD inizializzata con successo.")
        QMessageBox.information(
            self, "Inizializza SD",
            "SD formattata e pronta per la DSPico.\n\n"
            f"Pico Loader: {loader.message}\n"
            f"Pico Launcher: {launcher.message}",
        )
        self.main.refresh_drives()

    def _on_init_sd_failed(self, msg: str):
        self.init_sd_btn.setEnabled(True)
        self.main.drive_combo.setEnabled(True)
        self.main.set_status(f"Errore durante l'inizializzazione: {msg}")
        QMessageBox.critical(self, "Inizializza SD", f"Inizializzazione fallita:\n{msg}")

    # ------------------------------------------------------------ actions
    def _update_component(self, kind: str):
        drive = self.main.selected_drive
        if not drive or not drive.is_dspico:
            QMessageBox.warning(self, "Install and Update", "Seleziona prima una SD DSPico valida.")
            return
        release = self.latest_releases.get(kind)
        if not release:
            QMessageBox.information(self, "Install and Update", "Premi prima \"Controlla aggiornamenti\".")
            return

        self.main.set_status(f"Installazione {kind} in corso...")
        self._install_worker = InstallWorker(kind, drive, release)
        self._install_worker.progress.connect(self.main.set_status)
        self._install_worker.finished_ok.connect(self._on_install_finished)
        self._install_worker.failed.connect(self._on_install_failed)
        self._install_worker.start()

    def _on_install_finished(self, result):
        self.main.set_status(result.message)
        self.refresh_cards()
        if not result.ok:
            QMessageBox.warning(self, "Install and Update", result.message)

    def _on_install_failed(self, msg: str):
        self.main.set_status(f"Errore: {msg}")
        QMessageBox.critical(self, "Install and Update", f"Installazione fallita:\n{msg}")
