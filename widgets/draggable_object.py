from typing import List, Tuple
import numpy as np
from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsProxyWidget,
    QPushButton
)
from PySide6.QtCore import (
    QObject,
    QRectF,
    Signal,
    QMarginsF,
    Qt
)
from PySide6.QtGui import QPen, QColor
from widgets.header_widget import HeaderWidget
from widgets.harmonic_plot import HarmonicPlot
from models.asset_payload import AssetPayload
from config import config


class DraggableObject(QGraphicsItem, QObject):
    """
    A draggable widget container that can hold a plot and header.
    
    Supports selection, dragging, and closing functionality.
    """
    
    selected_item = None
    clicked = Signal()
    closed = Signal(object)

    def __init__(
        self,
        payload: AssetPayload,
        margins: QMarginsF = QMarginsF(0, 0, 0, 1)
    ) -> None:
        """
        Initialize the DraggableObject.

        Args:
            payload: AssetPayload instance
            margins: Margins around the widget
        """
        super().__init__()
        QObject.__init__(self)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        self.payload = payload
        # Cache commonly used values
        self._plot_height = payload.height * config.draggable.plot_height_ratio
        self._title_height = payload.height * config.draggable.title_height_ratio
        self._width = payload.width
        self.title = payload.title
        
        # Configure appearance using config values
        self.selected_color = QPen(QColor(config.draggable.selected_color), config.draggable.border_width)
        self.unselected_color = QPen(QColor(config.draggable.unselected_color), config.draggable.border_width)
        
        # Set up widget proxies
        self.header_proxy = QGraphicsProxyWidget(self)
        self.plot_proxy = QGraphicsProxyWidget(self)
        self.rect = QRectF(0, 0, payload.width, payload.height).marginsRemoved(margins)

        self._setup_close_button()
        self.createContent()

    def _setup_close_button(self) -> None:
        """Configure and position the close button."""
        btn_config = config.draggable.close_button
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(btn_config['size'], btn_config['size'])
        self.close_btn.setStyleSheet(btn_config['style'])
        self.close_btn.clicked.connect(self._on_close)
        
        self.close_btn_proxy = QGraphicsProxyWidget(self)
        self.close_btn_proxy.setWidget(self.close_btn)
        self.close_btn_proxy.setPos(
            self._width - btn_config['x_offset'],
            btn_config['y_offset']
        )

    def _on_close(self) -> None:
        """Handle close button click event."""
        self.closed.emit(self)
        if self.scene():
            self.scene().removeItem(self)
        self.deleteLater()

    def addHeader(self) -> None:
        """Create and add the header widget."""
        self.header_widget = HeaderWidget(self.title, self._width, int(self._title_height))
        self.header_proxy.setWidget(self.header_widget)

    def addContent(self, content: HarmonicPlot) -> None:
        """
        Add content to the draggable container.

        Args:
            content: HarmonicPlot widget to display
        """
        self.addHeader()
        self.header_widget.set_connected_widget(content)
        content.setFixedSize(self._width, int(self._plot_height))
        content.mouse_moved_signal.connect(self.header_widget.update_values)
        self.plot_proxy.setWidget(content)
        self.plot_proxy.setPos(0, self.header_proxy.size().height())

    def createContent(self) -> None:
        """
        Add a Harmonic plot to this draggable object.
        """
                # Handle payload based on type
        if self.payload.type == "chart":
            plot = HarmonicPlot(x_vals=self.payload.x_values, enable_mouseover=self.payload.enable_mouseover, is_datetime=self.payload.is_datetime)
            self.addContent(plot)
            for line in self.payload.y_values_left:
                plot.addNewLines(line, data_label=self.payload.y_label_left, units=self.payload.left_units)
            if self.payload.dual_axis:
                for line in self.payload.y_values_right:
                    plot.addNewLines(line, data_label=self.payload.y_label_right, units=self.payload.right_units, plot_on_right=True)

        elif self.payload.type == "table":
            # Add table handling here if needed
            pass
        elif self.payload.type == "custom":
            # Add custom widget handling here if needed
            pass
        
            
    def boundingRect(self) -> QRectF:
        """Return the bounding rectangle of the widget."""
        return self.rect

    def paint(self, painter, option, widget) -> None:
        """
        Paint the widget border.

        Args:
            painter: QPainter instance
            option: QStyleOptionGraphicsItem instance
            widget: Optional widget being painted
        """
        pen = self.selected_color if DraggableObject.selected_item == self else self.unselected_color
        pen.setJoinStyle(Qt.BevelJoin)
        painter.setPen(pen)
        painter.drawRect(self.rect)

    def mousePressEvent(self, event) -> None:
        """
        Handle mouse press events for selection.

        Args:
            event: QGraphicsSceneMouseEvent instance
        """
        if DraggableObject.selected_item and DraggableObject.selected_item != self:
            DraggableObject.selected_item = None
            
        DraggableObject.selected_item = self
        self.clicked.emit()
        self.update()
        self.scene().update()
        self.setZValue(1)
        super().mousePressEvent(event)