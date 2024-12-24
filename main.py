# Standard library imports
import sys
import os
from typing import List

# Third-party imports
import pyqtgraph as pg
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QFont

# Local imports
from main_window import MainWindow  # Changed from relative to absolute import
from config import config  # Changed from relative to absolute import

# Configure pyqtgraph settings
pg.setConfigOptions(
    antialias=config.chart.antialiasing,
    foreground=config.chart.axis_color,
    background=config.chart.background_color,
    useNumba=config.enable_numba
)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Load custom font using known working method
    path = os.path.join("resources", "OxygenMono-Regular.ttf")
    abs_path = os.path.abspath(path)
    font_id = QFontDatabase.addApplicationFont(abs_path)
    
    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, config.font.size)
        app.setFont(font)
        config.font.family = font_family  # Update config to use loaded font
    else:
        print("Failed to load font")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())