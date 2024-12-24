import numpy as np
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