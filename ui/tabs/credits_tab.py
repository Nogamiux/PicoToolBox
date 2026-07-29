from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame

from core.i18n import t


class CreditsTab(QWidget):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        self.main = main

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 18, 20, 18)
        root.setSpacing(14)

        title = QLabel("CREDITS & THANKS")
        title.setProperty("class", "sectionTitle")
        root.addWidget(title)

        panel = QFrame()
        panel.setProperty("class", "card")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(16, 14, 16, 14)
        panel_layout.setSpacing(12)

        self.intro = QLabel()
        self.intro.setWordWrap(True)
        self.intro.setProperty("class", "bodyText")
        panel_layout.addWidget(self.intro)

        self.credits_list = QLabel()
        self.credits_list.setWordWrap(True)
        self.credits_list.setProperty("class", "bodyText")
        panel_layout.addWidget(self.credits_list)

        self.outro = QLabel()
        self.outro.setWordWrap(True)
        self.outro.setProperty("class", "bodyText")
        self.outro.setAlignment(Qt.AlignLeft)
        panel_layout.addWidget(self.outro)

        root.addWidget(panel)
        root.addStretch(1)

        self.main.lang_changed.connect(self.retranslate_ui)
        self.retranslate_ui()

    def retranslate_ui(self):
        self.intro.setText(t("credits_intro"))
        self.credits_list.setText(t("credits_html"))
        self.outro.setText(t("credits_outro"))