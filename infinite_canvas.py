from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtCore import QPointF
from draggable_object import DraggableObject  # Changed to absolute
from utils import generate_stock_data, generate_fed_rates  # Add generate_fed_rates import

class InfiniteCanvas(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(-1000, -1000, 2000, 2000)
        
        # Create single chart
        plot = DraggableObject(title="Stock Price vs Fed Rate")
        plot.clicked.connect(self.deselect_all)
        self.addItem(plot)
        plot.setPos(QPointF(-400, -150))  # Center position
        
        # Generate both datasets
        x_vals, stock_vals = generate_stock_data()
        _, rate_vals = generate_fed_rates(days=len(x_vals))
        
        # Configure plot widget with both datasets
        plot.plot_widget.x_vals = x_vals
        
        # Add stock price on left axis
        plot.plot_widget.addNewLines(
            stock_vals, 
            data_label="Stock Price", 
            units="$", 
            plot_on_right=False
        )
        
        # Add fed rate on right axis
        plot.plot_widget.addNewLines(
            rate_vals, 
            data_label="Fed Rate", 
            units="%", 
            plot_on_right=True
        )

    def deselect_all(self):
        for item in self.items():
            if isinstance(item, DraggableObject):
                item.setZValue(0)
                item.update()