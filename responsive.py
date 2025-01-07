from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSize

class ResponsiveUI:
    @staticmethod
    def get_screen_dpi(widget: QWidget) -> float:
        return widget.logicalDpiX() / 96.0

    @staticmethod
    def calculate_window_size(widget: QWidget) -> QSize:
        screen = widget.screen()
        screen_size = screen.size()
        
        if screen_size.width() > 1920:
            width = int(screen_size.width() * 0.6)
            height = int(screen_size.height() * 0.7)
        else:
            width = int(screen_size.width() * 0.8)
            height = int(screen_size.height() * 0.8)
            
        return QSize(width, height)

    @staticmethod
    def get_min_size(dpi: float) -> QSize:
        base_width = 800
        base_height = 600
        return QSize(
            int(base_width * dpi),
            int(base_height * dpi)
        )

    @staticmethod
    def scale_margins(dpi: float) -> tuple:
        base_margin = 10
        return (
            int(base_margin * dpi),
            int(base_margin * dpi)
        )
