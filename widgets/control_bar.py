from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QColor, QIcon, QPixmap
from config import config

class ControlBar(QWidget):
    close_requested = Signal()

    def __init__(self):
        super().__init__()
        self.setFixedHeight(30)
        
        # Create horizontal layout
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 0)  # Add small left/right margins
        layout.setSpacing(5)
        
        # Add icon
        icon_label = QLabel()
        icon = QIcon("resources/gestalt.ico")  # Adjust path as needed
        icon_pixmap = icon.pixmap(24, 24)  # Match height of control bar with padding
        icon_label.setPixmap(icon_pixmap)
        
        # Create close button with larger text
        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(24, 24)
        self.close_button.clicked.connect(self.close_requested.emit)
        self.close_button.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                color: {config.font.color};
                font-size: 18px;  /* Increase font size for the × symbol */
                font-family: Arial;  /* Use Arial for cleaner symbol rendering */
                padding: 0;
                margin: 0;
            }}
            QPushButton:hover {{
                color: {config.canvas_bar.close_button_hover};
            }}
        """)
        
        # Add widgets to layout
        layout.addWidget(icon_label)
        layout.addStretch()  # This pushes the close button to the right
        layout.addWidget(self.close_button)
        
        self.setLayout(layout)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(config.canvas_bar.background_color))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.dragging and self.offset:
            new_pos = event.globalPosition().toPoint() - self.offset
            self.window().move(self.window().pos() + new_pos)
            self.offset = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.dragging = False
