from PySide6.QtWidgets import QGraphicsScene, QGraphicsProxyWidget
from PySide6.QtCore import QPointF, Qt
from widgets.draggable_object import DraggableObject  
from widgets.harmonic_plot import HarmonicPlot
from widgets.canvas_bar import CanvasBarWidget  # Add this import
from utils.utils import generate_stock_data, generate_fed_rates
import numpy as np

class InfiniteCanvas(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(-10000, -10000, 20000, 20000)
        self.windows = {}  # Store plots by ID
        
        # Create two initial charts
        date_window_id = self.create_draggable_object("Stock Price (Date Axis)", pos=(-800, -150))
        self.add_stock_chart_datetime(date_window_id)
        
        number_window_id = self.create_draggable_object("Stock Price (Number Axis)", pos=(-200, -150))
        self.add_stock_chart_numeric(number_window_id)

    def create_draggable_object(self, title, pos=(-400, -150)):
        """Create a new draggable object and return its ID"""
        window = DraggableObject(title=title)
        window.clicked.connect(self.deselect_all)
        self.addItem(window)
        window.setPos(QPointF(*pos))
        
        window_id = id(window)
        self.windows[window_id] = window
        return window_id

    def add_stock_chart_datetime(self, window_id):
        """Add stock price chart with datetime x-axis"""
        if window_id not in self.windows:
            return
            
        window = self.windows[window_id]
        plot = HarmonicPlot(enable_mouseover=True, is_datetime=True)
        window.addContent(plot)
        
        # Generate datasets
        x_vals, stock_vals_qqq = generate_stock_data()
        _, stock_vals_appl = generate_stock_data()
        
        # Configure plot widget
        plot.x_vals = x_vals
        plot.addNewLines(stock_vals_qqq, data_label="QQQ", units="$")
        plot.addNewLines(stock_vals_appl, data_label="AAPL", units="$")

    def add_stock_chart_numeric(self, window_id):
        """Add stock price chart with numeric x-axis"""
        if window_id not in self.windows:
            return
            
        window = self.windows[window_id]
        plot = HarmonicPlot(enable_mouseover=True, is_datetime=False)
        window.addContent(plot)
        
        # Generate datasets with numeric x-axis
        days = 365
        x_vals = np.arange(days)  # Simple numeric x-axis
        _, stock_vals_qqq = generate_stock_data(days=days)
        _, stock_vals_appl = generate_stock_data(days=days)
        
        # Configure plot widget
        plot.x_vals = x_vals
        plot.addNewLines(stock_vals_qqq, data_label="QQQ", units="$")
        plot.addNewLines(stock_vals_appl, data_label="AAPL", units="$")

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
