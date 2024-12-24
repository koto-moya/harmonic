from config import chat_interface_html_head
import pyqtgraph as pg
from pyqtgraph.graphicsItems.DateAxisItem import DateAxisItem
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
import numpy as np
from typing import Optional, List
import datetime
import random
import matplotlib.pyplot as plt
from scipy.spatial import distance
from typing import List, Dict, Optional, Tuple
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsWidget, QVBoxLayout, QSizeGrip, QGraphicsLinearLayout
from PySide6.QtCore import QRectF, Qt, QPointF


class DraggableResizablePlot(QGraphicsWidget):
    def __init__(self, plot_widget):
        super().__init__()
        self.proxy_widget = QGraphicsWidget(self)
        self.proxy_widget.isWidget(plot_widget)
        self.plot_widget = plot_widget

        self.layout = QGraphicsLinearLayout(Qt.Vertical)
        self.layout.addItem(self.proxy_widget)
        self.setLayout(self.layout)

        self.setFlags(self.ItemIsMovable | self.ItemIsSelectable | self.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        self.resizing = False
        self.size_grip = QSizeGrip(plot_widget)
        self.size_grip.setVisible(True)

    def hoverMoveEvent(self, event):
        if self.isNearEdge(event.pos()):
            self.setCursor(Qt.SizeFDiagCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
        super().hoverMoveEvent(event)

    def mousePressEvent(self, event):
        if self.isNearEdge(event.pos()):
            self.resizing = True
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.resizing:
            diff = event.pos() - event.lastPos()
            rect = self.rect()
            rect.setWidth(rect.width() + diff.x())
            rect.setHeight(rect.height() + diff.y())
            self.setGeometry(rect)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.resizing = False
        super().mouseReleaseEvent(event)

    def isNearEdge(self, pos):
        edge_threshold = 10
        rect = self.rect()
        return rect.width() - pos.x() < edge_threshold and rect.height() - pos.y() < edge_threshold

def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)  # Remove the item from the layout
        widget = item.widget()  # Get the widget from the item
        if widget:
            widget.deleteLater()  # Delete the widget

def find_widget_position(grid_layout, target_widget):
    for row in range(grid_layout.rowCount()):
        for col in range(grid_layout.columnCount()):
            item = grid_layout.itemAtPosition(row, col)
            if item and item.widget() == target_widget:
                return row, col
    return None  # Widget not found

def rgb_to_tuple(hex_color: str) -> Tuple[int, int, int]:
    return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

def get_furthest_color(existing_colors: List[str], available_colors: List[str]) -> str:
    if not existing_colors:
        return random.choice(available_colors)
    
    existing_rgb: np.ndarray = np.array([rgb_to_tuple(c) for c in existing_colors])
    available_rgb: np.ndarray = np.array([rgb_to_tuple(c) for c in available_colors])

    # Calculate pairwise distances
    dist: np.ndarray = distance.cdist(existing_rgb, available_rgb, metric='euclidean')
    min_distances: np.ndarray = dist.min(axis=0)

    # Select the color with the maximum minimum distance
    furthest_color_index: int = np.argmax(min_distances)
    return available_colors[furthest_color_index]

def create_message(direction, message):
    return f'''<div class="{direction}">{message}</div>'''

def create_chat(formatted_chat_history):
    # print(chat_interface_html_head + "<body>" + formatted_chat_history + "</body>") 
    return chat_interface_html_head + "<body>" + formatted_chat_history + "</div></body>"

def create_first_stream_chunk(new_token):
    # print(f'''<div class="messageincoming">{new_token}</div>''')
    return f'''<div class="messageincoming">{new_token}'''

def create_next_stream_chunk(new_token):
    # print(f'''{new_token}</div>''')
    return f'''{new_token}'''

class CustomDateAxisItem(DateAxisItem):
    def tickStrings(self, values, scale, spacing):
        # Center ticks to midday (12:00 PM)
        return [datetime.datetime.fromtimestamp(value).strftime("%m/%d/%y") for value in values]
    



class HarmonicPlot(pg.PlotWidget):
    def __init__(self, x_vals: Optional[List] = None, enable_mouseover: bool = False, is_datetime: bool = True):
        pg.setConfigOptions(antialias=True) 
        super().__init__()

        self.plot_item = self.getPlotItem()
        self.setBackground('#2d2b2b')

    # Sample 20 evenly spaced values from the colormap
        self.available_colors = [
    '#9C179E',  # Bright purple
    '#BD3786',  # Magenta-pink
    '#D8576B',  # Reddish-pink
    '#ED7953',  # Orange-red
    '#FB9F3A',  # Bright orange
    '#FECD2A',  # Golden yellow
    '#F9E721',  # Yellow
    '#F5F120',  # Bright yellow-green
    '#E8E621',  # Neon green-yellow
    '#D1EF24'   # Yellow-green
]


        self.x_vals = x_vals
        self.plot_info = {}
        self.units = {}
        self.color_map = {}
        self.scatters = {}
        self.vb = self.getViewBox()
        self.is_datetime = is_datetime

        if enable_mouseover:
            self.scene().sigMouseMoved.connect(self.mouse_moved)
        if is_datetime:
            self.date_axis = CustomDateAxisItem(orientation='bottom')

        # Custom tooltip widget
        self.tooltip_widget = QLabel(self)
        self.tooltip_widget.setStyleSheet("""
            QLabel {
                background-color: #2d2b2b;
            }
        """)
        self.tooltip_widget.setWindowFlags(Qt.ToolTip)
        self.tooltip_widget.hide()


    def addNewLines(
        self,
        y_vals: List[float],
        data_label: Optional[str] = None,
        units: Optional[str] = None,
        is_right_axis: bool = False
    ) -> None:

        if data_label:
            self.plot_info[data_label] = y_vals
        if units:
            self.units[data_label] = units

        # Get list of used colors
        used_colors: List[str] = list(self.color_map.values())

        # Select the furthest color
        furthest_color: str = get_furthest_color(used_colors, self.available_colors)
        self.available_colors.remove(furthest_color)
        
        self.color_map[data_label] = furthest_color
        line: pg.PlotDataItem = pg.PlotDataItem(
            self.x_vals,
            y_vals,
            pen=pg.mkPen(color=furthest_color, width=2)
        )
        # if is_right_axis:
        #     right_axis = self.rightAxis()
        #     line.setYLink(right_axis)
        self.addItem(line)

    def render_plot(self):
        self.customYAxis()
        self.finalizePlot()
        self.resize(300, 200)

        # Position the tooltip widget in the top-right corner of the chart
        self.tooltip_widget.move(self.width() - self.tooltip_widget.width() - 10, 10)  # Top-right corner with a 10-pixel margin
        self.tooltip_widget.show()

    def rightAxis(self, is_dollars: bool = False):
        self.customYAxis(is_dollars=is_dollars, orientation = 'right')


    def customYAxis(self, is_dollars: bool = True, orientation: str ='left'):
        self.custom_axis = pg.AxisItem(orientation=orientation)
        max_val = max([max(y_vals) for _, y_vals in self.plot_info.items()])

        # Dynamically scale the number of ticks
        num_ticks = 5
        tick_step = round(max_val / num_ticks, -int(np.floor(np.log10(max_val / num_ticks))))
        tick_values = np.arange(0, max_val + tick_step, tick_step)

        # Generate tick labels
        if is_dollars:
            custom_ticks = [(val, f"${val:,.0f}") for val in tick_values]
        else:
            custom_ticks = [(val, f"{val:,.2f}") for val in tick_values]

        self.custom_axis.setTicks([custom_ticks])
        self.custom_axis.setPen(None)

    def setAxisFormat(self):
        #font = pg.Qt.QtGui.QFont("Roboto", 12)
        self.custom_axis.setStyle(tickLength=-1, showValues=True)
        if self.is_datetime:
            self.date_axis.setStyle(tickLength=-1, showValues=True)

    def finalizePlot(self):
        if self.is_datetime:
            self.setAxisItems({'bottom': self.date_axis, 'left': self.custom_axis})
        else:
            self.setAxisItems({'left': self.custom_axis})
        self.setAxisFormat()
        self.plot_item.showGrid(x=False, y=True)

  
    def clear_tooltip(self):
        # Hide the tooltip widget
        self.tooltip_widget.setText("")
        self.tooltip_widget.adjustSize()

        # Remove scatter points
        if self.scatters:
            for _, v in self.scatters.items():
                self.removeItem(v)
            self.scatters.clear()

    def addScatter(self, y_vals: list, x_vals = None):
        if x_vals == None:
            x_vals = self.x_vals
        scatter = pg.ScatterPlotItem(x_vals, y_vals, pen=None, symbol='o', size=4, brush='#c9d1d9') 
        self.addItem(scatter)
        return scatter
    
    def mouse_moved(self, evt):
        pos = evt
        if self.sceneBoundingRect().contains(pos):
            mouse_point = self.vb.mapSceneToView(pos)

            # Find the closest point index
            index = np.argmin(np.abs(np.array(self.x_vals) - mouse_point.x()))
            if 0 <= index < max([len(y_vals) for _, y_vals in self.plot_info.items()]):
                # Data for the tooltip
                timestamp = datetime.datetime.fromtimestamp(self.x_vals[index]).strftime('%Y-%m-%d')
                values = {data_label: (self.units[data_label], y_vals[index]) for data_label, y_vals in self.plot_info.items()}
            
            # Remove previous scatter points
                if self.scatters:
                    for _, v in self.scatters.items():
                        self.removeItem(v)
                for k, v in self.plot_info.items():
                    self.scatters[k] = self.addScatter([v[index]], x_vals=[self.x_vals[index]])

            # Tooltip text
                values_text = "".join([f"<b style='color: {self.color_map[data_label]}';>{data_label}: {val[0]}{val[1]:,.2f}</b><br>" for data_label, val in values.items()])
                tooltip_text = f"""
                    <b>Date:</b> {timestamp}<br>
                    {values_text}
                """

            # Update the tooltip widget
                self.tooltip_widget.setText(tooltip_text)
                self.tooltip_widget.adjustSize()
            else:
                # Hide the tooltip when the index is out of bounds
                self.tooltip_widget.setText("")
                self.tooltip_widget.adjustSize()
        else:
        # Hide the tooltip when the mouse is outside the scene bounds
            self.tooltip_widget.setText("")
            self.tooltip_widget.adjustSize()
