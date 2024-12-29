from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QHBoxLayout,
    QLabel
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import (
    QPainter,
    QColor,
    QIcon,
    QMouseEvent
)
from config import config


class ControlBar(QWidget):
    """
    A custom window control bar widget that provides dragging and close functionality.
    
    Includes an application icon and a close button, with custom styling and drag behavior.
    """
    
    close_requested = Signal()

    def __init__(self) -> None:
        """Initialize the control bar with icon and close button."""
        super().__init__()
        self.setFixedHeight(config.canvas_bar.height)
        
        self.dragging = False
        self.offset = None
        
        self._setup_layout()
        self._setup_icon()
        self._setup_close_button()

    def _setup_layout(self) -> None:
        """Configure the main horizontal layout."""
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(5, 0, 5, 0)
        self.layout.setSpacing(5)
        self.setLayout(self.layout)

    def _setup_icon(self) -> None:
        """Add and configure the application icon."""
        icon_label = QLabel()
        icon = QIcon("resources/gestalt.ico")
        icon_pixmap = icon.pixmap(24, 24)
        icon_label.setPixmap(icon_pixmap)
        self.layout.addWidget(icon_label)
        self.layout.addStretch()

    def _setup_close_button(self) -> None:
        """Create and configure the close button."""
        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(
            config.canvas_bar.button_size,
            config.canvas_bar.button_size
        )
        self.close_button.clicked.connect(self.close_requested.emit)
        self.close_button.setStyleSheet(config.canvas_bar.close_button_style)
        self.layout.addWidget(self.close_button)

    def paintEvent(self, event) -> None:
        """
        Paint the control bar background.

        Args:
            event: QPaintEvent instance
        """
        painter = QPainter(self)
        painter.fillRect(
            self.rect(),
            QColor(config.canvas_bar.background_color)
        )

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Handle mouse press for window dragging.

        Args:
            event: QMouseEvent instance
        """
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """
        Handle mouse movement for window dragging.

        Args:
            event: QMouseEvent instance
        """
        if self.dragging and self.offset:
            new_pos = event.globalPosition().toPoint() - self.offset
            self.window().move(self.window().pos() + new_pos)
            self.offset = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """
        Handle mouse release to end dragging.

        Args:
            event: QMouseEvent instance
        """
        self.dragging = False
