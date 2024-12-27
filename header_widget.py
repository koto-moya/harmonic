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
        self.margin_h = parent_width * 0.02
        self.margin_v = parent_height * 0.1
        self.header_layout.setContentsMargins(self.margin_h, self.margin_v, self.margin_h, self.margin_v)
        self.header_layout.setSpacing(10)
        
        self.parent_width = parent_width
        self.parent_height = parent_height
        self.setFixedSize(self.parent_width, self.parent_height)
        
        # Title takes 30% of width
        title_width = int(self.parent_width * 0.3)
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
        
        # Calculate position based on config
        values_position = int(self.parent_width * config.chart.value_label_position)
        self.values_container.setFixedWidth(self.parent_width - values_position)
        self.values_container.move(values_position, 0)
        
        self.values_container.setStyleSheet(f"background-color: {bg_color};")
        
        self.header_layout.addWidget(self.values_container)
        
        # Container for value labels
        self.value_labels = {}
        self.connected_widget = None
        self.max_cols = 2  # Number of columns in the grid

    def set_connected_widget(self, plot_widget):
        self.connected_widget = plot_widget

    @Slot(dict)
    def update_values(self, values: dict):
        if not self.connected_widget:
            return
            
        color_map = self.connected_widget.color_map
        label_width = int(self.parent_width * 0.2)
        label_height = int(self.parent_height * 0.4)
        
        # Clear existing labels if number of values changed
        if len(values) != len(self.value_labels):
            for label in self.value_labels.values():
                label.setParent(None)
            self.value_labels.clear()

        # First, handle the first value's x-axis info
        first_key = next(iter(values))
        x_value = values[first_key]['x']
        x_label = values[first_key]['x_axis']
        
        if 'x_axis' not in self.value_labels:
            self.value_labels['x_axis'] = QLabel()
            self.value_labels['x_axis'].setFixedSize(QSize(label_width, label_height))
            self.value_labels['x_axis'].setStyleSheet(f"""
                font-size: {config.font.value_label_size}px;
                background-color: rgba({int(config.title.background_color[1:3], 16)},
                                     {int(config.title.background_color[3:5], 16)},
                                     {int(config.title.background_color[5:7], 16)},
                                     {config.title.background_opacity});
            """)
            self.value_labels['x_axis'].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.values_grid.addWidget(self.value_labels['x_axis'], 0, 0)  # Always top-left
        
        # Format x-axis value
        x_text = f'<span style="color: {config.font.color}">{x_label}: </span>' \
                 f'<span style="color: {config.font.color}">{x_value:.0f}</span>'
        self.value_labels['x_axis'].setText(x_text)
        
        # Now handle the rest of the values, starting from position (0,1)
        for i, (label, data) in enumerate(values.items()):
            value = data['value']
            units = data['units']
            
            if label not in self.value_labels:
                self.value_labels[label] = QLabel()
                self.value_labels[label].setFixedSize(QSize(label_width, label_height))
                self.value_labels[label].setStyleSheet(f"""
                    font-size: {config.font.value_label_size}px;
                    background-color: rgba({int(config.title.background_color[1:3], 16)},
                                         {int(config.title.background_color[3:5], 16)},
                                         {int(config.title.background_color[5:7], 16)},
                                         {config.title.background_opacity});
                """)
                self.value_labels[label].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                
                # Adjust grid positioning to account for x-axis label
                row = (i + 1) % (len(values) // 2 + len(values) % 2)
                col = (i + 1) // (len(values) // 2 + len(values) % 2)
                self.values_grid.addWidget(self.value_labels[label], row, col)
            
            # Format value based on units
            if units == '$':
                formatted_value = f"${value:,.2f}"
            else:
                formatted_value = f"{value:.2f}{units if units else ''}"
            
            # Use HTML to color label and value separately
            color = color_map.get(label, '#FFFFFF')
            self.value_labels[label].setText(
                f'<span style="color: {config.font.color}">{label}: </span>'
                f'<span style="color: {color}">{formatted_value}</span>'
            )