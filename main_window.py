from PySide6.QtWidgets import QGraphicsView, QGraphicsProxyWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor
from infinite_canvas import InfiniteCanvas  # Changed to relative import
from harmonic_plot import HarmonicPlot  # Changed to relative import
from config import config  # Changed to relative import

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
        
        self.scene = InfiniteCanvas()
        self.setRenderHint(QPainter.Antialiasing)
        self.setScene(self.scene)
        self.setBackgroundBrush(QColor("##0A0A0A"))
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setWindowTitle(config.window_title)
        self.setGeometry(*config.window_position, *config.window_size)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

    def wheelEvent(self, event):
        # Check if mouse is over any plot
        pos = event.position()
        item = self.itemAt(int(pos.x()), int(pos.y()))
        
        if isinstance(item, QGraphicsProxyWidget) and isinstance(item.widget(), HarmonicPlot):
            # Let the plot handle its own wheel event
            super().wheelEvent(event)
        else:
            # Handle canvas zoom
            factor = 1.1
            if event.angleDelta().y() < 0:
                factor = 0.9
            
            self.scale(factor, factor)
            event.accept()
