from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtCore import QPointF
from draggable_object import DraggableObject  
from harmonic_plot import HarmonicPlot
from utils import generate_stock_data, generate_fed_rates  

class InfiniteCanvas(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(-10000, -10000, 20000, 20000)
        self.windows = {}  # Store plots by ID
        
        # Create initial chart
        window_id = self.create_draggable_object("Stock Price vs Fed Rate", pos=(-400, -150))
        self.add_stock_and_rate_chart(window_id)

    def create_draggable_object(self, title, pos=(-400, -150)):
        """Create a new draggable object and return its ID"""
        window = DraggableObject(title=title)
        window.clicked.connect(self.deselect_all)
        self.addItem(window)
        window.setPos(QPointF(*pos))
        
        window_id = id(window)
        self.windows[window_id] = window
        return window_id

    def add_stock_and_rate_chart(self, window_id):
        """Add stock price and fed rate chart to a draggable object"""
        if window_id not in self.windows:
            return
            
        window = self.windows[window_id]
        plot = HarmonicPlot(enable_mouseover=True)
        window.addContent(plot)
        
        # Generate both datasets
        x_vals, stock_vals = generate_stock_data()
        _, rate_vals = generate_fed_rates(days=len(x_vals))
        
        # Configure plot widget with both datasets
        plot.x_vals = x_vals
        
        # Add stock price on left axis
        plot.addNewLines(
            stock_vals, 
            data_label="Stock Price", 
            units="$", 
            plot_on_right=False
        )
        
        # Add fed rate on right axis
        # plot.addNewLines(
        #     rate_vals, 
        #     data_label="Fed Rate", 
        #     units="%", 
        #     plot_on_right=True
        # )

    def deselect_all(self):
        for item in self.items():
            if isinstance(item, DraggableObject):
                item.setZValue(0)
                item.update()
