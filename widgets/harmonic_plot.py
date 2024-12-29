from typing import Dict, List, Optional, Union, Tuple
import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import Signal, QTimer
from PySide6.QtGui import QFont

# Change absolute imports to relative imports
from config import config
from utils.utils import (
    find_furthest_color,
    CustomDateAxisItem,
    round_to_significant
)


class HarmonicPlot(pg.PlotWidget):
    """
    A customized plot widget for displaying harmonic data.
    
    Supports datetime and numerical x-axes, multiple y-axes, and interactive features.
    """
    
    mouse_moved_signal = Signal(dict)

    def __init__(
        self,
        x_vals: Optional[np.ndarray] = None,
        enable_mouseover: bool = config.chart.mouse_tracking_enabled,
        is_datetime: bool = True
    ) -> None:
        """
        Initialize the HarmonicPlot widget.

        Args:
            x_vals: Array of x-axis values
            enable_mouseover: Enable mouse tracking functionality
            is_datetime: Whether x-axis represents datetime values
        """
        axis_items = {'bottom': CustomDateAxisItem(orientation='bottom')} if is_datetime else {}
        super().__init__(axisItems=axis_items)
        
        bg_color = pg.mkColor(config.chart.background_color)
        bg_color.setAlpha(config.chart.background_opacity)
        self.setBackground(bg_color)
        self.available_colors = config.chart.color_palette.copy()
        if x_vals is not None and not is_datetime:
            self.x_vals = np.round(x_vals, config.performance.decimal_precision)
        elif x_vals is not None:
            self.x_vals = x_vals
        if enable_mouseover:
            self.scene().sigMouseMoved.connect(self._on_mouse_move)

        self.scatter = pg.ScatterPlotItem(
            size=config.chart.scatter_dot_size,
            pen=pg.mkPen(config.chart.scatter_pen), 
            brush=pg.mkBrush(*config.chart.scatter_brush_color, config.chart.scatter_opacity),
            pxMode=config.chart.scatter_px_mode
        )


        self.plot_item = self.getPlotItem()
        self.plot_item.showGrid(x=True, y=True, alpha=config.chart.grid_alpha)
        self.plot_item.setClipToView(config.chart.clip_to_view)
        self.plot_item.addItem(self.scatter)
        self.plot_item.getAxis('left').setZValue(config.chart.axis_z_value)
        self.plot_item.getAxis('bottom').setZValue(config.chart.axis_z_value)
        font = QFont(config.font.family, config.font.value_label_size)
        self.plot_item.getAxis('left').setStyle(tickFont=font, tickTextOffset=config.chart.axis_label_padding)
        self.plot_item.getAxis('bottom').setStyle(tickFont=font, tickTextOffset=config.chart.axis_label_padding)
        self.plot_item.layout.setContentsMargins(*config.chart.plot_margins)
        self.vb = self.plot_item.vb
        self.vb.sigResized.connect(self.updateViews)
        self.vb.setMouseEnabled(
            x=config.chart.enable_x_mouse,
            y=config.chart.enable_y_mouse
        )
        self.vb.setLimits(xMin=None, xMax=None, yMin=None, yMax=None)
        if config.chart.auto_range_disabled:
            QTimer.singleShot(0, lambda: self.vb.disableAutoRange())

        self.plot_info = {}
        self.first_plot = True
        self.units = {}
        self.color_map = {}
        self.scatters = {}
        self.left_units = None
        self.right_vb = pg.ViewBox()
        self.right_axis = None
        self.right_axis_items = {}
        self.right_units = None
        self.is_datetime = is_datetime
        self.has_right_axis = False
        self.left_axis = self.plot_item.getAxis('left')
        self.left_axis.enableAutoSIPrefix(False)

        if is_datetime:
            self.plot_item.getAxis('bottom').setLabel('Date')

    def tick_value_loop(
        self,
        values: np.ndarray,
        prefix: str = '',
        suffix: str = ''
    ) -> List[List[Tuple[float, str]]]:
        """
        Format tick values with K/M suffixes.

        Args:
            values: Array of tick values to format
            prefix: String to prepend to tick labels
            suffix: String to append to tick labels

        Returns:
            List containing major and minor tick value pairs
        """
        major_ticks = []
        minor_ticks = []
        
        for val in values:
            if abs(val) >= 1000000:
                text = f"{prefix}{val/1000000:.1f}M {suffix}"
                major_ticks.append((val, text))
            elif abs(val) >= 1000:
                text = f"{prefix}{val/1000:.1f}K {suffix}"
                major_ticks.append((val, text))
            else:
                text = f"{prefix}{int(val)} {suffix}"
                minor_ticks.append((val, text))
                
        return [major_ticks, minor_ticks]


    def format_tick_values(self, values: np.ndarray) -> List[List[Tuple[float, str]]]:
        """
        Apply unit formatting to tick values.

        Args:
            values: Array of values to format

        Returns:
            Formatted tick values with appropriate units
        """
        prefix = ''
        suffix = ''
        if self.left_units:
            if self.left_units == '$':
                prefix = f"{self.left_units} "

            else:
                suffix = f"{self.left_units}"
        return self.tick_value_loop(values, prefix, suffix)        

    def update_axis_ticks(self) -> None:
        """Update axis ticks with formatted values based on current view range."""
        if self.left_axis:
            view_range = self.left_axis.range
            min_val, max_val = view_range
            
            range_size = max_val - min_val
            magnitude = 10 ** np.floor(np.log10(range_size))
            
            if range_size / magnitude >= 5:
                step = magnitude
            elif range_size / magnitude >= 2:
                step = magnitude / 2
            else:
                step = magnitude / 5
            
            start = round_to_significant(min_val - (min_val % step))
            end = round_to_significant(max_val + step)
            tick_values = np.arange(start, end, step)
            
            tick_values = tick_values[(tick_values >= min_val) & (tick_values <= max_val)]
            
            formatted_ticks = self.format_tick_values(tick_values)
            self.left_axis.setTicks(formatted_ticks)
            
            if self.right_axis:
                self.right_axis.setTicks(formatted_ticks)

    def wheelEvent(self, ev) -> None:
        """Handle mouse wheel events for zooming."""
        if self.has_right_axis:
            ev.accept()
            return
            
        if self.plot_item.sceneBoundingRect().contains(ev.position()):
            view_box = self.plot_item.getViewBox()
            delta = ev.angleDelta().y()
            
            if delta != 0:
                scale = 1.01 ** (delta / 20.0)
                view_box.scaleBy(x=scale, y=1.0)
                
            ev.accept()

    def updateViews(self) -> None:
        """Synchronize views between left and right axes."""
        if self.right_vb:
            self.right_vb.setGeometry(self.plot_item.vb.sceneBoundingRect())
            self.right_vb.linkedViewChanged(self.plot_item.vb, self.right_vb.XAxis)
        self.update_axis_ticks()

    def addNewLines(
        self,
        y_vals: np.ndarray,
        x_vals: Optional[np.ndarray] = None,
        data_label: Optional[str] = None,
        units: Optional[str] = None,
        plot_on_right: bool = False
    ) -> None:
        """
        Add new data lines to the plot.

        Args:
            y_vals: Y-axis values to plot
            x_vals: Optional X-axis values
            data_label: Label for the data series
            units: Units for the data series
            plot_on_right: Whether to plot on right axis
        """
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
            else:
                self.left_units = units

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
            self.has_right_axis = True
            self.hideButtons()
            
            if self.right_axis is None:
                self.right_axis = pg.AxisItem('right')
                self.plot_item.layout.addItem(self.right_axis, 2, 3)
                self.right_axis.linkToView(self.right_vb)
                self.scene().addItem(self.right_vb)
                self.right_vb.setXLink(self.plot_item.vb)
                
                self.right_vb.setGeometry(self.plot_item.vb.sceneBoundingRect())
                self.right_vb.enableAutoRange(axis='y')
                
                self.right_axis.setPen(pg.mkPen(
                    color=config.chart.axis_color,
                    width=config.chart.axis_width,
                    alpha=0
                ))
                self.right_axis.setZValue(-1000)
                self.right_axis.setLabel('')
            
            self.vb.setMouseEnabled(x=False, y=False)
            self.right_vb.setMouseEnabled(x=False, y=False)
            
            self.right_vb.addItem(line)
            
        else:
            self.plot_item.addItem(line)
            if len(self.plot_info) == 1:
                self.plot_item.getAxis('left').setLabel('')
        
        self.update_axis_ticks()

    def _on_mouse_move(self, evt) -> None:
        """
        Handle mouse movement events for hover effects.

        Args:
            evt: Mouse event data
        """
        if isinstance(evt, tuple):
            pos = evt[0]
        else:
            pos = evt
            
        if self.sceneBoundingRect().contains(pos):
            mouse_point = self.plotItem.vb.mapSceneToView(pos)
            mouse_x = mouse_point.x()
            
            if self.x_vals is not None and len(self.x_vals) > 0:
                idx = min(range(len(self.x_vals)), 
                         key=lambda i: abs(self.x_vals[i] - mouse_x))
                
                scatter_points = []
                for label, data in self.plot_info.items():
                    if idx < len(data):
                        y = float(data[idx])
                        
                        if label in self.right_axis_items:
                            vb = self.right_vb
                        else:
                            vb = self.vb
                            
                        point = vb.mapFromView(pg.Point(self.x_vals[idx], y))
                        scene_point = vb.mapToScene(point)
                        view_point = self.vb.mapSceneToView(scene_point)
                        
                        scatter_points.append({
                            'pos': (view_point.x(), view_point.y()),
                            'brush': pg.mkBrush(self.color_map.get(label, '#FFFFFF'))
                        })
                
                self.scatter.setData(spots=scatter_points)
                
                values = {
                    label: {
                        'value': data[idx],
                        'units': self.units.get(label),
                        'right_axis': label in self.right_axis_items,
                        'x': self.x_vals[idx],
                        'x_axis': 'date' if self.is_datetime else 'index'
                    } 
                    for label, data in self.plot_info.items() 
                    if idx < len(data)
                }
                if values:
                    self.mouse_moved_signal.emit(values)
        else:
            self.scatter.clear()