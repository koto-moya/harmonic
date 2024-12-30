from typing import Dict, Optional
from PySide6.QtWidgets import (
    QGraphicsView,
    QApplication,
    QSizeGrip
)
from PySide6.QtCore import Qt, QEvent, QRect, QPointF, Signal, QSize
from PySide6.QtGui import QPainter, QColor, QTransform

from scenes.infinite_canvas import InfiniteCanvas
from widgets.canvas_bar import CanvasBarWidget
from widgets.control_bar import ControlBar
from widgets.Nyx import Nyx
from utils.layer import Layer
from config import config
from widgets.controller import Controller


class MainWindow(QGraphicsView):
    """
    Main application window with infinite canvas and UI controls.
    
    Provides a frameless window with custom controls, multiple canvases,
    and parallax background effects.
    """
    current_scene_changed = Signal(object)
    
    # Add zoom limit constants
    ZOOM_MAX_SCALE = 2.0  # 3x initial scale
    ZOOM_MIN_SCALE = 0.3  # 0.3x initial scale
    
    def __init__(self, token) -> None:
        if not token:
            raise ValueError("Invalid token")
        super().__init__()
        self.token = token
        self._refs = []  # Keep references to prevent GC
        self.initial_scale = 1.0  # Store initial scale
        self._setup_window()
        self._setup_graphics()
        self._setup_canvases()
        self._setup_controls()
        self._setup_background()

    def _setup_window(self) -> None:
        """Configure window properties and positioning."""
        screen = QApplication.primaryScreen().geometry()
        window_width = 1630
        window_height = 930
        center_x = (screen.width() - window_width) // 2
        center_y = (screen.height() - window_height) // 2
        
        self.setGeometry(center_x, center_y, window_width, window_height)
        self.setWindowTitle(config.application_title)
        self.setWindowFlags(
            self.windowFlags() | 
            Qt.FramelessWindowHint | 
            Qt.MSWindowsFixedSizeDialogHint
        )
        
        # Remove system resize handles
        for child in self.findChildren(QSizeGrip):
            child.setVisible(False)
            child.deleteLater()

    def _setup_graphics(self) -> None:
        """Configure graphics view properties."""
        self.setCacheMode(
            QGraphicsView.CacheBackground if config.performance.cache_background 
            else QGraphicsView.CacheNone
        )
        self.setViewportUpdateMode(
            QGraphicsView.SmartViewportUpdate if config.performance.smart_viewport_update 
            else QGraphicsView.FullViewportUpdate
        )
        self.setOptimizationFlags(
            QGraphicsView.DontAdjustForAntialiasing if config.performance.disable_antialiasing_optimization 
            else QGraphicsView.DontSavePainterState
        )
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setRenderHint(QPainter.Antialiasing)
        self.setBackgroundBrush(QColor(config.canvas_color))
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

    def _setup_canvases(self) -> None:
        """Initialize and store canvases."""
        self.canvases: Dict[str, InfiniteCanvas] = {}
        self.current_scene: Optional[InfiniteCanvas] = None
        
        self.home_canvas = InfiniteCanvas()
        self.canvases["home"] = self.home_canvas
        self.setScene(self.home_canvas)
        self.current_scene = self.home_canvas

    def _setup_controls(self) -> None:
        """Create and position control and canvas bars."""
        self.control_bar = ControlBar()
        self.control_bar_layer = Layer(
            self,
            self.control_bar,
            Qt.AlignTop | Qt.AlignLeft,
            setWidth=True
        )
        self.control_bar.raise_()
        self.control_bar.close_requested.connect(self.close)
        
        self.canvas_bar = CanvasBarWidget()
        self.canvas_bar_layer = Layer(
            self, 
            self.canvas_bar, 
            Qt.AlignBottom | Qt.AlignLeft,
            setWidth=True
        )
        self.canvas_bar.raise_()
        self.canvas_bar.canvas_selected.connect(self.switch_canvas)
        self.canvas_bar.canvas_closed.connect(self.remove_canvas)
        self.canvas_bar.new_canvas_requested.connect(self.create_new_canvas)

        # Replace the Layer-based controller setup with manual positioning
        self.controller = Controller()
        self.controller.setParent(self)
        
        # Use config values for positioning
        initial_x = self.width() - self.controller.width() - config.controller.position_x_offset
        initial_y = config.controller.position_y_offset
        self.controller.move(initial_x, initial_y)
        
        # Keep references to prevent premature destruction
        self._refs.extend([self.control_bar, self.canvas_bar, self.controller])
        
        self.controller.raise_()
        self.controller.token = self.token
        self.controller.set_current_canvas(self.current_scene)
        self.current_scene_changed.connect(self.controller.set_current_canvas)

    def _setup_background(self) -> None:
        """Initialize background colors and pattern."""
        self.base_color = QColor(config.canvas_color)
        self.pattern_color = QColor(config.canvas_color).lighter(150)
        self.dot_size = 2

    def create_new_canvas(self) -> None:
        """Create a new canvas tab."""
        new_canvas = InfiniteCanvas()
        tab_id = f"tab_{len(self.canvases)}"
        self.canvases[tab_id] = new_canvas
        self.switch_canvas(tab_id)

    def create_draggable_object(self, title, payload) -> None:
        """Add a draggable object to the current scene."""
        self.current_scene.create_draggable_object(title, payload)
        pass

    def switch_canvas(self, tab_id: str) -> None:
        """Switch to the specified canvas."""
        if tab_id in self.canvases:
            self.current_scene = self.canvases[tab_id]
            self.setScene(self.current_scene)
            self.current_scene_changed.emit(self.current_scene)

    def remove_canvas(self, tab_id: str) -> None:
        """Remove a canvas when its tab is closed."""
        if tab_id in self.canvases and tab_id != "home":
            del self.canvases[tab_id]
            self.switch_canvas("home")

    def wheelEvent(self, event: QEvent) -> None:
        """Handle wheel events with zoom limits."""
        if self.current_scene:
            # Get current scale
            current_scale = self.transform().m11()  # Get current horizontal scale
            
            # Calculate zoom factor based on wheel delta
            factor = 1.1 if event.angleDelta().y() > 0 else 0.9
            new_scale = current_scale * factor
            
            # Check if new scale would exceed limits
            if (new_scale <= self.initial_scale * self.ZOOM_MAX_SCALE and 
                new_scale >= self.initial_scale * self.ZOOM_MIN_SCALE):
                # Only apply zoom if within limits
                if self.current_scene.handle_wheel_event(event, self):
                    event.accept()
                    return
        
        super().wheelEvent(event)

    def drawBackground(self, painter: QPainter, rect: QRect) -> None:
        """Draw background with static dot grid pattern."""
        painter.fillRect(rect, self.base_color)
        
        # Set up dot drawing
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.pattern_color)
        
        # Get visible area
        visible_rect = self.mapToScene(self.viewport().rect()).boundingRect()
        
        # Fixed grid spacing
        spacing = 50
        
        # Draw dots aligned to grid
        x = visible_rect.left() - (visible_rect.left() % spacing)
        while x <= visible_rect.right():
            y = visible_rect.top() - (visible_rect.top() % spacing)
            while y <= visible_rect.bottom():
                painter.drawEllipse(int(x), int(y), self.dot_size, self.dot_size)
                y += spacing
            x += spacing

    def resizeEvent(self, event: QEvent) -> None:
        """Handle window resize events."""
        super().resizeEvent(event)
        
        # Update controller position
        new_width = event.size().width()
        new_x = new_width - self.controller.width() - config.controller.position_x_offset
        self.controller.move(new_x, config.controller.position_y_offset)
        
        # Make sure controller stays on top
        self.controller.raise_()

    def closeEvent(self, event):
        """Clean up resources properly."""
        self._refs.clear()  # Clear references
        super().closeEvent(event)
