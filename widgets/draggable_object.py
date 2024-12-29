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
        title: str = "Plot Title",
        width: int = 780,
        height: int = 420,
        margins: QMarginsF = QMarginsF(0, 0, 0, 1)
    ) -> None:
        """
        Initialize the DraggableObject.

        Args:
            title: Title text for the header
            width: Widget width in pixels
            height: Widget height in pixels
            margins: Margins around the widget
        """
        super().__init__()
        QObject.__init__(self)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

        # Cache commonly used values
        self._plot_height = height * config.draggable.plot_height_ratio
        self._title_height = height * config.draggable.title_height_ratio
        self._width = width
        self.title = title
        
        # Configure appearance using config values
        self.selected_color = QPen(QColor(config.draggable.selected_color), config.draggable.border_width)
        self.unselected_color = QPen(QColor(config.draggable.unselected_color), config.draggable.border_width)
        
        # Set up widget proxies
        self.header_proxy = QGraphicsProxyWidget(self)
        self.plot_proxy = QGraphicsProxyWidget(self)
        self.rect = QRectF(0, 0, width, height).marginsRemoved(margins)

        self._setup_close_button()

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