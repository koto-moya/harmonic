import numpy as np
import random
import datetime
from PySide6.QtGui import QFont
from pyqtgraph.graphicsItems.DateAxisItem import DateAxisItem
from config import config

# def create_message(direction, message):
#     return f'''<div class="{direction}">{message}</div>'''

# def create_chat(formatted_chat_history):
#     # print(chat_interface_html_head + "<body>" + formatted_chat_history + "</body>") 
#     return chat_interface_html_head + "<body>" + formatted_chat_history + "</div></body>"

# def create_first_stream_chunk(new_token):
#     # print(f'''<div class="messageincoming">{new_token}</div>''')
#     return f'''<div class="messageincoming">{new_token}'''

# def create_next_stream_chunk(new_token):
#     # print(f'''{new_token}</div>''')
#     return f'''{new_token}'''

# class CustomDateAxisItem(DateAxisItem):
#     def tickStrings(self, values, scale, spacing):
#         # Center ticks to midday (12:00 PM)
#         return [datetime.datetime.fromtimestamp(value).strftime("%m/%d/%y") for value in values]
    

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

def generate_fed_rates(days=365, start_rate=2.0, end_rate=5.0, volatility=0.3):
    """Generate simulated Fed rate data with less volatility than stock prices"""
    t = np.linspace(0, days, days)
    total_change = np.log(end_rate / start_rate)
    mu = total_change / days + (volatility ** 2) / 2
    
    # Generate smoother random walk for rates
    W = np.random.standard_normal(size=days)
    W = np.cumsum(W) * np.sqrt(1/days)
    W = np.convolve(W, np.ones(20)/20, mode='same')  # Smooth the data
    
    # Calculate rate path
    R = start_rate * np.exp((mu - volatility ** 2 / 2) * t + volatility * W)
    return t, np.round(R, 2)

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