# Standard library imports
import sys
import os
from typing import List

# Third-party imports
import pyqtgraph as pg
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QFont

# Local imports
from windows.main_window import MainWindow  
from windows.login_window import LoginWindow 
from config import config  

# Configure pyqtgraph settings
pg.setConfigOptions(
    antialias=config.chart.antialiasing,
    foreground=config.chart.axis_color,
    background=config.chart.background_color,
    useNumba=config.enable_numba
)

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        
        # Load custom font using known working method
        path = os.path.join("resources", "OxygenMono-Regular.ttf")
        abs_path = os.path.abspath(path)
        font_id = QFontDatabase.addApplicationFont(abs_path)
        
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_family, config.font.size)
            app.setFont(font)
            config.font.family = font_family
        else:
            print("Failed to load font, using system default")
            
        # Keep reference to main window to prevent premature garbage collection
        main_window = None
        def on_login_success(token):
            global main_window
            if token:
                main_window = MainWindow(token)
                main_window.show()
                login_window.close()
        
        login_window = LoginWindow()
        login_window.login_successful.connect(on_login_success)
        login_window.show()
        
        sys.exit(app.exec())
    except Exception as e:
        print(f"Critical error: {str(e)}")
        sys.exit(1)