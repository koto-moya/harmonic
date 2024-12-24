import numpy as np
import pyqtgraph as pg
import random
from PySide6.QtCore import Signal, QTimer
from PySide6.QtGui import QPainter
from config import config  # Changed to absolute
from utils import find_furthest_color  # Add this import

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
        self.right_vb = pg.ViewBox()
        self.right_axis = None
        self.right_axis_items = {}
        self.right_units = None
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
        
        # Style the grid - keep existing grid styling
        grid_pen = pg.mkPen(color=config.chart.grid_color, alpha=int(255 * config.chart.grid_alpha))
        self.plot_item.showGrid(x=False, y=True, alpha=config.chart.grid_alpha)
        
        # Style the axes - make y-axis fully transparent while keeping x-axis visible
        x_axis_pen = pg.mkPen(
            color=config.chart.axis_color, 
            width=config.chart.axis_width, 
            alpha=int(255 * config.chart.axis_alpha)
        )
        y_axis_pen = pg.mkPen(
            color=config.chart.axis_color, 
            width=config.chart.axis_width, 
            alpha=0  # Set y-axis to fully transparent
        )
        self.plot_item.getAxis('left').setPen(y_axis_pen)
        self.plot_item.getAxis('bottom').setPen(x_axis_pen)
        
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
        self.right_axis = None
        self.right_axis_items = {}  # Track items on right axis
        self.right_units = None     # Track units for right axis

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
            self.units[data_label] = units
            if plot_on_right:
                self.right_axis_items[data_label] = True
                if self.right_units is None:
                    self.right_units = units

        # Select color furthest from existing colors using utility function
        furthest_color = find_furthest_color(config.chart.color_palette, list(self.color_map.values()))
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
            if self.right_axis is None:
                # Initialize right axis setup
                self.right_axis = pg.AxisItem('right')
                self.plot_item.layout.addItem(self.right_axis, 2, 3)
                self.right_axis.linkToView(self.right_vb)
                self.scene().addItem(self.right_vb)
                self.right_vb.setXLink(self.plot_item.vb)
                
                # Match the main viewbox settings
                self.right_vb.setGeometry(self.plot_item.vb.sceneBoundingRect())
                self.right_vb.enableAutoRange(axis='y')
                
                # Style the right axis
                self.right_axis.setPen(pg.mkPen(
                    color=config.chart.axis_color,
                    width=config.chart.axis_width,
                    alpha=0  # Match left axis transparency
                ))
                self.right_axis.setZValue(-1000)
            
            # Add item to right viewbox
            self.right_vb.addItem(line)
            
            # Update axis label
            if units == '$':
                self.right_axis.setLabel(f'Value ({units})', color=config.chart.axis_color)
            else:
                self.right_axis.setLabel(f'Value {units if units else ""}', color=config.chart.axis_color)
        else:
            self.plot_item.addItem(line)
            # Format left axis based on units of first item
            if len(self.plot_info) == 1:
                if units == '$':
                    self.plot_item.getAxis('left').setLabel(f'Value ({units})')
                else:
                    self.plot_item.getAxis('left').setLabel(f'Value {units if units else ""}')

    def _on_mouse_move(self, evt):
        if isinstance(evt, tuple):
            pos = evt[0]
        else:
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
                        
                        # Determine which viewbox to use based on axis
                        if label in self.right_axis_items:
                            vb = self.right_vb
                        else:
                            vb = self.vb
                            
                        # Transform the point to scene coordinates
                        point = vb.mapFromView(pg.Point(self.x_vals[idx], y))
                        scene_point = vb.mapToScene(point)
                        # Transform back to view coordinates of the main viewbox
                        view_point = self.vb.mapSceneToView(scene_point)
                        
                        scatter_points.append({
                            'pos': (view_point.x(), view_point.y()),
                            'brush': pg.mkBrush(self.color_map.get(label, '#FFFFFF'))
                        })
                
                self.scatter.setData(spots=scatter_points)
                
                # Emit values for labels
                values = {
                    label: {
                        'value': data[idx],
                        'units': self.units.get(label),
                        'right_axis': label in self.right_axis_items
                    } 
                    for label, data in self.plot_info.items() 
                    if idx < len(data)
                }
                if values:
                    self.mouse_moved_signal.emit(values)
        else:
            # Clear scatter point when mouse leaves plot
            self.scatter.clear()