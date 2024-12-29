from typing import Dict, Optional
from PySide6.QtWidgets import (
    QGraphicsView,
    QApplication,
    QSizeGrip
)
from PySide6.QtCore import Qt, QEvent, QRect, QPointF, Signal
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
    def __init__(self) -> None:
        super().__init__()
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
        screen_geometry = self.geometry()
        controller_x = screen_geometry.width() - self.controller.width() - config.controller.position_x_offset
        controller_y = config.controller.position_y_offset
        self.controller.move(controller_x, controller_y)
        
        self.controller.raise_()
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
        """Handle wheel events and delegate to scene."""
        if self.current_scene and self.current_scene.handle_wheel_event(event, self):
            event.accept()
        else:
            super().wheelEvent(event)

    def drawBackground(self, painter: QPainter, rect: QRect) -> None:
        """Override drawBackground to create a dot-based parallax effect."""
        painter.fillRect(rect, self.base_color)
        
        if config.parallax.enabled:
            transform: QTransform = self.transform()
            scale: float = transform.m11()
            
            view_center: QPointF = self.viewport().rect().center()
            scene_center: QPointF = self.mapToScene(view_center)
            
            parallax_x: float = scene_center.x() * config.parallax.factor_x
            parallax_y: float = scene_center.y() * config.parallax.factor_y
            
            spacing: int = 50
            
            offset_x: float = parallax_x % spacing
            offset_y: float = parallax_y % spacing
            
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.pattern_color)
            
            visible_rect: QRect = self.mapToScene(self.viewport().rect()).boundingRect()
            
            x: float = visible_rect.left() - (visible_rect.left() % spacing) - offset_x
            while x <= visible_rect.right():
                y: float = visible_rect.top() - (visible_rect.top() % spacing) - offset_y
                while y <= visible_rect.bottom():
                    painter.drawEllipse(int(x), int(y), self.dot_size, self.dot_size)
                    y += spacing
                x += spacing
