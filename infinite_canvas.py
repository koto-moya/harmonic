from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtCore import QPointF
from draggable_object import DraggableObject  # Changed to absolute
from utils import generate_stock_data  # Changed to absolute

class InfiniteCanvas(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(-1000, -1000, 2000, 2000)
        
        # Create single chart
        plot = DraggableObject(title="Stock Price")
        plot.clicked.connect(self.deselect_all)
        self.addItem(plot)
        plot.setPos(QPointF(-400, -150))  # Center position
        
        # Generate basic data
        x_vals, y_vals = generate_stock_data()
        
        # Configure plot widget with data
        plot.plot_widget.x_vals = x_vals
        plot.plot_widget.addNewLines(
            y_vals, 
            data_label="Price", 
            units="$", 
            plot_on_right=False
        )

    def deselect_all(self):
        for item in self.items():
            if isinstance(item, DraggableObject):
                item.setZValue(0)
                item.update()