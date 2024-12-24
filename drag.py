import sys
import os
import numpy as np
import pyqtgraph as pg
import random  # Add to imports at top
# ...existing imports...
from config import config

pg.setConfigOptions(
    antialias=config.chart.antialiasing,  # Use the same setting
    foreground=config.chart.axis_color,
    background=config.chart.background_color,
    useNumba=config.enable_numba
)

from PySide6.QtWidgets import (
    QApplication,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QFrame,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QWidget,
    QGraphicsProxyWidget,
    QHBoxLayout,
    QGridLayout
)
from PySide6.QtCore import Qt, QPointF, QRectF, Signal, QObject, QSize, QMarginsF, Slot, QTimer
from PySide6.QtGui import QPainter, QColor, QPen
from typing import List, Optional
from pyqtgraph.graphicsItems.DateAxisItem import DateAxisItem
import datetime

import pyqtgraph as pg
from PySide6.QtGui import QFontDatabase, QFont

def apply_font_style(widget):
    """Apply global font style to a widget"""
    font = QFont(config.font.family)
    font.setPointSize(config.font.size)
    font.setWeight(config.font.weight)
    widget.setFont(font)
    widget.setStyleSheet(f"color: {config.font.color};")

class CustomDateAxisItem(DateAxisItem):
    def tickStrings(self, values, scale, spacing):
        # Center ticks to midday (12:00 PM)
        return [datetime.datetime.fromtimestamp(value).strftime("%m/%d/%y") for value in values]

def generate_stock_data(days=365, start_price=1.0, end_price=100.0, volatility=0.9):  # Increased volatility from 0.02 to 0.15
    """Generate simulated stock price data with geometric Brownian motion"""
    t = np.linspace(0, days, days)
    # Calculate drift to reach target price
    total_return = np.log(end_price / start_price)
    mu = total_return / days + (volatility ** 2) / 2
    
    # Generate random walk
    W = np.random.standard_normal(size=days)
    W = np.cumsum(W) * np.sqrt(1/days)
    
    # Calculate price path
    S = start_price * np.exp((mu - volatility ** 2 / 2) * t + volatility * W)
    return t, np.round(S, 2)

class HarmonicPlot(pg.PlotWidget):
    # Add signal
    mouse_moved_signal = Signal(dict)  # Signal to emit {label: value} pairs

    def __init__(self, x_vals=None, enable_mouseover=False, is_datetime=True):
        super().__init__()
        self.setRenderHint(QPainter.Antialiasing, config.chart.antialiasing)
        
        self.plot_item = self.getPlotItem()
        self.setBackground(config.chart.background_color)
        self.plot_item.setDownsampling(auto=config.chart.downsampling, mode='peak')  # Enable downsampling
        self.plot_item.setClipToView(config.chart.clip_to_view)  # Only render visible data
        
        # Add the available_colors list that was missing
        self.available_colors = config.chart.color_palette.copy()
        
        # Pre-allocate numpy arrays for better performance
        if x_vals is not None:
            self.x_vals = np.round(x_vals, config.performance.decimal_precision)
        
        self.plot_info = {}
        self.units = {}
        self.color_map = {}
        self.scatters = {}
        self.right_vb = None
        self.vb = self.plot_item.vb  # Main ViewBox
        self.is_datetime = is_datetime

        if enable_mouseover:
            self.scene().sigMouseMoved.connect(self.mouse_moved)

        # Add scatter point for mouse tracking with configured size
        self.scatter = pg.ScatterPlotItem(
            size=config.chart.scatter_dot_size,  # Use new scatter_dot_size parameter
            pen=pg.mkPen(None), 
            brush=pg.mkBrush(255, 255, 255, config.chart.scatter_opacity)
        )
        self.plot_item.addItem(self.scatter)

        # Synchronize ViewBoxes
        self.vb.sigResized.connect(self.updateViews)

        # Lock Y-axis movement and set mouse enabled only for X
        view_box = self.plot_item.getViewBox()
        view_box.setMouseEnabled(x=True, y=False)
        view_box.setLimits(yMin=None, yMax=None)
        
        # Set auto range once for initial view, then disable
        view_box.enableAutoRange(axis='y')
        view_box.enableAutoRange(axis='x')
        
        # Configure grid and axes separately
        self.plot_item.showGrid(x=False, y=True)
        
        # Style the grid
        grid_pen = pg.mkPen(color=config.chart.grid_color, alpha=int(255 * config.chart.grid_alpha))
        self.plot_item.showGrid(x=False, y=True, alpha=config.chart.grid_alpha)
        
        # Style the axes
        axis_pen = pg.mkPen(
            color=config.chart.axis_color, 
            width=config.chart.axis_width, 
            alpha=int(255 * config.chart.axis_alpha)
        )
        self.plot_item.getAxis('left').setPen(axis_pen)
        self.plot_item.getAxis('bottom').setPen(axis_pen)
        
        # Set axis layers
        self.plot_item.getAxis('left').setZValue(-1000)
        self.plot_item.getAxis('bottom').setZValue(-1000)
        
        # Wait for the next update cycle to disable auto-range
        QTimer.singleShot(0, lambda: view_box.disableAutoRange())
        
        self.setAntialiasing(False)  # Start with antialiasing off

        # Enable mouse tracking
        self.scene().sigMouseMoved.connect(self._on_mouse_move)

        # Fix mouse tracking
        self.plotItem.vb.setAutoVisible(y=1.0)
        self.scene().sigMouseMoved.connect(self._on_mouse_move)
        self.proxy = pg.SignalProxy(
            self.scene().sigMouseMoved, 
            rateLimit=config.performance.ratelimit_mouse, 
            slot=self._on_mouse_move
        )

    def wheelEvent(self, ev):
        # Only zoom X-axis on wheel event
        if self.plot_item.sceneBoundingRect().contains(ev.position()):  # Changed from pos() to position()
            view_box = self.plot_item.getViewBox()
            delta = ev.angleDelta().y()
            
            if delta != 0:
                scale = 1.01 ** (delta / 20.0)
                view_box.scaleBy(x=scale, y=1.0)  # Only scale X axis
                
            ev.accept()

    def updateViews(self):
        if self.right_vb:
            self.right_vb.setGeometry(self.plot_item.vb.sceneBoundingRect())
            self.right_vb.linkedViewChanged(self.plot_item.vb, self.right_vb.XAxis)

    def addNewLines(self, y_vals, data_label=None, units=None, plot_on_right=False):
        # Round y_vals to configured precision
        y_vals = np.round(y_vals, config.performance.decimal_precision)
        
        if data_label:
            self.plot_info[data_label] = y_vals
            self.units[data_label] = units  # Store units with data label

        # Random color selection instead of popping first color
        furthest_color = random.choice(config.chart.color_palette)
        self.color_map[data_label] = furthest_color

        pen = pg.mkPen(color=furthest_color, width=2)
        line = pg.PlotDataItem(
            self.x_vals, 
            y_vals,
            pen=pen,
            skipFiniteCheck=config.performance.skip_finite_check,
            downsample=config.chart.downsampling
        )

        if plot_on_right:
            # Create right ViewBox and AxisItem
            self.right_vb = pg.ViewBox()
            self.right_vb.setMouseEnabled(x=False, y=False)  # Disable mouse interaction for right axis
            self.right_axis = pg.AxisItem('right')
            self.right_axis.setLabel("Right Axis")
            self.right_axis.setStyle(tickLength=-10)

            # Add AxisItem to the plot layout
            self.plot_item.layout.addItem(self.right_axis, 2, 2)
            self.plot_item.showAxis('right')
            self.right_axis.linkToView(self.right_vb)
            self.plot_item.scene().addItem(self.right_vb)
            self.right_vb.addItem(line)
        else:
            self.plot_item.addItem(line)

    def _on_mouse_move(self, evt):
        if isinstance(evt, tuple):
            # Handle proxy signal case
            pos = evt[0]
        else:
            # Handle direct signal case
            pos = evt
            
        if self.sceneBoundingRect().contains(pos):
            mouse_point = self.plotItem.vb.mapSceneToView(pos)
            x = mouse_point.x()
            
            # Find nearest x value
            if self.x_vals is not None and len(self.x_vals) > 0:
                idx = min(max(0, int(x)), len(self.x_vals)-1)
                
                # Update scatter point position
                scatter_points = []
                for label, data in self.plot_info.items():
                    if idx < len(data):
                        y = float(data[idx])
                        scatter_points.append({
                            'pos': (self.x_vals[idx], y),
                            'brush': pg.mkBrush(self.color_map.get(label, '#FFFFFF'))
                        })
                
                self.scatter.setData(spots=scatter_points)
                
                # Emit values for labels
                values = {
                    label: {
                        'value': data[idx],
                        'units': self.units.get(label)
                    } 
                    for label, data in self.plot_info.items() 
                    if idx < len(data)
                }
                if values:
                    self.mouse_moved_signal.emit(values)
        else:
            # Clear scatter point when mouse leaves plot
            self.scatter.clear()

class HeaderWidget(QWidget):
    def __init__(self, title: str = "Title", parent_width: int = 0, parent_height: int = 0):
        super().__init__()
        
        # Main horizontal layout
        self.header_layout = QHBoxLayout(self)
        self.margin_h = parent_width * 0.02
        self.margin_v = parent_height * 0.1
        self.header_layout.setContentsMargins(self.margin_h, self.margin_v, self.margin_h, self.margin_v)
        self.header_layout.setSpacing(10)
        
        self.parent_width = parent_width
        self.parent_height = parent_height
        self.setFixedSize(self.parent_width, self.parent_height)
        
        # Title takes 30% of width
        title_width = int(self.parent_width * 0.3)
        self.title_label = QLabel(title)
        self.title_label.setFixedSize(QSize(title_width, int(self.parent_height * 0.8)))
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.title_label.setStyleSheet(f"color: {config.font.color}; font-size: {config.font.size}px;")
        self.header_layout.addWidget(self.title_label)
        
        # Flexible spacer
        self.header_layout.addStretch()
        
        # Values container with grid layout - modified alignment
        self.values_container = QWidget()
        self.values_grid = QGridLayout(self.values_container)
        self.values_grid.setContentsMargins(0, 0, 0, 0)
        self.values_grid.setSpacing(5)
        self.values_grid.setAlignment(Qt.AlignTop)  # Align to top
        self.header_layout.addWidget(self.values_container)
        
        # Container for value labels
        self.value_labels = {}
        self.plot_widget = None
        self.max_cols = 2  # Number of columns in the grid

    def set_plot_widget(self, plot_widget):
        self.plot_widget = plot_widget

    @Slot(dict)
    def update_values(self, values: dict):
        if not self.plot_widget:
            return
            
        color_map = self.plot_widget.color_map
        label_width = int(self.parent_width * 0.2)  # Each label gets 20% of width
        label_height = int(self.parent_height * 0.4)  # Each label gets 40% of height
        
        # Clear existing labels if number of values changed
        if len(values) != len(self.value_labels):
            for label in self.value_labels.values():
                label.setParent(None)
            self.value_labels.clear()
        
        # Add labels in order
        for i, (label, data) in enumerate(values.items()):
            value = data['value']
            units = data['units']
            
            if label not in self.value_labels:
                self.value_labels[label] = QLabel()
                color = color_map.get(label, '#FFFFFF')
                self.value_labels[label].setFixedSize(QSize(label_width, label_height))
                self.value_labels[label].setStyleSheet(f"color: {color}; font-size: {config.font.size}px;")
                self.value_labels[label].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                
                # Calculate grid position ensuring left column starts at top
                row = i % (len(values) // 2 + len(values) % 2)  # Distribute evenly
                col = i // (len(values) // 2 + len(values) % 2)  # Switch columns after half
                self.values_grid.addWidget(self.value_labels[label], row, col)
            
            # Format value based on units
            if units == '$':
                formatted_value = f"${value:,.2f}"
            else:
                formatted_value = f"{value:.2f}{units if units else ''}"
            
            self.value_labels[label].setText(f"{label}: {formatted_value}")

class DraggableObject(QGraphicsItem, QObject):
    selected_item = None
    clicked = Signal()

    class DraggableObject(QGraphicsItem, QObject):
        selected_item = None
        clicked = Signal()

    def __init__(self, title: str = "Plot Title", width=780, height=420, margins=QMarginsF(0, 0, 0, 1)):
        super().__init__()
        QObject.__init__(self)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

        # Cache commonly used values - increase title height
        self._height_factor = height * 0.94
        self._title_height = height * 0.06
        
        # Update to use HeaderWidget instead of TitleWidget
        self.header_widget = HeaderWidget(title, width, int(height * 0.06))
        
        # Generate stock data
        x_vals, y_vals = generate_stock_data()
        self.plot_widget = HarmonicPlot(x_vals=x_vals)
        self.header_widget.set_plot_widget(self.plot_widget)
        self.plot_widget.setFixedSize(width, int(self._height_factor))
        self.plot_widget.addNewLines(y_vals, data_label="Stock Price", units="$")

        self.header_proxy = QGraphicsProxyWidget(self)
        self.plot_proxy = QGraphicsProxyWidget(self)

        self.header_proxy.setWidget(self.header_widget)
        self.plot_proxy.setWidget(self.plot_widget)
        self.plot_proxy.setPos(0, self.header_proxy.size().height())

        self.rect = QRectF(0, 0, width, height).marginsRemoved(margins)

        # Connect plot signals to title
        self.plot_widget.mouse_moved_signal.connect(self.header_widget.update_values)

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        if DraggableObject.selected_item == self:
            pen = QPen(QColor(255, 50, 26, 255), 1.0)
        else:
            pen = QPen(QColor(80, 80, 80, 255), 1.0)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        painter.drawRect(self.rect)

    def mousePressEvent(self, event):
        if DraggableObject.selected_item and DraggableObject.selected_item != self:
            DraggableObject.selected_item = None
            
        DraggableObject.selected_item = self
        self.clicked.emit()
        self.update()
        self.scene().update()
        self.setZValue(1)  # Bring selected item to the top
        super().mousePressEvent(event)

class InfiniteCanvas(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(-1000, -1000, 2000, 2000)
        
        # Create multiple charts in a grid layout
        charts = [
            ("Stock Price A", (-800, -400)),
            ("Stock Price B", (-800, 100)),
            ("Stock Price C", (0, -400)),
            ("Stock Price D", (0, 100)),
            ("Stock Price E", (-400, -150))  # Center chart
        ]
        
        # Create each chart with different random data
        for title, position in charts:
            plot = DraggableObject(title=title)
            plot.clicked.connect(self.deselect_all)
            self.addItem(plot)
            plot.setPos(QPointF(*position))
            
            # Generate new random data for each chart
            x_vals, y_vals = generate_stock_data(
                days=365,
                start_price=random.uniform(1, 50),
                end_price=random.uniform(51, 150),
                volatility=random.uniform(0.5, 1.5)
            )
            
            # Add 2-3 lines per chart for additional stress
            plot.plot_widget.x_vals = x_vals
            plot.plot_widget.addNewLines(y_vals, data_label=f"{title} Price")
            plot.plot_widget.addNewLines(y_vals * random.uniform(0.8, 1.2), data_label=f"{title} MA-50")
            if random.random() > 0.5:  # 50% chance of third line
                plot.plot_widget.addNewLines(y_vals * random.uniform(0.9, 1.1), data_label=f"{title} MA-200")

    def deselect_all(self):
        for item in self.items():
            if isinstance(item, DraggableObject):
                item.setZValue(0)  # Reset layer order for all items
                item.update()

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Load custom font using known working method
    path = os.path.join("resources", "OxygenMono-Regular.ttf")
    abs_path = os.path.abspath(path)
    font_id = QFontDatabase.addApplicationFont(abs_path)
    
    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, config.font.size)
        app.setFont(font)
        config.font.family = font_family  # Update config to use loaded font
    else:
        print("Failed to load font")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())