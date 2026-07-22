from __future__ import annotations

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QDialog, QMessageBox, QWidget,
)


class ComponentCard(QFrame):
    def __init__(self, title: str, subtitle_getter, on_update, parent=None):
        super().__init__(parent)
        self.setProperty("class", "card")
        self._subtitle_getter = subtitle_getter
        self._on_update = on_update

        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)

        text_col = QVBoxLayout()
        self.title_label = QLabel(title)
        self.title_label.setProperty("class", "cardTitle")
        self.subtitle_label = QLabel("")
        self.subtitle_label.setProperty("class", "cardSubtitle")
        self.subtitle_label.setWordWrap(True)
        text_col.addWidget(self.title_label)
        text_col.addWidget(self.subtitle_label)
        layout.addLayout(text_col, stretch=1)

        self.badge = QLabel("")
        self.badge.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.badge)

        self.update_btn = QPushButton("Update")
        self.update_btn.setProperty("class", "pillButton")
        self.update_btn.clicked.connect(lambda: self._on_update())
        layout.addWidget(self.update_btn)

        self.refresh()

    def refresh(self):
        subtitle, badge_text, badge_class, btn_enabled, btn_text = self._subtitle_getter()
        self.subtitle_label.setText(subtitle)
        self.badge.setText(badge_text)
        self.badge.setProperty("class", badge_class)
        self.badge.style().unpolish(self.badge)
        self.badge.style().polish(self.badge)
        self.update_btn.setEnabled(btn_enabled)
        self.update_btn.setText(btn_text)


class StatusChip(QFrame):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setProperty("class", "statusChip")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 8, 14, 8)
        layout.setSpacing(8)

        self.title_label = QLabel(title)
        self.title_label.setProperty("class", "chipTitle")
        layout.addWidget(self.title_label)

        self.pills_container = QWidget()
        self.pills_layout = QHBoxLayout(self.pills_container)
        self.pills_layout.setContentsMargins(0, 0, 0, 0)
        self.pills_layout.setSpacing(6)
        layout.addWidget(self.pills_container)

    def set_pills(self, pills: list[tuple[str, str]]):
        while self.pills_layout.count():
            item = self.pills_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for text, badge_class in pills:
            lbl = QLabel(text)
            lbl.setProperty("class", badge_class)
            self.pills_layout.addWidget(lbl)


class SectionTitle(QLabel):
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setProperty("class", "sectionTitle")


def open_external_link_with_disclaimer(parent, url: str, title: str, message: str) -> None:
    box = QMessageBox(parent)
    box.setWindowTitle(title)
    box.setText(message)
    box.setIcon(QMessageBox.Information)
    box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    box.setDefaultButton(QMessageBox.Ok)
    if box.exec() == QMessageBox.Ok:
        QDesktopServices.openUrl(QUrl(url))