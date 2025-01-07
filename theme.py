from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import QSize

class Theme:
    BACKGROUND = "#1a1a1a"
    TEXT = "#00ff00"
    ACCENT = "#32CD32"
    INPUT_BG = "#000000"
    BUTTON_HOVER = "#006400"
    ERROR = "#ff0000"
    WARNING = "#ffff00"
    
    FONT_SMALL = 10
    FONT_NORMAL = 12
    FONT_LARGE = 14
    FONT_HEADER = 16
    
    PADDING = 10
    MARGIN = 8
    
    @staticmethod
    def get_stylesheet():
        return """
            QMainWindow {
                background-color: """ + Theme.BACKGROUND + """;
            }
            QWidget {
                background-color: """ + Theme.BACKGROUND + """;
                color: """ + Theme.TEXT + """;
                font-family: 'Courier';
            }
            QLabel {
                color: """ + Theme.TEXT + """;
                font-weight: bold;
                padding: """ + str(Theme.PADDING) + """px;
            }
            QTextEdit, QLineEdit {
                background-color: """ + Theme.INPUT_BG + """;
                border: 2px solid """ + Theme.TEXT + """;
                border-radius: 5px;
                color: """ + Theme.TEXT + """;
                font-family: 'Courier';
                padding: """ + str(Theme.PADDING) + """px;
                min-height: 25px;
            }
            QPushButton {
                background-color: """ + Theme.INPUT_BG + """;
                color: """ + Theme.TEXT + """;
                border: 2px solid """ + Theme.TEXT + """;
                border-radius: 5px;
                padding: """ + str(Theme.PADDING) + """px;
                font-weight: bold;
                min-width: 80px;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: """ + Theme.BUTTON_HOVER + """;
                border-color: """ + Theme.ACCENT + """;
            }
            QPushButton:pressed {
                background-color: """ + Theme.ACCENT + """;
                color: """ + Theme.INPUT_BG + """;
            }
            QCheckBox {
                color: """ + Theme.TEXT + """;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid """ + Theme.TEXT + """;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background-color: """ + Theme.ACCENT + """;
            }
            QComboBox {
                background-color: """ + Theme.INPUT_BG + """;
                border: 2px solid """ + Theme.TEXT + """;
                border-radius: 5px;
                color: """ + Theme.TEXT + """;
                padding: 5px;
                min-height: 30px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid """ + Theme.TEXT + """;
                margin-right: 5px;
            }
            QScrollBar:vertical {
                background: """ + Theme.INPUT_BG + """;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: """ + Theme.TEXT + """;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """

    @staticmethod
    def scale_size(size: int, dpi: float) -> int:
        return int(size * dpi / 96.0)

    @staticmethod
    def get_font(size: int, dpi: float) -> QFont:
        font = QFont('Courier')
        font.setPixelSize(Theme.scale_size(size, dpi))
        return font
