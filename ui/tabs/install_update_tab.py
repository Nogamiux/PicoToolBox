from __future__ import annotations

import datetime

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QFrame,
)

from core import state as state_mod
from core.i18n import t
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

        self.subtitle = QLabel()
        self.subtitle.setProperty("class", "mutedText")
        root.addWidget(self.subtitle)

                                                                           
        init_panel = QFrame()
        init_panel.setProperty("class", "card")
        init_layout = QVBoxLayout(init_panel)
        init_layout.setContentsMargins(16, 14, 16, 14)

        self.init_title_label = QLabel()
        self.init_title_label.setProperty("class", "cardTitle")
        init_layout.addWidget(self.init_title_label)

        self.init_desc = QLabel()
        self.init_desc.setWordWrap(True)
        self.init_desc.setProperty("class", "bodyText")
        init_layout.addWidget(self.init_desc)

        init_row = QHBoxLayout()
        self.init_sd_btn = QPushButton()
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
        self.check_btn = QPushButton()
        self.check_btn.setProperty("class", "pillButton")
        self.check_btn.clicked.connect(self._check_updates)
        check_row.addWidget(self.check_btn)
        root.addLayout(check_row)

        root.addStretch(1)

        self.main.drive_changed.connect(self.refresh_cards)
        self.main.lang_changed.connect(self.retranslate_ui)
        self.retranslate_ui()

    def retranslate_ui(self):
        self.subtitle.setText(t("install_subtitle"))
        self.init_title_label.setText(t("init_title"))
        self.init_desc.setText(t("install_init_desc"))
        self.init_sd_btn.setText(t("init_title"))
        self.check_btn.setText(t("install_check_btn"))
        self.refresh_cards()

                                                                           

    def _check_updates(self):
        self.main.set_status(t("install_checking"))
        self._release_worker = ReleaseCheckWorker(keys=["pico_loader", "pico_launcher"])
        self._release_worker.finished_ok.connect(self._on_releases_checked)
        self._release_worker.failed.connect(
            lambda msg: self.main.set_status(t("install_check_error", msg=msg))
        )
        self._release_worker.start()

    def _on_releases_checked(self, releases: dict):
        self.latest_releases = releases
        self.main.set_status(t("install_check_done"))
        self.refresh_cards()

                                                                           

    def _installed_version(self, component_key: str):
        drive = self.main.selected_drive
        if not drive or not drive.is_dspico:
            return None
        return state_mod.get_component_version(drive.pico_folder, component_key)

    def _status_tuple(self, component_key: str):
        drive = self.main.selected_drive
        if not drive or not drive.is_dspico:
            return (t("install_no_sd"), "N/D", "badgeMissing", False, t("install_btn_update"))

        installed = self._installed_version(component_key)
        latest = self.latest_releases.get(component_key)

        installed_txt = installed or t("install_unknown")
        if latest is None:
            return (
                t("install_version", ver=installed_txt),
                "?", "badgeUnknown", False, t("install_check_first"),
            )

        if installed == latest.tag_name:
            return (
                t("install_version_ok", ver=installed_txt, date=_fmt_date(latest.published_at)),
                t("install_up_to_date"), "badgeUpToDate", False, t("install_up_to_date"),
            )

        return (
            t("install_version_diff", ver=installed_txt, latest=latest.tag_name),
            t("install_update_available"), "badgeUpdate", True, t("install_btn_update"),
        )

    def _loader_status(self):
        return self._status_tuple("pico_loader")

    def _launcher_status(self):
        return self._status_tuple("pico_launcher")

    def refresh_cards(self):
        self.loader_card.refresh()
        self.launcher_card.refresh()

                                                                           

    def _init_sd(self):
        drive = self.main.selected_drive
        if not drive:
            QMessageBox.warning(self, t("init_title"), t("select_drive"))
            return

        box = QMessageBox(self)
        box.setWindowTitle(t("init_title"))
        box.setText(t("init_text", label=drive.label))
        box.setIcon(QMessageBox.Question)

        btn_format    = box.addButton(t("btn_format"),    QMessageBox.DestructiveRole)
        btn_no_format = box.addButton(t("btn_no_format"), QMessageBox.AcceptRole)
        btn_cancel    = box.addButton(t("btn_cancel"),    QMessageBox.RejectRole)

        box.exec()

        clicked = box.clickedButton()
        if clicked == btn_cancel:
            return

        do_format = (clicked == btn_format)

        self.init_sd_btn.setEnabled(False)
        self.main.drive_combo.setEnabled(False)

        self.main.set_status(
            t("install_fmt_progress", label=drive.label) if do_format
            else t("install_nofmt_progress", label=drive.label)
        )

        self._init_worker = PrepareSdWorker(drive, format_sd=do_format)
        self._init_worker.progress.connect(self.main.set_status)
        self._init_worker.finished_ok.connect(self._on_init_sd_ok)
        self._init_worker.failed.connect(self._on_init_sd_failed)
        self._init_worker.start()

    def _on_init_sd_ok(self, result: dict):
        self.init_sd_btn.setEnabled(True)
        self.main.drive_combo.setEnabled(True)
        loader = result["loader"]
        launcher = result["launcher"]
        self.main.set_status(t("install_sd_ok"))
        QMessageBox.information(
            self, t("init_title"),
            t("install_sd_ok_text", loader=loader.message, launcher=launcher.message),
        )
        self.main.refresh_drives()

    def _on_init_sd_failed(self, msg: str):
        self.init_sd_btn.setEnabled(True)
        self.main.drive_combo.setEnabled(True)
        self.main.set_status(t("install_sd_fail", msg=msg))
        QMessageBox.critical(self, t("init_title"), t("install_sd_fail_msg", msg=msg))

                                                                           

    def _update_component(self, kind: str):
        drive = self.main.selected_drive
        if not drive or not drive.is_dspico:
            QMessageBox.warning(self, "Install and Update", t("install_select_sd"))
            return
        release = self.latest_releases.get(kind)
        if not release:
            QMessageBox.information(self, "Install and Update", t("install_check_first_msg"))
            return

        self.main.set_status(t("install_in_progress", kind=kind))
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
        self.main.set_status(msg)
        QMessageBox.critical(self, "Install and Update", t("install_failed_msg", msg=msg))