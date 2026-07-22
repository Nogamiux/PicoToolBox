from __future__ import annotations

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame

from core import links
from ..widgets import open_external_link_with_disclaimer

DISCLAIMER_TEXT = (
    "PicoCover è uno strumento sviluppato da altri volenterosi sviluppatori della community, "
    "non affiliato né sviluppato da chi ha creato questo tool.\n\n"
    "Verrà aperto nel tuo browser predefinito. Continuare?"
)


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

        text = QLabel(
            "Pico-Launcher può mostrare le copertine dei giochi in modalità cover flow, o sul "
            "monitor superiore in modalità icone. Per generarle e posizionarle correttamente "
            "sulla SD, usa PicoCover, un tool web di terze parti."
        )
        text.setWordWrap(True)
        text.setProperty("class", "bodyText")
        panel_layout.addWidget(text)

        open_btn = QPushButton("Apri PicoCover")
        open_btn.setProperty("class", "pillButton")
        open_btn.clicked.connect(self._open_picocover)
        panel_layout.addWidget(open_btn)

        root.addWidget(panel)
        root.addStretch(1)

    def _open_picocover(self):
        open_external_link_with_disclaimer(
            self, links.PICOCOVER_URL, "Apertura di uno strumento esterno", DISCLAIMER_TEXT
        )
