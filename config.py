import os
from random import shuffle  # Add at top with other imports

from dataclasses import dataclass
from typing import Dict, List, Optional
from PySide6.QtCore import Qt
from enum import Enum

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
    smart_viewport_update: bool = True
    disable_antialiasing_optimization: bool = False
    viewport_anchor: str = "mouse"
    default_array_size: int = 100
    downsampling_mode: str = "peak"
    skip_finite_check: bool = True

@dataclass
class CanvasBarConfig:
    height: int = 25
    tab_width: int = 125
    max_tabs: int = 12
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

@dataclass
class GlobalConfig:
    color_scheme: ColorScheme = ColorScheme.DARK
    application_title: str = "Harmonic Plots"
    canvas_color: str = "#2d2b2b"
    application_size: tuple = (1920, 1080)
    application_position: tuple = (100, 100)
    canvas_size: tuple = (2000, 2000)
    font: FontConfig = None
    chart: ChartConfig = None
    title: TitleConfig = None
    enable_numba: bool = True
    default_window_size: tuple = (569, 320)
    performance: PerformanceConfig = None
    canvas_bar: CanvasBarConfig = None

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

# Create default configuration instance
config = GlobalConfig()