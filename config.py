import os
from random import shuffle  # Add at top with other imports

from dataclasses import dataclass
from typing import Dict, List, Optional
from PySide6.QtCore import Qt
from enum import Enum

server_endpoint = "http://192.168.0.150/harmonic"

class ColorScheme(Enum):
    DARK = "dark"
    LIGHT = "light"

@dataclass
class FontConfig:
    path: str = "modules/OxygenMono-Regular.ttf"  # Simplified path that we know works
    family: str = "Arial"  # Default fallback font
    size: int = 11
    value_label_size: int = 10  # New config for value labels
    color: str = "#c9d1d9"
    weight: int = 500  # Normal weight

@dataclass
class ChartConfig:
    background_color: str = "#111111"
    background_opacity: int = 255*.95  # Add new parameter for background opacity (0-255)
    grid_alpha: float = 0.1
    axis_color: str = "#c9d1d9"
    axis_width: float = 1.0
    antialiasing: bool = True  # Single antialiasing toggle
    enable_grid: bool = True
    line_width: int = 2
    downsampling: bool = True
    clip_to_view: bool = True
    color_palette: List[str] = None
    scatter_dot_size: int = 4 # New parameter for scatter dots
    scatter_opacity: int = 120
    y_axis_units: str = None  # Default unit type for y-axis
    currency_symbol: str = '$'  # Default currency symbol
    value_label_position: float = 0.4  # Position as percentage of header width (0.0 to 1.0)
    axis_font_family: str = "Arial"  # New axis font settings
    axis_font_size: int = 10
    axis_font_weight: int = 400
    mouse_tracking_enabled: bool = True  # Enable mouse tracking by default
    
    # Additional mouse-related settings
    scatter_pen: Optional[str] = None  # Pen for scatter points
    scatter_brush_color: tuple = (255, 255, 255)  # White color for scatter points
    scatter_px_mode: bool = True  # Use pixel mode for scatter points
    
    # Viewport settings
    enable_x_mouse: bool = True  # Enable mouse interaction on x-axis
    enable_y_mouse: bool = True  # Enable mouse interaction on y-axis
    auto_range_disabled: bool = True  # Disable auto-range by default
    
    # Axis settings
    axis_z_value: int = -1000  # Z-index for axes
    axis_label_padding: int = 5  # Padding for axis labels
    plot_margins: tuple = (5, 0, 5, 1)  # Plot margins (left, top, right, bottom)

    def __post_init__(self):
        if self.color_palette is None:
            self.color_palette = [
                '#9C179E', '#BD3786', '#D8576B', '#ED7953', '#FB9F3A',
                '#FECD2A', '#F9E721', '#F5F120', '#E8E621', '#D1EF24',  # Original 10
                '#FF0055', '#FF2200', '#FF4C00', '#FF7000', '#FF9400',  # Neon reds/oranges
                '#FFB700', '#FFD500', '#FFFF00', '#CCFF00', '#99FF00',  # Bright yellows/greens
                '#66FF00', '#33FF00', '#00FF00', '#00FF66', '#00FF99',  # Neon greens
                '#00FFFF', '#00CCFF', '#0099FF', '#0066FF', '#3300FF',  # Electric blues
                '#6600FF', '#9900FF', '#CC00FF', '#FF00FF', '#FF00CC',  # Vivid purples/pinks
                '#FF0099', '#FF0077', '#FF0066', '#FF0055', '#E6005C'   # Deep magentas/pinks
            ]
            shuffle(self.color_palette)  # Shuffle the palette on initialization

@dataclass
class TitleConfig:
    font: FontConfig = None
    margin_factor_width: float = 156.0  # parent_width/156
    margin_factor_height: float = 5.0   # Restore original value
    height_factor: float = 0.06         # Restore original value
    background_color: str = "#111111"  # Add header background color
    background_opacity: int = 255  # Add header background opacity (0-255)

    def __post_init__(self):
        if self.font is None:
            self.font = FontConfig()

@dataclass
class PerformanceConfig:
    decimal_precision: int = 2
    ratelimit_mouse: int = 60
    enable_cache: bool = True
    cache_background: bool = True
    smart_viewport_update: bool = False
    disable_antialiasing_optimization: bool = False
    viewport_anchor: str = "mouse"
    default_array_size: int = 100
    downsampling_mode: str = "peak"
    skip_finite_check: bool = True

@dataclass
class CanvasBarConfig:
    height: int = 25
    tab_width: int = 125
    max_tabs: int = 14
    background_color: str = "#111111"
    border_color: str = "#333333"
    
    # Tab specific settings
    tab_background: str = "#111111"
    tab_active_opacity: float = 0.6
    tab_hover_opacity: float = 0.05
    tab_border_radius: str = "4px 4px 0 0"
    tab_font_size: int = 18  # New tab font size
    tab_font_family: str = "Arial"  # New tab font family
    tab_font_weight: int = 400  # New tab font weight
    
    # Button settings
    button_size: int = 30
    button_radius: int = 4
    close_button_size: int = 8
    close_button_hover: str = "#ff5555"
    close_button_style: str = """
        QPushButton {
            background: transparent;
            border: none;
            color: #c9d1d9;
            font-size: 18px;
            font-family: Arial;
            padding: 0;
            margin: 0;
        }
        QPushButton:hover {
            color: #ff5555;
        }
    """

@dataclass
class DraggableConfig:
    selected_color: str = "#3000b3"  # rgb(48, 0, 179)
    unselected_color: str = "#505050"  # rgb(80, 80, 80)
    border_width: float = 1.0
    plot_height_ratio: float = 0.92
    title_height_ratio: float = 0.08
    close_button: dict = None

    def __post_init__(self):
        if self.close_button is None:
            self.close_button = {
                'size': 16,
                'x_offset': 20,
                'y_offset': 4,
                'style': """
                    QPushButton {
                        background: transparent;
                        border: none;
                        color: #c9d1d9;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        color: #ff5555;
                    }
                """
            }

@dataclass
class HeaderConfig:
    # Layout settings
    margin_horizontal_ratio: float = 0.01  # Percent of parent width
    margin_vertical_ratio: float = 0.1  # Percent of parent height
    layout_spacing: int = 5
    grid_horizontal_spacing: int = 5
    grid_vertical_spacing: int = 0
    
    # Title settings
    title_width_ratio: float = 0.25  # Percent of parent width
    title_height_ratio: float = 0.8  # Percent of parent height
    title_alignment: tuple = (Qt.AlignLeft, Qt.AlignVCenter)
    
    # Values container settings
    values_position_ratio: float = 0.3  # Position as percentage of parent width
    label_width_ratio: float = 0.15  # Width as percentage of parent width
    label_height_ratio: float = 0.30  # Height as percentage of parent height
    max_columns: int = 2
    
    # Number formatting
    million_format: str = "{:.2f}M"
    thousand_format: str = "{:.1f}K"
    decimal_format: str = "{:.2f}"
    
    # Label alignment
    static_label_alignment: tuple = (Qt.AlignRight, Qt.AlignVCenter)
    value_label_alignment: tuple = (Qt.AlignLeft, Qt.AlignVCenter)

@dataclass
class ControllerConfig:
    width: int = 300
    margin: int = 10
    position_x_offset: int = 20
    position_y_offset: int = 60
    style: str = """
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QLineEdit {
            padding: 5px;
            border: 1px solid #3d3d3d;
            border-radius: 3px;
        }
    """
    placeholder_text: str = ""
    commands: List[str] = None
    context_label_style: str = """
        QLabel {
            color: #666666;
            font-size: 12px;
            padding: 2px;
        }
    """
    
    def __post_init__(self):
        if self.commands is None:
            self.commands = [
                "/chart",
                "/table",
                "/help",
                "/chat",
            ]

@dataclass
class GlobalConfig:
    color_scheme: ColorScheme = ColorScheme.DARK
    application_title: str = "harmonic"
    canvas_color: str = "#2d2b2b"
    application_size: tuple = (1630, 930)  # Updated default window size
    application_position: tuple = None  # Remove hardcoded position, will be calculated
    canvas_size: tuple = (8000, 8000)
    font: FontConfig = None
    chart: ChartConfig = None
    title: TitleConfig = None
    enable_numba: bool = True
    default_window_size: tuple = (780, 420)
    performance: PerformanceConfig = None
    canvas_bar: CanvasBarConfig = None
    draggable: DraggableConfig = None
    header: HeaderConfig = None
    controller: ControllerConfig = None

    def __post_init__(self):
        if self.font is None:
            self.font = FontConfig()
        if self.chart is None:
            self.chart = ChartConfig()
        if self.title is None:
            self.title = TitleConfig()
        if self.performance is None:
            self.performance = PerformanceConfig()
        if self.canvas_bar is None:
            self.canvas_bar = CanvasBarConfig()
        if self.draggable is None:
            self.draggable = DraggableConfig()
        if self.header is None:
            self.header = HeaderConfig()
        if self.controller is None:
            self.controller = ControllerConfig()

# Create default configuration instance
config = GlobalConfig()