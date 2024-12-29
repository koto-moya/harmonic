from typing import Dict, List
from PySide6.QtWidgets import QGraphicsScene, QGraphicsProxyWidget
from PySide6.QtCore import QPointF
from PySide6.QtGui import QWheelEvent
from models.asset_payload import AssetPayload  # Add this import

from widgets.draggable_object import DraggableObject
from widgets.harmonic_plot import HarmonicPlot


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
        # Remove windows dictionary since we don't need it anymore

    def create_draggable_object(
        self,
        title: str,
        payload: AssetPayload,
        pos: tuple[float, float] = (-400, -150)
    ) -> DraggableObject:
        """
        Create a new draggable window object with typed payload.
        
        Args:
            title: Window title
            payload: Asset payload containing type and data
            pos: Initial position tuple (x, y)
            
        Returns:
            Created DraggableObject instance
        """
        window = DraggableObject(title=title)
        window.clicked.connect(self.deselect_all)
        self.addItem(window)
        window.setPos(QPointF(*pos))
        
        # Handle payload based on type
        if payload.type == "chart":
            window.add_harmonic_plot(
                payload.x_values,
                payload.data_series,
                payload.is_datetime,
                payload.enable_mouseover
            )
        elif payload.type == "table":
            # Add table handling here if needed
            pass
        elif payload.type == "custom":
            # Add custom widget handling here if needed
            pass
            
        return window

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
