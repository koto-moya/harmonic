from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtCore import QPointF
from draggable_object import DraggableObject  # Changed to absolute
from utils import generate_stock_data, generate_fed_rates  # Add generate_fed_rates import

class InfiniteCanvas(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(-1000, -1000, 2000, 2000)
        self.plots = {}  # Store plots by ID
        
        # Create initial chart
        plot_id = self.create_draggable_object("Stock Price vs Fed Rate", pos=(-400, -150))
        self.add_stock_and_rate_chart(plot_id)

    def create_draggable_object(self, title, pos=(-400, -150), width=780, height=420):
        """Create a new draggable object and return its ID"""
        plot = DraggableObject(title=title, width=width, height=height)
        plot.clicked.connect(self.deselect_all)
        self.addItem(plot)
        plot.setPos(QPointF(*pos))
        
        plot_id = id(plot)
        self.plots[plot_id] = plot
        return plot_id

    def add_stock_and_rate_chart(self, plot_id):
        """Add stock price and fed rate chart to a draggable object"""
        if plot_id not in self.plots:
            return
            
        plot = self.plots[plot_id]
        
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
