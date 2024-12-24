import numpy as np
import random
import datetime
from PySide6.QtGui import QFont
from pyqtgraph.graphicsItems.DateAxisItem import DateAxisItem
from config import config

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

def find_furthest_color(palette, existing_colors):
    """Find color from palette that's furthest from existing colors."""
    if not existing_colors:
        return random.choice(palette)
        
    def color_distance(c1, c2):
        # Convert hex to RGB
        c1 = tuple(int(c1.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        c2 = tuple(int(c2.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        # Calculate Euclidean distance
        return sum((a-b)**2 for a, b in zip(c1, c2))**0.5
        
    # Find color with maximum minimum distance to existing colors
    return max(
        palette,
        key=lambda c: min(color_distance(c, ec) for ec in existing_colors)
    )