import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import Signal, QTimer
from PySide6.QtGui import QFont
from config import config  # Changed to absolute
from utils.utils import find_furthest_color  # Add this import

class HarmonicPlot(pg.PlotWidget):
    mouse_moved_signal = Signal(dict)  # Signal to emit {label: value} pairs

    def __init__(self, x_vals=None, enable_mouseover=False, is_datetime=True):
        super().__init__()
        bg_color = pg.mkColor(config.chart.background_color)
        bg_color.setAlpha(config.chart.background_opacity)
        self.setBackground(bg_color)
        self.available_colors = config.chart.color_palette.copy()
        if x_vals is not None and not is_datetime:
            self.x_vals = np.round(x_vals, config.performance.decimal_precision)
        if enable_mouseover:
            self.scene().sigMouseMoved.connect(self._on_mouse_move)

        self.scatter = pg.ScatterPlotItem(
            size=config.chart.scatter_dot_size,  # Use new scatter_dot_size parameter
            pen=pg.mkPen(None), 
            brush=pg.mkBrush(255, 255, 255, config.chart.scatter_opacity),
            pxMode=True
        )


        self.plot_item = self.getPlotItem()
        self.plot_item.showGrid(x=True, y=True, alpha=config.chart.grid_alpha)
        self.plot_item.setClipToView(config.chart.clip_to_view)  # Only render visible data
        self.plot_item.addItem(self.scatter)
        self.plot_item.getAxis('left').setZValue(-1000)
        self.plot_item.getAxis('bottom').setZValue(-1000)
        font = QFont(config.font.family, config.font.value_label_size)
        self.plot_item.getAxis('left').setStyle(tickFont=font, tickTextOffset=5)
        self.plot_item.getAxis('bottom').setStyle(tickFont=font, tickTextOffset=5)
        self.plot_item.layout.setContentsMargins(5, 0, 5, 1)
        self.vb = self.plot_item.vb  # Main ViewBox
        self.vb.sigResized.connect(self.updateViews)
        self.vb.setMouseEnabled(x=True, y=True)
        self.vb.setLimits(xMin=None, xMax=None, yMin=None, yMax=None)
        QTimer.singleShot(0, lambda: self.vb.disableAutoRange())

        self.plot_info = {}
        self.first_plot = True # Add flag to track first plot for axis label
        self.units = {}
        self.color_map = {}
        self.scatters = {}
        self.right_vb = pg.ViewBox()
        self.right_axis = None
        self.right_axis_items = {}
        self.right_units = None
        self.is_datetime = is_datetime
        self.has_right_axis = False  # Add flag to track right axis presence
        
    def wheelEvent(self, ev):
        # Ignore wheel events if there's a right axis
        if self.has_right_axis:
            ev.accept()
            return
            
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

    def addNewLines(self, y_vals, x_vals=None, data_label=None, units=None, plot_on_right=False):
        # Round y_vals to configured precision
        y_vals = np.round(y_vals, config.performance.decimal_precision)

        if self.x_vals is None:
            raise ValueError("x_vals must be set before adding new lines")
        if self.first_plot:
            self.first_plot = False
            self.plot_item.getAxis('bottom').setLabel('date' if self.is_datetime else 'Index')
        
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
            self.has_right_axis = True  # Set flag when right axis is added
            # Hide the auto-range button when we have a right axis
            self.hideButtons()
            
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
                    alpha=0  # Make right axis transparent
                ))
                self.right_axis.setZValue(-1000)
            
            # Lock both viewboxes when right axis exists
            self.vb.setMouseEnabled(x=False, y=False)
            self.right_vb.setMouseEnabled(x=False, y=False)
            
            # Add item to right viewbox
            self.right_vb.addItem(line)
            
            # Update axis label
            if units == '$':
                self.right_axis.setLabel(f'{units}', color=config.chart.axis_color)
            else:
                self.right_axis.setLabel(f'{units if units else ""}', color=config.chart.axis_color)
        else:
            self.plot_item.addItem(line)
            # Format left axis based on units of first item
            if len(self.plot_info) == 1:
                if units == '$':
                    self.plot_item.getAxis('left').setLabel(f'({units})')
                else:
                    self.plot_item.getAxis('left').setLabel(f'{units if units else ""}')

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
                        'right_axis': label in self.right_axis_items,
                        'x': self.x_vals[idx],
                        'x_axis': 'date' if self.is_datetime else 'Index'
                    } 
                    for label, data in self.plot_info.items() 
                    if idx < len(data)
                }
                if values:
                    self.mouse_moved_signal.emit(values)
        else:
            # Clear scatter point when mouse leaves plot
            self.scatter.clear()