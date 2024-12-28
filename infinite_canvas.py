from PySide6.QtWidgets import QGraphicsScene, QGraphicsProxyWidget
from PySide6.QtCore import QPointF, Qt
from draggable_object import DraggableObject  
from harmonic_plot import HarmonicPlot
from canvas_bar import CanvasBarWidget  # Add this import
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
        x_vals, stock_vals_qqq = generate_stock_data()
        _, rate_vals = generate_fed_rates(days=len(x_vals))
        x_vals, stock_vals_appl = generate_stock_data()
        
        # Configure plot widget with both datasets
        plot.x_vals = x_vals
        
        # Add stock price on left axis
        plot.addNewLines(
            stock_vals_qqq, 
            data_label="stock price qqq", 
            units="$", 
            plot_on_right=False
        )

        plot.addNewLines(
            stock_vals_appl, 
            data_label="stock price appl", 
            units="$", 
            plot_on_right=False
        )
        
        # Add fed rate on right axis
        plot.addNewLines(
            rate_vals, 
            data_label="Fed Rate", 
            units="%", 
            plot_on_right=True
        )

    def handle_wheel_event(self, event, view):
        """Handle wheel events for the canvas"""
        pos = event.position()
        item = view.itemAt(int(pos.x()), int(pos.y()))
        
        if isinstance(item, QGraphicsProxyWidget):
            if isinstance(item.widget(), HarmonicPlot):
                return False
        
        factor = 1.1 if event.angleDelta().y() > 0 else 0.9
        view.scale(factor, factor)
        return True

    def deselect_all(self):
        for item in self.items():
            if isinstance(item, DraggableObject):
                item.setZValue(0)
                item.update()
