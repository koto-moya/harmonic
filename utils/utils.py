from typing import List, Tuple, Union
import datetime
import random
import numpy as np
from PySide6.QtGui import QFont
from pyqtgraph.graphicsItems.DateAxisItem import DateAxisItem

from config import config

# Date and Time Utilities
class CustomDateAxisItem(DateAxisItem):
    """Custom date axis formatter for monthly intervals."""
    
    def tickSpacing(self, minVal: float, maxVal: float, size: int) -> List[Tuple[float, int]]:
        """Override to force monthly tick intervals."""
        return [(3600*24*30.5, 0)]  # One month intervals

    def tickStrings(self, values: List[float], scale: float, spacing: float) -> List[str]:
        """Format tick labels to show month names."""
        strings = []
        for value in values:
            try:
                dt = datetime.datetime.fromtimestamp(value)
                strings.append(dt.strftime("%b") if dt.day <= 15 else '')
            except:
                strings.append('')
        return strings

    def tickValues(self, minVal: float, maxVal: float, size: int) -> List[Tuple[float, List[float]]]:
        """Generate ticks for the middle of each month."""
        spacing = self.tickSpacing(minVal, maxVal, size)[0][0]
        start_dt = datetime.datetime.fromtimestamp(minVal)
        end_dt = datetime.datetime.fromtimestamp(maxVal)
        
        if start_dt.day != 1:
            start_dt = (start_dt.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
        
        timestamps = []
        current = start_dt
        while current <= end_dt:
            mid_month = current.replace(day=15)
            timestamps.append(mid_month.timestamp())
            current = (current + datetime.timedelta(days=32)).replace(day=1)
            
        return [(spacing, timestamps)]

# Styling Utilities
def apply_font_style(widget) -> None:
    """Apply global font configuration to a widget."""
    font = QFont(config.font.family)
    font.setPointSize(config.font.size)
    font.setWeight(config.font.weight)
    widget.setFont(font)
    widget.setStyleSheet(f"color: {config.font.color};")

def find_furthest_color(palette: List[str], existing_colors: List[str]) -> str:
    """
    Find the color from palette that's most different from existing colors.
    
    Args:
        palette: List of available colors in hex format
        existing_colors: List of currently used colors in hex format
    
    Returns:
        Hex color string most distant from existing colors
    """
    if not existing_colors:
        return random.choice(palette)
        
    def color_distance(c1: str, c2: str) -> float:
        c1_rgb = tuple(int(c1.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        c2_rgb = tuple(int(c2.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        return sum((a-b)**2 for a, b in zip(c1_rgb, c2_rgb))**0.5
        
    return max(
        palette,
        key=lambda c: min(color_distance(c, ec) for ec in existing_colors)
    )

# Numerical Utilities
def round_to_significant(value: float) -> float:
    """
    Round a number to its first significant digit.
    
    Args:
        value: Number to round
        
    Returns:
        Rounded value
    """
    if value == 0:
        return 0
    magnitude = 10 ** np.floor(np.log10(abs(value)))
    return np.round(value / magnitude) * magnitude

# Data Generation Utilities
def generate_stock_data(
    days: int = 365,
    start_price: float = 1.0,
    end_price: float = 100.0,
    volatility: float = 0.9
) -> Tuple[List[float], np.ndarray]:
    """
    Generate simulated stock price data using geometric Brownian motion.
    
    Args:
        days: Number of days to simulate
        start_price: Initial price
        end_price: Target end price
        volatility: Price volatility factor
    
    Returns:
        Tuple of (timestamps, prices)
    """
    start_date = datetime.datetime(2024, 1, 1)
    timestamps = [(start_date + datetime.timedelta(days=x)).timestamp() for x in range(days)]
    
    t = np.linspace(0, days, days)
    total_return = np.log(end_price / start_price)
    mu = total_return / days + (volatility ** 2) / 2
    
    W = np.random.standard_normal(size=days)
    W = np.cumsum(W) * np.sqrt(1/days)
    
    S = start_price * np.exp((mu - volatility ** 2 / 2) * t + volatility * W)
    return timestamps, np.round(S, 2) * 10000

def generate_fed_rates(
    days: int = 365,
    start_rate: float = 2.0,
    end_rate: float = 5.0,
    volatility: float = 0.3
) -> Tuple[List[float], np.ndarray]:
    """
    Generate simulated Federal Reserve rate data.
    
    Args:
        days: Number of days to simulate
        start_rate: Initial rate
        end_rate: Target end rate
        volatility: Rate volatility factor
    
    Returns:
        Tuple of (timestamps, rates)
    """
    start_date = datetime.datetime(2024, 1, 1)
    timestamps = [(start_date + datetime.timedelta(days=x)).timestamp() for x in range(days)]
    
    t = np.linspace(0, days, days)
    total_change = np.log(end_rate / start_rate)
    mu = total_change / days + (volatility ** 2) / 2
    
    W = np.random.standard_normal(size=days)
    W = np.cumsum(W) * np.sqrt(1/days)
    W = np.convolve(W, np.ones(20)/20, mode='same')
    
    R = start_rate * np.exp((mu - volatility ** 2 / 2) * t + volatility * W)
    return timestamps, np.round(R, 2)