import os

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
    size: int = 9
    value_label_size: int = 8  # New config for value labels
    color: str = "#FFFFFF"
    weight: int = 400  # Normal weight

@dataclass
class ChartConfig:
    background_color: str = "#2d2b2b"
    grid_color: str = "#404040"
    grid_alpha: float = 0.1
    axis_color: str = "#FFFFFF"
    axis_alpha: float = 1.0
    axis_width: float = 1.0
    antialiasing: bool = True  # Single antialiasing toggle
    enable_grid: bool = True
    line_width: int = 2
    downsampling: bool = True
    clip_to_view: bool = True
    color_palette: List[str] = None
    scatter_size: int = 10
    scatter_dot_size: int = 5  # New parameter for scatter dots
    scatter_opacity: int = 120
    y_axis_units: str = None  # Default unit type for y-axis
    currency_symbol: str = '$'  # Default currency symbol
    value_label_position: float = 0.4  # Position as percentage of header width (0.0 to 1.0)

    def __post_init__(self):
        if self.color_palette is None:
            self.color_palette = [
                '#9C179E', '#BD3786', '#D8576B', '#ED7953', '#FB9F3A',
                '#FECD2A', '#F9E721', '#F5F120', '#E8E621', '#D1EF24'
            ]

@dataclass
class TitleConfig:
    font: FontConfig = None
    margin_factor_width: float = 156.0  # parent_width/156
    margin_factor_height: float = 5.0   # Restore original value
    height_factor: float = 0.06         # Restore original value

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
    disable_antialiasing_optimization: bool = True
    viewport_anchor: str = "mouse"
    default_array_size: int = 100
    downsampling_mode: str = "peak"
    skip_finite_check: bool = True

@dataclass
class GlobalConfig:
    color_scheme: ColorScheme = ColorScheme.DARK
    window_title: str = "Harmonic Plots"
    window_size: tuple = (1200, 800)
    window_position: tuple = (100, 100)
    canvas_size: tuple = (2000, 2000)
    font: FontConfig = None
    chart: ChartConfig = None
    title: TitleConfig = None
    enable_numba: bool = True
    default_chart_size: tuple = (780, 420)
    performance: PerformanceConfig = None

    def __post_init__(self):
        if self.font is None:
            self.font = FontConfig()
        if self.chart is None:
            self.chart = ChartConfig()
        if self.title is None:
            self.title = TitleConfig()
        if self.performance is None:
            self.performance = PerformanceConfig()

# Create default configuration instance
config = GlobalConfig()