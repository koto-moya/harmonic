from typing import Dict, Optional, Union
from PySide6.QtWidgets import QGraphicsScene, QGraphicsProxyWidget
from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QWheelEvent

from widgets.draggable_object import DraggableObject
from widgets.harmonic_plot import HarmonicPlot
from utils.utils import generate_stock_data, generate_fed_rates
import numpy as np


class InfiniteCanvas(QGraphicsScene):
    """
    An infinite scrollable canvas that manages multiple draggable chart windows.
    
    Provides a large workspace where multiple charts can be placed and manipulated.
    Supports both date-based and numeric-based charts with draggable windows.
    """

    def __init__(self) -> None:
        """Initialize the infinite canvas with default charts."""
        super().__init__()
        self.setSceneRect(-10000, -10000, 20000, 20000)
        self.windows: Dict[int, DraggableObject] = {}
        
        # Create initial charts
        self._create_initial_charts()

    def _create_initial_charts(self) -> None:
        """Create and position the default charts on canvas initialization."""
        date_window_id = self.create_draggable_object(
            title="Stock Price (Date Axis)",
            pos=(-800, -150)
        )
        self.add_stock_chart_datetime(date_window_id)
        
        number_window_id = self.create_draggable_object(
            title="Stock Price (Number Axis)",
            pos=(-200, -150)
        )
        self.add_stock_chart_numeric(number_window_id)

    def create_draggable_object(
        self,
        title: str,
        pos: tuple[float, float] = (-400, -150)
    ) -> int:
        """
        Create a new draggable window object.
        
        Args:
            title: Window title
            pos: Initial position tuple (x, y)
            
        Returns:
            Unique identifier for the created window
        """
        window = DraggableObject(title=title)
        window.clicked.connect(self.deselect_all)
        self.addItem(window)
        window.setPos(QPointF(*pos))
        
        window_id = id(window)
        self.windows[window_id] = window
        return window_id

    def add_stock_chart_datetime(self, window_id: int) -> None:
        """
        Add a stock price chart with datetime x-axis to specified window.
        
        Args:
            window_id: ID of the window to add chart to
        """
        window = self.windows.get(window_id)
        if not window:
            return
            
        plot = HarmonicPlot(enable_mouseover=True, is_datetime=True)
        window.addContent(plot)
        
        # Generate and add datasets
        x_vals, stock_vals_qqq = generate_stock_data()
        _, stock_vals_appl = generate_stock_data()
        
        plot.x_vals = x_vals
        plot.addNewLines(stock_vals_qqq, data_label="QQQ", units="$")
        plot.addNewLines(stock_vals_appl, data_label="AAPL", units="$")

    def add_stock_chart_numeric(self, window_id: int) -> None:
        """
        Add a stock price chart with numeric x-axis to specified window.
        
        Args:
            window_id: ID of the window to add chart to
        """
        window = self.windows.get(window_id)
        if not window:
            return
            
        plot = HarmonicPlot(enable_mouseover=True, is_datetime=False)
        window.addContent(plot)
        
        # Generate datasets with numeric x-axis
        days = 365
        x_vals = np.arange(days)
        _, stock_vals_qqq = generate_stock_data(days=days)
        _, stock_vals_appl = generate_stock_data(days=days)
        
        plot.x_vals = x_vals
        plot.addNewLines(stock_vals_qqq, data_label="QQQ", units="$")
        plot.addNewLines(stock_vals_appl, data_label="AAPL", units="$")

    def handle_wheel_event(self, event: QWheelEvent, view: QGraphicsProxyWidget) -> bool:
        """
        Handle mouse wheel events for zooming.
        
        Args:
            event: Mouse wheel event
            view: View widget receiving the event
            
        Returns:
            True if event was handled, False otherwise
        """
        pos = event.position()
        item = view.itemAt(int(pos.x()), int(pos.y()))
        
        if isinstance(item, QGraphicsProxyWidget):
            if isinstance(item.widget(), HarmonicPlot):
                return False
        
        factor = 1.1 if event.angleDelta().y() > 0 else 0.9
        view.scale(factor, factor)
        return True

    def deselect_all(self) -> None:
        """Reset z-index and update all draggable objects."""
        for item in self.items():
            if isinstance(item, DraggableObject):
                item.setZValue(0)
                item.update()
