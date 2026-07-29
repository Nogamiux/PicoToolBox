from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QMessageBox, QFrame, QTextEdit, QFileDialog, QScrollArea
)

from core.i18n import t
from ..workers import (
    AkMenuInstallWorker, NdsBootstrapInstallWorker,
    TwlMenuInstallWorker, BackupSavesWorker, RestoreSavesWorker
)


class ExtraTab(QWidget):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        self.main = main
        self._akmenu_worker = None
        self._nds_worker = None

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QWidget()
        content.setObjectName("centralArea")

        root = QVBoxLayout(content)
        root.setContentsMargins(20, 18, 20, 18)
        root.setSpacing(14)

        self.subtitle_label = QLabel()
        self.subtitle_label.setProperty("class", "mutedText")
        root.addWidget(self.subtitle_label)

                                                                           
        akmenu_card = QFrame()
        akmenu_card.setProperty("class", "card")
        akmenu_layout = QVBoxLayout(akmenu_card)
        akmenu_layout.setContentsMargins(16, 14, 16, 14)
        akmenu_layout.setSpacing(8)

        akmenu_title = QLabel("AkMenuNext")
        akmenu_title.setProperty("class", "cardTitle")
        akmenu_layout.addWidget(akmenu_title)

        self.akmenu_desc = QLabel()
        self.akmenu_desc.setWordWrap(True)
        self.akmenu_desc.setProperty("class", "bodyText")
        akmenu_layout.addWidget(self.akmenu_desc)

        akmenu_btn_row = QHBoxLayout()
        self.akmenu_btn = QPushButton()
        self.akmenu_btn.setProperty("class", "pillButton")
        self.akmenu_btn.clicked.connect(self._install_akmenu)
        akmenu_btn_row.addWidget(self.akmenu_btn)
        akmenu_btn_row.addStretch(1)
        akmenu_layout.addLayout(akmenu_btn_row)

        root.addWidget(akmenu_card)

                                                                           
        twl_card = QFrame()
        twl_card.setProperty("class", "card")
        twl_layout = QVBoxLayout(twl_card)
        twl_layout.setContentsMargins(16, 14, 16, 14)
        twl_layout.setSpacing(8)

        twl_title = QLabel("TWiLightMenu++")
        twl_title.setProperty("class", "cardTitle")
        twl_layout.addWidget(twl_title)

        self.twl_desc = QLabel()
        self.twl_desc.setWordWrap(True)
        self.twl_desc.setProperty("class", "bodyText")
        twl_layout.addWidget(self.twl_desc)

        twl_btn_row = QHBoxLayout()
        self.twl_btn = QPushButton()
        self.twl_btn.setProperty("class", "pillButton")
        self.twl_btn.clicked.connect(self._install_twlmenu)
        twl_btn_row.addWidget(self.twl_btn)
        twl_btn_row.addStretch(1)
        twl_layout.addLayout(twl_btn_row)

        root.addWidget(twl_card)

                                                                           
        saves_card = QFrame()
        saves_card.setProperty("class", "card")
        saves_layout = QVBoxLayout(saves_card)
        saves_layout.setContentsMargins(16, 14, 16, 14)
        saves_layout.setSpacing(8)

        self.saves_title_label = QLabel()
        self.saves_title_label.setProperty("class", "cardTitle")
        saves_layout.addWidget(self.saves_title_label)

        self.saves_desc = QLabel()
        self.saves_desc.setWordWrap(True)
        self.saves_desc.setProperty("class", "bodyText")
        saves_layout.addWidget(self.saves_desc)

        saves_btn_row = QHBoxLayout()
        self.backup_btn = QPushButton()
        self.backup_btn.setProperty("class", "pillButtonSecondary")
        self.backup_btn.clicked.connect(self._backup_saves)
        saves_btn_row.addWidget(self.backup_btn)

        self.restore_btn = QPushButton()
        self.restore_btn.setProperty("class", "pillButton")
        self.restore_btn.clicked.connect(self._restore_saves)
        saves_btn_row.addWidget(self.restore_btn)

        saves_btn_row.addStretch(1)
        saves_layout.addLayout(saves_btn_row)

        root.addWidget(saves_card)

                                                                           
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setFixedHeight(140)
        self.log_box.setProperty("class", "logBox")
        self.log_box.hide()
        root.addWidget(self.log_box)
        root.addStretch(1)

        scroll.setWidget(content)
        main_layout.addWidget(scroll, stretch=1)

                                          
        self.main.lang_changed.connect(self.retranslate_ui)
        self.retranslate_ui()

    def retranslate_ui(self):
        self.subtitle_label.setText(t("extra_subtitle"))
        self.akmenu_desc.setText(t("ak_desc"))
        self.akmenu_btn.setText(t("ak_install_btn"))
        self.twl_desc.setText(t("twl_desc"))
        self.twl_btn.setText(t("twl_install_btn"))
        self.saves_title_label.setText(t("saves_title"))
        self.saves_desc.setText(t("saves_desc"))
        self.backup_btn.setText(t("backup_btn"))
        self.restore_btn.setText(t("restore_btn"))

                                                                          

    def _install_akmenu(self):
        drive = self.main.selected_drive
        if not drive:
            QMessageBox.warning(self, t("ak_title"), t("select_drive"))
            return

        box = QMessageBox(self)
        box.setWindowTitle(t("ak_title"))
        box.setText(t("ak_text", label=drive.label))
        box.setIcon(QMessageBox.Question)

        btn_format    = box.addButton(t("btn_ak_format"), QMessageBox.DestructiveRole)
        btn_no_format = box.addButton(t("btn_ak_nofmt"),  QMessageBox.AcceptRole)
        btn_cancel    = box.addButton(t("btn_cancel"),    QMessageBox.RejectRole)

        box.exec()

        clicked = box.clickedButton()
        if clicked == btn_cancel:
            return

        do_format = (clicked == btn_format)
        self._set_busy(True)
        self._clear_log()
        self.log_box.show()

        self.main.set_status(
            t("ak_fmt_installing") if do_format else t("ak_installing")
        )

        self._akmenu_worker = AkMenuInstallWorker(drive, format_sd=do_format)
        self._akmenu_worker.progress.connect(self._log)
        self._akmenu_worker.progress.connect(self.main.set_status)
        self._akmenu_worker.finished_ok.connect(self._on_akmenu_done)
        self._akmenu_worker.failed.connect(self._on_akmenu_failed)
        self._akmenu_worker.start()

    def _on_akmenu_done(self, result):
        self._set_busy(False)
        self._log(result.message)
        self.main.set_status(result.message)

        if not result.ok:
            QMessageBox.warning(self, t("ak_title"), result.message)
            return

        reply = QMessageBox.question(
            self, t("nds_title"), t("nds_q"),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self._install_nds_bootstrap()
        else:
            QMessageBox.information(
                self, t("ak_title"),
                f"{t('ak_title')} installed!\n\nFiles: {len(result.installed_files)}"
            )

    def _on_akmenu_failed(self, msg: str):
        self._set_busy(False)
        self._log(f"ERROR: {msg}")
        self.main.set_status(f"Error: {msg}")
        QMessageBox.critical(self, t("ak_title"), msg)

                                                                          

    def _install_nds_bootstrap(self):
        drive = self.main.selected_drive
        if not drive:
            return

        self._set_busy(True)
        self.main.set_status("Installing nds-bootstrap...")

        self._nds_worker = NdsBootstrapInstallWorker(drive)
        self._nds_worker.progress.connect(self._log)
        self._nds_worker.progress.connect(self.main.set_status)
        self._nds_worker.finished_ok.connect(self._on_nds_done)
        self._nds_worker.failed.connect(self._on_nds_failed)
        self._nds_worker.start()

    def _on_nds_done(self, result):
        self._set_busy(False)
        self._log(result.message)
        self.main.set_status(result.message)
        if result.ok:
            QMessageBox.information(self, "Installation complete", t("nds_ok"))
        else:
            QMessageBox.warning(self, t("nds_title"), result.message)

    def _on_nds_failed(self, msg: str):
        self._set_busy(False)
        self._log(f"ERROR nds-bootstrap: {msg}")
        self.main.set_status(f"nds-bootstrap error: {msg}")
        QMessageBox.critical(self, t("nds_title"), msg)

                                                                          

    def _set_busy(self, busy: bool):
        self.akmenu_btn.setEnabled(not busy)
        self.twl_btn.setEnabled(not busy)
        self.backup_btn.setEnabled(not busy)
        self.restore_btn.setEnabled(not busy)
        self.main.drive_combo.setEnabled(not busy)

                                                                          

    def _backup_saves(self):
        drive = self.main.selected_drive
        if not drive:
            QMessageBox.warning(self, t("backup_title"), t("select_drive"))
            return

        zip_path, _ = QFileDialog.getSaveFileName(
            self, t("backup_file_dlg"), "backup_salvataggi_dspico.zip",
            "ZIP Archives (*.zip)"
        )
        if not zip_path:
            return

        self._set_busy(True)
        self._clear_log()
        self.log_box.show()
        self.main.set_status(t("backup_in_progress"))

        self._backup_worker = BackupSavesWorker(drive, zip_path)
        self._backup_worker.progress.connect(self._log)
        self._backup_worker.progress.connect(self.main.set_status)
        self._backup_worker.finished_ok.connect(self._on_backup_done)
        self._backup_worker.failed.connect(self._on_backup_failed)
        self._backup_worker.start()

    def _on_backup_done(self, count):
        self._set_busy(False)
        msg = t("backup_done", count=count)
        self._log(msg)
        self.main.set_status(msg)
        QMessageBox.information(self, t("backup_title"), msg)

    def _on_backup_failed(self, msg):
        self._set_busy(False)
        self._log(f"ERROR: {msg}")
        self.main.set_status(f"Backup error: {msg}")
        QMessageBox.critical(self, t("backup_title"), msg)

    def _restore_saves(self):
        drive = self.main.selected_drive
        if not drive:
            QMessageBox.warning(self, t("restore_title"), t("select_drive"))
            return

        zip_path, _ = QFileDialog.getOpenFileName(
            self, t("restore_title"), "", "ZIP Archives (*.zip)"
        )
        if not zip_path:
            return

        reply = QMessageBox.question(
            self, t("restore_title"), t("restore_q"),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
        )
        is_twl = (reply == QMessageBox.Yes)

        self._set_busy(True)
        self._clear_log()
        self.log_box.show()
        self.main.set_status(t("restore_in_progress"))

        self._restore_worker = RestoreSavesWorker(drive, zip_path, is_twl)
        self._restore_worker.progress.connect(self._log)
        self._restore_worker.progress.connect(self.main.set_status)
        self._restore_worker.finished_ok.connect(self._on_restore_done)
        self._restore_worker.failed.connect(self._on_restore_failed)
        self._restore_worker.start()

    def _on_restore_done(self, restored, orphaned):
        self._set_busy(False)
        msg = t("restore_done", restored=restored, orphaned=orphaned)
        self._log(msg)
        self.main.set_status(t("restore_title") + " OK")
        QMessageBox.information(self, t("restore_title"), msg)

    def _on_restore_failed(self, msg):
        self._set_busy(False)
        self._log(f"ERROR: {msg}")
        self.main.set_status(f"Restore error: {msg}")
        QMessageBox.critical(self, t("restore_title"), msg)

                                                                           

    def _install_twlmenu(self):
        drive = self.main.selected_drive
        if not drive:
            QMessageBox.warning(self, t("twl_title"), t("select_drive"))
            return

        box = QMessageBox(self)
        box.setWindowTitle(t("twl_title"))
        box.setText(t("twl_text", label=drive.label))
        box.setIcon(QMessageBox.Question)

        btn_format    = box.addButton(t("btn_ak_format"), QMessageBox.DestructiveRole)
        btn_no_format = box.addButton(t("btn_ak_nofmt"),  QMessageBox.AcceptRole)
        btn_cancel    = box.addButton(t("btn_cancel"),    QMessageBox.RejectRole)

        box.exec()
        clicked = box.clickedButton()
        if clicked == btn_cancel:
            return

        do_format = (clicked == btn_format)
        set_autoboot = False

        if do_format:
            set_autoboot = True
        else:
            reply = QMessageBox.question(
                self, t("twl_kernel_q"), t("twl_kernel_text"),
                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
            )
            set_autoboot = (reply == QMessageBox.Yes)

        self._set_busy(True)
        self._clear_log()
        self.log_box.show()

        self.main.set_status(
            t("twl_fmt_installing") if do_format else t("twl_installing")
        )

        self._twl_worker = TwlMenuInstallWorker(drive, format_sd=do_format, set_autoboot=set_autoboot)
        self._twl_worker.progress.connect(self._log)
        self._twl_worker.progress.connect(self.main.set_status)
        self._twl_worker.finished_ok.connect(self._on_twl_done)
        self._twl_worker.failed.connect(self._on_twl_failed)
        self._twl_worker.start()

    def _on_twl_done(self, result):
        self._set_busy(False)
        self._log(result.message)
        self.main.set_status(result.message)
        if result.ok:
            QMessageBox.information(self, t("twl_title"), result.message)
        else:
            QMessageBox.warning(self, t("twl_title"), result.message)

    def _on_twl_failed(self, msg: str):
        self._set_busy(False)
        self._log(f"ERROR: {msg}")
        self.main.set_status(f"Error: {msg}")
        QMessageBox.critical(self, t("twl_title"), msg)

    def _log(self, msg: str):
        self.log_box.append(msg)

    def _clear_log(self):
        self.log_box.clear()
