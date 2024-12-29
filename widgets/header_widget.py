from PySide6.QtWidgets import QWidget, QHBoxLayout, QGridLayout, QLabel, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QSize, Slot
from PySide6.QtGui import QColor
from config import config  # Changed from relative to absolute

class HeaderWidget(QWidget):
    def __init__(self, title: str = "Title", parent_width: int = 0, parent_height: int = 0):
        super().__init__()
        
        # Set background for the main widget
        bg_color = f"rgba({int(config.title.background_color[1:3], 16)}, \
                         {int(config.title.background_color[3:5], 16)}, \
                         {int(config.title.background_color[5:7], 16)}, \
                         {config.title.background_opacity})"
        self.setStyleSheet(f"background-color: {bg_color};")
        
        # Main horizontal layout
        self.header_layout = QHBoxLayout(self)
        self.margin_h = parent_width * 0.01  # Reduce horizontal margin (was 0.02)
        self.margin_v = parent_height * 0.1
        self.header_layout.setContentsMargins(self.margin_h, self.margin_v, self.margin_h, self.margin_v)
        self.header_layout.setSpacing(5)  # Reduce spacing between title and values (was 10)
        
        self.parent_width = parent_width
        self.parent_height = parent_height
        self.setFixedSize(self.parent_width, self.parent_height)
        
        # Title takes 25% of width (was 30%)
        title_width = int(self.parent_width * 0.25)
        self.title_label = QLabel(title)
        self.title_label.setFixedSize(QSize(title_width, int(self.parent_height * 0.8)))
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.title_label.setStyleSheet(f"""
            color: {config.font.color};
            font-size: {config.font.size}px;
            background-color: {bg_color};
        """)
        self.header_layout.addWidget(self.title_label)
        
        # Flexible spacer
        self.header_layout.addStretch(stretch=1)
        
        # Values container with grid layout - modified alignment and position
        self.values_container = QWidget()
        self.values_grid = QGridLayout(self.values_container)
        self.values_grid.setContentsMargins(0, 0, 0, 0)
        self.values_grid.setSpacing(1)
        self.values_grid.setAlignment(Qt.AlignTop)  # Align to top
        
        # Calculate position based on config - move values closer
        values_position = int(self.parent_width * 0.3)  # Fixed position instead of using config
        self.values_container.setFixedWidth(self.parent_width - values_position)
        self.values_container.move(values_position, 0)
        
        self.values_container.setStyleSheet(f"background-color: {bg_color};")
        
        self.header_layout.addWidget(self.values_container)
        
        # Container for value labels
        self.value_labels = {}
        self.connected_widget = None
        self.max_cols = 2  # Number of columns in the grid
        self.static_labels = {}  # Store the static labels
        self.dynamic_values = {}  # Store the value labels

    def set_connected_widget(self, plot_widget):
        self.connected_widget = plot_widget

    def _create_value_labels(self, values):
        """Create initial layout with static labels"""
        label_width = int(self.parent_width * 0.15)  # Reduced from 0.2
        label_height = int(self.parent_height * 0.30)  # Reduced from 0.4
        
        for i, (label, data) in enumerate(values.items()):
            if label not in self.static_labels:
                # Create static label
                static_label = QLabel(f"{label}:")
                static_label.setFixedSize(QSize(label_width // 2, label_height))
                static_label.setStyleSheet(f"""
                    font-size: {config.font.value_label_size}px;
                    color: {config.font.color};
                    background-color: transparent;
                """)
                static_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                
                # Create dynamic value label
                value_label = QLabel()
                value_label.setFixedSize(QSize(label_width // 2, label_height))
                value_label.setStyleSheet(f"""
                    font-size: {config.font.value_label_size}px;
                    background-color: transparent;
                """)
                value_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                
                # Calculate grid position
                row = i % (len(values) // 2 + len(values) % 2)
                col = i // (len(values) // 2 + len(values) % 2) * 2  # Multiply by 2 for label-value pairs
                
                # Add to grid with smaller spacing
                self.values_grid.setHorizontalSpacing(5)  # Add small horizontal spacing
                self.values_grid.setVerticalSpacing(0)    # Remove vertical spacing
                self.values_grid.addWidget(static_label, row, col)
                self.values_grid.addWidget(value_label, row, col + 1)
                
                self.static_labels[label] = static_label
                self.dynamic_values[label] = value_label

    def _format_number(self, value: float, units: str = None) -> str:
        """Format numbers with appropriate notation based on size"""
        if units == '$':
            if value >= 1000000:
                return f"${value/1000000:.2f}M"
            elif value >= 1000:
                return f"${value/1000:.1f}K"
            else:
                return f"${value:.2f}"
        else:
            if value >= 1000000:
                return f"{value/1000000:.2f}M{units if units else ''}"
            elif value >= 1000:
                return f"{value/1000:.1f}K{units if units else ''}"
            else:
                return f"{value:.2f}{units if units else ''}"

    @Slot(dict)
    def update_values(self, values: dict):
        if not self.connected_widget:
            return
            
        color_map = self.connected_widget.color_map
        
        # Create labels if they don't exist
        if not self.static_labels:
            self._create_value_labels(values)
        
        # Update only the values
        for label, data in values.items():
            if label in self.dynamic_values:
                value = data['value']
                units = data['units']
                formatted_value = self._format_number(value, units)
                color = color_map.get(label, '#FFFFFF')
                
                self.dynamic_values[label].setStyleSheet(f"""
                    font-size: {config.font.value_label_size}px;
                    color: {color};
                    background-color: transparent;
                """)
                self.dynamic_values[label].setText(formatted_value)