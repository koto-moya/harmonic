from PySide6.QtWidgets import QGraphicsView, QWidget
from PySide6.QtCore import Qt, QObject, QEvent
from PySide6.QtGui import QPainter, QColor
from infinite_canvas import InfiniteCanvas
from canvas_bar import CanvasBarWidget
from config import config

class Layer(QObject):
    def __init__(self, host, child, alignment=Qt.AlignLeft, setWidth=False, setHeight=False, parent=None):
        super().__init__(parent)
        self._host = host
        self._child = child
        self._alignment = alignment
        self._setWidth = setWidth
        self._setHeight = setHeight
        child.setParent(host)
        host.installEventFilter(self)

    def eventFilter(self, watched, event):
        if watched != self._host or event.type() != QEvent.Resize:
            return False
        hostSize = event.size()
        childSize = self._child.sizeHint()
        alignment = self._alignment
        x = 0
        y = 0
        dWidth = max(0, hostSize.width() - childSize.width())
        dHeight = max(0, hostSize.height() - childSize.height())
        
        if alignment & Qt.AlignRight:
            x = dWidth
        elif alignment & Qt.AlignHCenter:
            x = dWidth / 2
        
        if alignment & Qt.AlignVCenter:
            y = dHeight / 2
        elif alignment & Qt.AlignBottom:
            y = dHeight
        
        width = hostSize.width() if self._setWidth else childSize.width()
        height = hostSize.height() if self._setHeight else childSize.height()
        self._child.setGeometry(x, y, width, height)
        return False

class MainWindow(QGraphicsView):
    def __init__(self):
        super().__init__()
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
        # Enable viewport caching
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.setOptimizationFlags(QGraphicsView.DontAdjustForAntialiasing)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Hide horizontal scrollbar
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)    # Hide vertical scrollbar
        
        self.setRenderHint(QPainter.Antialiasing)
        self.setBackgroundBrush(QColor(config.canvas_color))
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setWindowTitle(config.application_title)
        self.setGeometry(*config.application_position, *config.application_size)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        
        # Create and store canvases
        self.canvases = {}
        self.current_scene = None
        
        # Initialize home canvas
        self.home_canvas = InfiniteCanvas()
        self.canvases["home"] = self.home_canvas
        self.setScene(self.home_canvas)
        self.current_scene = self.home_canvas
        
        # Create and position the canvas bar
        self.canvas_bar = CanvasBarWidget()
        self.canvas_bar_layer = Layer(
            self, 
            self.canvas_bar, 
            Qt.AlignBottom | Qt.AlignHCenter, 
            setWidth=True
        )
        self.canvas_bar.setContentsMargins(0, 0, 0, 5)
        self.canvas_bar.raise_()
        
        # Connect signals
        self.canvas_bar.canvas_selected.connect(self.switch_canvas)
        self.canvas_bar.canvas_closed.connect(self.remove_canvas)

    def create_new_canvas(self):
        """Create a new canvas tab"""
        new_canvas = InfiniteCanvas()
        tab_id = f"tab_{len(self.canvases)}"
        self.canvases[tab_id] = new_canvas
        self.switch_canvas(tab_id)

    def switch_canvas(self, tab_id: str):
        """Switch to the specified canvas"""
        if tab_id in self.canvases:
            self.current_scene = self.canvases[tab_id]
            self.setScene(self.current_scene)

    def remove_canvas(self, tab_id: str):
        """Remove a canvas when its tab is closed"""
        if tab_id in self.canvases and tab_id != "home":
            del self.canvases[tab_id]
            self.switch_canvas("home")

    def wheelEvent(self, event):
        """Handle wheel events and delegate to scene"""
        if self.current_scene and self.current_scene.handle_wheel_event(event, self):
            event.accept()
        else:
            super().wheelEvent(event)
