import os

DSI_NAVY_DARKEST = "#050A14"
DSI_NAVY_DARK = "#0A1220"
DSI_NAVY = "#101B2E"
DSI_NAVY_LIGHT = "#182742"
DSI_NAVY_BORDER = "#22314F"

DS_RED = "#E60012"
DS_RED_DARK = "#B4000E"
DS_RED_LIGHT = "#FF4D57"

DSI_WHITE = "#F2F5FA"
DSI_TEXT_MUTED = "#8A97AD"
DSI_GREEN = "#3DBE6C"
DSI_ORANGE = "#F2A93B"
DSI_RED = DS_RED

PIXEL_FONT_FAMILY = "Press Start 2P"
UI_FONT_FAMILY = "'Consolas', 'Courier New', monospace"


def pixel_font_path() -> str:
    ui_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(ui_dir)
    return os.path.join(project_root, "assets", "fonts", "PressStart2P-Regular.ttf")


STYLESHEET = f"""
* {{
    font-family: {UI_FONT_FAMILY};
}}

QMainWindow {{
    background: {DSI_NAVY_DARKEST};
}}

QWidget#topBar {{
    background: {DSI_NAVY_DARKEST};
    border-bottom: 4px solid {DS_RED};
}}

QLabel#appTitle {{
    color: {DSI_WHITE};
    font-family: "{PIXEL_FONT_FAMILY}";
    font-size: 15px;
    padding: 12px 16px 4px 16px;
}}

QLabel#appSubtitle {{
    color: {DSI_TEXT_MUTED};
    font-size: 12px;
    padding: 0 16px 10px 16px;
}}

QWidget {{
    color: {DSI_WHITE};
}}

QWidget#centralArea {{
    background: {DSI_NAVY_DARKEST};
}}

QTabWidget::pane {{
    border: 3px solid {DSI_NAVY_BORDER};
    background: {DSI_NAVY_DARK};
    top: -1px;
}}

QTabBar {{
    qproperty-drawBase: 0;
}}

QTabBar::tab {{
    background: {DSI_NAVY};
    color: {DSI_TEXT_MUTED};
    border: 3px solid {DSI_NAVY_BORDER};
    border-bottom: none;
    padding: 9px 12px;
    margin-right: 3px;
    font-family: "{PIXEL_FONT_FAMILY}";
    font-size: 8px;
}}

QTabBar::tab:selected {{
    background: {DS_RED};
    color: {DSI_WHITE};
    border-color: {DS_RED_DARK};
}}

QTabBar::tab:hover:!selected {{
    color: {DSI_WHITE};
    background: {DSI_NAVY_LIGHT};
}}

QFrame.card {{
    background: {DSI_NAVY};
    border: 3px solid {DSI_NAVY_BORDER};
    border-radius: 0;
}}

QFrame.panel {{
    background: {DSI_NAVY_DARK};
    border: 3px solid {DSI_NAVY_BORDER};
    border-radius: 0;
}}

QLabel.cardTitle {{
    color: {DSI_WHITE};
    font-size: 14px;
    font-weight: 700;
}}

QLabel.cardSubtitle {{
    color: {DSI_TEXT_MUTED};
    font-size: 12px;
}}

QLabel.sectionTitle {{
    color: {DSI_WHITE};
    font-family: "{PIXEL_FONT_FAMILY}";
    font-size: 11px;
    padding: 4px 0 10px 0;
}}

QLabel.bodyText {{
    color: {DSI_WHITE};
    font-size: 12px;
}}

QLabel.mutedText {{
    color: {DSI_TEXT_MUTED};
    font-size: 11px;
}}

QLabel.badgeUpToDate {{
    background: {DSI_GREEN};
    color: #052B14;
    border: 2px solid #052B14;
    border-radius: 0;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 700;
}}

QLabel.badgeUpdate {{
    background: {DSI_ORANGE};
    color: #3A2400;
    border: 2px solid #3A2400;
    border-radius: 0;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 700;
}}

QLabel.badgeUnknown {{
    background: {DSI_NAVY_BORDER};
    color: {DSI_TEXT_MUTED};
    border: 2px solid {DSI_NAVY_DARK};
    border-radius: 0;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 700;
}}

QLabel.badgeMissing {{
    background: {DS_RED};
    color: {DSI_WHITE};
    border: 2px solid {DS_RED_DARK};
    border-radius: 0;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 700;
}}

QPushButton.pillButton {{
    background: {DS_RED};
    color: {DSI_WHITE};
    border-radius: 0;
    border-top: 2px solid {DS_RED_LIGHT};
    border-left: 2px solid {DS_RED_LIGHT};
    border-bottom: 2px solid {DS_RED_DARK};
    border-right: 2px solid {DS_RED_DARK};
    padding: 8px 18px;
    font-size: 12px;
    font-weight: 700;
}}
QPushButton.pillButton:hover {{
    background: {DS_RED_LIGHT};
}}
QPushButton.pillButton:pressed {{
    background: {DS_RED_DARK};
    border-top: 2px solid {DS_RED_DARK};
    border-left: 2px solid {DS_RED_DARK};
    border-bottom: 2px solid {DS_RED_LIGHT};
    border-right: 2px solid {DS_RED_LIGHT};
}}
QPushButton.pillButton:disabled {{
    background: {DSI_NAVY_BORDER};
    color: {DSI_TEXT_MUTED};
    border-color: {DSI_NAVY_DARK};
}}

QPushButton.pillButtonSecondary {{
    background: {DSI_NAVY_LIGHT};
    color: {DSI_WHITE};
    border-radius: 0;
    border-top: 2px solid {DSI_NAVY_BORDER};
    border-left: 2px solid {DSI_NAVY_BORDER};
    border-bottom: 2px solid {DSI_NAVY_DARKEST};
    border-right: 2px solid {DSI_NAVY_DARKEST};
    padding: 7px 16px;
    font-size: 12px;
    font-weight: 600;
}}
QPushButton.pillButtonSecondary:hover {{
    background: {DSI_NAVY_BORDER};
}}
QPushButton.pillButtonSecondary:pressed {{
    border-top: 2px solid {DSI_NAVY_DARKEST};
    border-left: 2px solid {DSI_NAVY_DARKEST};
    border-bottom: 2px solid {DSI_NAVY_BORDER};
    border-right: 2px solid {DSI_NAVY_BORDER};
}}

QCheckBox {{
    font-size: 12px;
    spacing: 8px;
}}
QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border: 2px solid {DSI_NAVY_BORDER};
    background: {DSI_NAVY_LIGHT};
    border-radius: 0;
}}
QCheckBox::indicator:checked {{
    background: {DS_RED};
    border: 2px solid {DS_RED_DARK};
}}

QComboBox {{
    background: {DSI_NAVY_LIGHT};
    color: {DSI_WHITE};
    border: 2px solid {DSI_NAVY_BORDER};
    border-radius: 0;
    padding: 6px 10px;
    min-width: 260px;
}}
QComboBox QAbstractItemView {{
    background: {DSI_NAVY_LIGHT};
    color: {DSI_WHITE};
    selection-background-color: {DS_RED_DARK};
    border: 1px solid {DSI_NAVY_BORDER};
}}

QLineEdit {{
    background: {DSI_NAVY_LIGHT};
    color: {DSI_WHITE};
    border: 2px solid {DSI_NAVY_BORDER};
    border-radius: 0;
    padding: 6px 10px;
}}
QLineEdit:focus {{
    border: 2px solid {DS_RED};
}}

QListWidget {{
    background: {DSI_NAVY_LIGHT};
    color: {DSI_WHITE};
    border: 2px solid {DSI_NAVY_BORDER};
    border-radius: 0;
    padding: 6px;
}}
QListWidget::item:selected {{
    background: {DS_RED_DARK};
    color: {DSI_WHITE};
}}

QScrollArea {{
    border: none;
    background: transparent;
}}

QLabel#statusBar {{
    color: {DSI_WHITE};
    background: {DSI_NAVY_DARK};
    border: 2px solid {DSI_NAVY_BORDER};
    border-radius: 0;
    padding: 6px 12px;
    font-size: 12px;
}}

QScrollBar:vertical {{
    background: {DSI_NAVY_DARK};
    width: 12px;
    border-radius: 0;
}}
QScrollBar::handle:vertical {{
    background: {DSI_NAVY_BORDER};
    border-radius: 0;
    min-height: 24px;
}}
QScrollBar::handle:vertical:hover {{
    background: {DS_RED_DARK};
}}
QDialog, QMessageBox {{
    background: {DSI_NAVY_DARKEST};
}}

QMessageBox QLabel {{
    color: {DSI_WHITE};
    font-size: 12px;
}}

QMessageBox QPushButton {{
    background: {DSI_NAVY_LIGHT};
    color: {DSI_WHITE};
    border-radius: 0;
    border-top: 2px solid {DSI_NAVY_BORDER};
    border-left: 2px solid {DSI_NAVY_BORDER};
    border-bottom: 2px solid {DSI_NAVY_DARKEST};
    border-right: 2px solid {DSI_NAVY_DARKEST};
    padding: 6px 14px;
    font-weight: 600;
}}

QMessageBox QPushButton:hover {{
    background: {DSI_NAVY_BORDER};
}}

QMessageBox QPushButton:pressed {{
    border-top: 2px solid {DSI_NAVY_DARKEST};
    border-left: 2px solid {DSI_NAVY_DARKEST};
    border-bottom: 2px solid {DSI_NAVY_BORDER};
    border-right: 2px solid {DSI_NAVY_BORDER};
}}
"""