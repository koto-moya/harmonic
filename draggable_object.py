from PySide6.QtWidgets import QGraphicsItem, QGraphicsProxyWidget
from PySide6.QtCore import QObject, QRectF, Signal, QMarginsF
from PySide6.QtGui import QPen, QColor
from PySide6.QtCore import Qt
from header_widget import HeaderWidget  # Changed to absolute
from harmonic_plot import HarmonicPlot  # Changed to absolute
from utils import generate_stock_data  # Changed to absolute

class DraggableObject(QGraphicsItem, QObject):
    selected_item = None
    clicked = Signal()

    def __init__(self, title: str = "Plot Title", width=780, height=420, margins=QMarginsF(0, 0, 0, 1)):
        super().__init__()
        QObject.__init__(self)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

        # Cache commonly used values - increase title height
        self._height_factor = height * 0.94
        self._title_height = height * 0.06
        
        # Update to use HeaderWidget instead of TitleWidget
        self.header_widget = HeaderWidget(title, width, int(height * 0.06))
        
        # Generate stock data
        x_vals, y_vals = generate_stock_data()
        self.plot_widget = HarmonicPlot(x_vals=x_vals)
        self.header_widget.set_plot_widget(self.plot_widget)
        self.plot_widget.setFixedSize(width, int(self._height_factor))
        self.plot_widget.addNewLines(y_vals, data_label="Stock Price", units="$")

        self.header_proxy = QGraphicsProxyWidget(self)
        self.plot_proxy = QGraphicsProxyWidget(self)

        self.header_proxy.setWidget(self.header_widget)
        self.plot_proxy.setWidget(self.plot_widget)
        self.plot_proxy.setPos(0, self.header_proxy.size().height())

        self.rect = QRectF(0, 0, width, height).marginsRemoved(margins)

        # Connect plot signals to title
        self.plot_widget.mouse_moved_signal.connect(self.header_widget.update_values)

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        if DraggableObject.selected_item == self:
            pen = QPen(QColor(255, 50, 26, 255), 1.0)
        else:
            pen = QPen(QColor(80, 80, 80, 255), 1.0)
        pen.setJoinStyle(Qt.RoundJoin)
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