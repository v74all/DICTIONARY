from PyQt5.QtGui import QFont


class Theme:
    """Multi-theme palette + stylesheet provider for the DICTIONARY GUI.

    Each entry in THEMES is a palette. get_stylesheet() renders a full Qt
    stylesheet from the selected palette, so adding a new look is just a
    matter of adding a palette dict here.
    """

    FONT_SMALL = 10
    FONT_NORMAL = 12
    FONT_LARGE = 14
    FONT_HEADER = 16

    PADDING = 10
    MARGIN = 8

    DEFAULT = "Matrix"

    THEMES = {
        # The original green-on-black hacker look (default).
        "Matrix": {
            "background": "#1a1a1a",
            "text": "#00ff00",
            "accent": "#32CD32",
            "input_bg": "#000000",
            "button_hover": "#006400",
            "border": "#00ff00",
            "error": "#ff0000",
            "warning": "#ffff00",
        },
        "Dracula": {
            "background": "#282a36",
            "text": "#f8f8f2",
            "accent": "#bd93f9",
            "input_bg": "#1e1f29",
            "button_hover": "#44475a",
            "border": "#6272a4",
            "error": "#ff5555",
            "warning": "#f1fa8c",
        },
        "Cyberpunk": {
            "background": "#0d0221",
            "text": "#00f0ff",
            "accent": "#ff2a6d",
            "input_bg": "#06021a",
            "button_hover": "#241734",
            "border": "#ff2a6d",
            "error": "#ff2a6d",
            "warning": "#f9f871",
        },
        "Amber": {
            "background": "#1a1200",
            "text": "#ffb000",
            "accent": "#ff8800",
            "input_bg": "#0d0900",
            "button_hover": "#3a2a00",
            "border": "#ffb000",
            "error": "#ff4400",
            "warning": "#ffd000",
        },
        "Light": {
            "background": "#f5f5f5",
            "text": "#1a1a1a",
            "accent": "#0066cc",
            "input_bg": "#ffffff",
            "button_hover": "#e0e0e0",
            "border": "#999999",
            "error": "#cc0000",
            "warning": "#b35900",
        },
        "Nord": {
            "background": "#2e3440",
            "text": "#d8dee9",
            "accent": "#88c0d0",
            "input_bg": "#3b4252",
            "button_hover": "#434c5e",
            "border": "#4c566a",
            "error": "#bf616a",
            "warning": "#ebcb8b",
        },
    }

    _current = DEFAULT

    @classmethod
    def names(cls):
        return list(cls.THEMES.keys())

    @classmethod
    def current(cls) -> str:
        return cls._current

    @classmethod
    def set_theme(cls, name: str) -> None:
        if name in cls.THEMES:
            cls._current = name

    @classmethod
    def palette(cls, name: str = None) -> dict:
        return cls.THEMES.get(name or cls._current, cls.THEMES[cls.DEFAULT])

    @classmethod
    def get_stylesheet(cls, name: str = None) -> str:
        p = cls.palette(name)
        pad = cls.PADDING
        return f"""
            QMainWindow {{
                background-color: {p['background']};
            }}
            QWidget {{
                background-color: {p['background']};
                color: {p['text']};
                font-family: 'Courier';
            }}
            QLabel {{
                color: {p['text']};
                font-weight: bold;
                font-size: 12px;
            }}
            QTextEdit, QLineEdit {{
                background-color: {p['input_bg']};
                border: 1px solid {p['border']};
                border-radius: 5px;
                color: {p['text']};
                font-family: 'Courier';
                padding: 5px;
            }}
            QPushButton {{
                background-color: {p['input_bg']};
                color: {p['text']};
                border: 1px solid {p['border']};
                border-radius: 5px;
                padding: {pad}px;
                font-weight: bold;
                min-width: 80px;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background-color: {p['button_hover']};
                border-color: {p['accent']};
            }}
            QPushButton:pressed {{
                background-color: {p['accent']};
                color: {p['input_bg']};
            }}
            QCheckBox {{
                color: {p['text']};
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 1px solid {p['border']};
                border-radius: 3px;
            }}
            QCheckBox::indicator:checked {{
                background-color: {p['accent']};
            }}
            QComboBox {{
                background-color: {p['input_bg']};
                border: 1px solid {p['border']};
                border-radius: 5px;
                color: {p['text']};
                padding: 5px;
                min-height: 24px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {p['input_bg']};
                color: {p['text']};
                selection-background-color: {p['button_hover']};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {p['text']};
                margin-right: 5px;
            }}
            QScrollBar:vertical {{
                background: {p['input_bg']};
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background: {p['text']};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """

    @staticmethod
    def scale_size(size: int, dpi: float) -> int:
        return int(size * dpi / 96.0)

    @staticmethod
    def get_font(size: int, dpi: float) -> QFont:
        font = QFont('Courier')
        font.setPixelSize(Theme.scale_size(size, dpi))
        return font
