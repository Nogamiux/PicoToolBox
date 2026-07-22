import sys

from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from ui.theme import pixel_font_path


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("DSPico Toolbox")

    font_path = pixel_font_path()
    if font_path and QFontDatabase.addApplicationFont(font_path) == -1:
        print(f"Attenzione: impossibile caricare il font pixel da {font_path}")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
