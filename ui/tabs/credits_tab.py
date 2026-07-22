from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame

class CreditsTab(QWidget):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        self.main = main

        # Impostazione del layout principale identica alle altre tab
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 18, 20, 18)
        root.setSpacing(14)

        # Titolo della sezione
        title = QLabel("CREDITS & THANKS")
        title.setProperty("class", "sectionTitle")
        root.addWidget(title)

        # Pannello contenitore in stile "card"
        panel = QFrame()
        panel.setProperty("class", "card")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(16, 14, 16, 14)
        panel_layout.setSpacing(12)

        # Testo introduttivo
        intro = QLabel("Questo tool non sarebbe possibile senza il lavoro fantastico di molte persone. Un ringraziamento speciale va a:")
        intro.setWordWrap(True)
        intro.setProperty("class", "bodyText")
        panel_layout.addWidget(intro)

        # Ringraziamenti specifici formattati con stile
        credits_html = """
        <ul style="margin-top: 5px; margin-bottom: 5px; line-height: 1.5;">
            <li><b>Team Sanrax:</b> per le loro preziosissime e dettagliate guide sulla DSPico e su innumerevoli altre flashcarts.</li>
            <li><b>Team LNH:</b> per l'invenzione, lo sviluppo della cartuccia DSPico e di tutti i suoi componenti essenziali.</li>
            <li><b>Sviluppatore di Pico Cover:</b> per l'ottimo e comodissimo strumento dedicato alla gestione delle copertine.</li>
            <li><b>Per il progetto DSPico e le sue guide. Supportate il Team LNH e il Team di Flashcarts.net e Sanrax.</li>
        </ul>
        """
        credits_list = QLabel(credits_html)
        credits_list.setWordWrap(True)
        credits_list.setProperty("class", "bodyText")
        panel_layout.addWidget(credits_list)

        # Conclusione e cuore
        outro = QLabel("E un grazie a tutta la <b>Community Homebrew Nintendo DS</b>, che con la sua passione continua a creare, sperimentare e mantenere in vita ancora oggi questa fantastica console! ❤️")
        outro.setWordWrap(True)
        outro.setProperty("class", "bodyText")
        outro.setAlignment(Qt.AlignLeft)
        panel_layout.addWidget(outro)

        root.addWidget(panel)
        
        # Aggiunge spazio vuoto in fondo per spingere la card verso l'alto
        root.addStretch(1)