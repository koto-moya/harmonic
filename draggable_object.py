from PySide6.QtWidgets import (QGraphicsItem, QGraphicsProxyWidget, 
                             QPushButton)  # Add QPushButton import
from PySide6.QtCore import QObject, QRectF, Signal, QMarginsF
from PySide6.QtGui import QPen, QColor
from PySide6.QtCore import Qt
from header_widget import HeaderWidget  # Changed to absolute
from harmonic_plot import HarmonicPlot  # Changed to absolute
from utils import generate_stock_data  # Changed to absolute

class DraggableObject(QGraphicsItem, QObject):
    selected_item = None
    clicked = Signal()
    closed = Signal(object)  # Add signal for close events

    def __init__(self, title: str = "Plot Title", width=780, height=420, margins=QMarginsF(0, 0, 0, 1)):
        super().__init__()
        QObject.__init__(self)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

        # Cache commonly used values - increase title height
        self._plot_height = height * 0.92
        self._title_height = height * 0.08
        self._width = width
        self.title = title
        self.selected_color =QPen(QColor(48, 0, 179, 255), 1.0) 
        self.unselected_color =QPen(QColor(80, 80, 80, 255), 1.0) 
        
        self.header_proxy = QGraphicsProxyWidget(self)
        self.plot_proxy = QGraphicsProxyWidget(self)
        self.rect = QRectF(0, 0, width, height).marginsRemoved(margins)

        # Add close button
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(16, 16)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #c9d1d9;
                font-size: 14px;
            }
            QPushButton:hover {
                color: #ff5555;
            }
        """)
        self.close_btn.clicked.connect(self._on_close)
        
        # Create proxy for close button
        self.close_btn_proxy = QGraphicsProxyWidget(self)
        self.close_btn_proxy.setWidget(self.close_btn)
        # Position in top-right corner with 4px padding
        self.close_btn_proxy.setPos(width - 20, 4)

    def _on_close(self):
        """Handle close button click"""
        self.closed.emit(self)  # Emit signal with self reference
        if self.scene():
            self.scene().removeItem(self)
        self.deleteLater()

    def addHeader(self, ):
        self.header_widget = HeaderWidget(self.title, self._width, int(self._title_height))
        self.header_proxy.setWidget(self.header_widget)

    def addContent(self, content: HarmonicPlot): # only accepts HarmonicPlot for now
        self.addHeader()
        self.header_widget.set_connected_widget(content)
        content.setFixedSize(self._width, int(self._plot_height))
        content.mouse_moved_signal.connect(self.header_widget.update_values)
        self.plot_proxy.setWidget(content)
        self.plot_proxy.setPos(0, self.header_proxy.size().height())

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        if DraggableObject.selected_item == self:
            pen = self.selected_color
        else:
            pen = self.unselected_color 
        pen.setJoinStyle(Qt.BevelJoin)
        painter.setPen(pen)
        painter.drawRect(self.rect)

    def mousePressEvent(self, event):
        if DraggableObject.selected_item and DraggableObject.selected_item != self:
            DraggableObject.selected_item = None
            
        DraggableObject.selected_item = self
        self.clicked.emit()
        self.update()
        self.scene().update()
        self.setZValue(1)  # Bring selected item to the top
        super().mousePressEvent(event)