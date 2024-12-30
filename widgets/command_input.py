from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import QPainter, QFontMetrics
from PySide6.QtCore import Qt, QRect

class CommandInput(QLineEdit):
    PREFIX = " > "
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._prefix_width = QFontMetrics(self.font()).horizontalAdvance(self.PREFIX)
        self.textMargins = self.contentsMargins()
        # Add left margin to make room for prefix
        self.setTextMargins(self._prefix_width, 0, 0, 0)
        
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(self.palette().text().color())
        painter.drawText(QRect(self.textMargins.left(), 0, self._prefix_width, self.height()),
                        Qt.AlignLeft | Qt.AlignVCenter,
                        self.PREFIX)
