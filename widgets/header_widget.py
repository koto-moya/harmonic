from typing import Dict, Optional
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QGridLayout,
    QLabel
)
from PySide6.QtCore import Qt, QSize, Slot
from config import config


class HeaderWidget(QWidget):
    """
    A custom header widget that displays a title and dynamic values.
    
    Supports displaying multiple value pairs in a grid layout with configurable styling.
    """

    def __init__(
        self,
        title: str = "Title",
        parent_width: int = 0,
        parent_height: int = 0
    ) -> None:
        """
        Initialize the header widget.

        Args:
            title: Title text to display
            parent_width: Width of parent container
            parent_height: Height of parent container
        """
        super().__init__()
        
        self.parent_width = parent_width
        self.parent_height = parent_height
        self.connected_widget = None
        self.value_labels = {}
        self.static_labels = {}
        self.dynamic_values = {}
        self.max_cols = config.header.max_columns
        
        self._setup_background()
        self._setup_layout()
        self._setup_title(title)
        self._setup_values_container()

    def _setup_background(self) -> None:
        """Configure widget background color."""
        bg_color = (
            f"rgba({int(config.title.background_color[1:3], 16)}, "
            f"{int(config.title.background_color[3:5], 16)}, "
            f"{int(config.title.background_color[5:7], 16)}, "
            f"{config.title.background_opacity})"
        )
        self.setStyleSheet(f"background-color: {bg_color};")
        self.bg_color = bg_color

    def _setup_layout(self) -> None:
        """Configure main layout and margins."""
        self.header_layout = QHBoxLayout(self)
        self.margin_h = self.parent_width * config.header.margin_horizontal_ratio
        self.margin_v = self.parent_height * config.header.margin_vertical_ratio
        self.header_layout.setContentsMargins(
            self.margin_h,
            self.margin_v,
            self.margin_h,
            self.margin_v
        )
        self.header_layout.setSpacing(config.header.layout_spacing)
        self.setFixedSize(self.parent_width, self.parent_height)

    def _setup_title(self, title: str) -> None:
        """
        Configure and add title label.

        Args:
            title: Text to display as title
        """
        title_width = int(self.parent_width * config.header.title_width_ratio)
        self.title_label = QLabel(title)
        self.title_label.setFixedSize(
            QSize(
                title_width,
                int(self.parent_height * config.header.title_height_ratio)
            )
        )
        # Fix: Combine alignment flags with bitwise OR
        self.title_label.setAlignment(
            config.header.title_alignment[0] | config.header.title_alignment[1]
        )
        self.title_label.setStyleSheet(
            f"""
            color: {config.font.color};
            font-size: {config.font.size}px;
            background-color: {self.bg_color};
            """
        )
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch(stretch=1)

    def _setup_values_container(self) -> None:
        """Configure container for value labels."""
        self.values_container = QWidget()
        self.values_grid = QGridLayout(self.values_container)
        self.values_grid.setContentsMargins(0, 0, 0, 0)
        self.values_grid.setSpacing(1)
        self.values_grid.setAlignment(Qt.AlignTop)
        
        values_position = int(self.parent_width * config.header.values_position_ratio)
        self.values_container.setFixedWidth(self.parent_width - values_position)
        self.values_container.move(values_position, 0)
        self.values_container.setStyleSheet(f"background-color: {self.bg_color};")
        
        self.header_layout.addWidget(self.values_container)

    def set_connected_widget(self, plot_widget) -> None:
        """
        Set the plot widget to connect for value updates.

        Args:
            plot_widget: HarmonicPlot instance to connect
        """
        self.connected_widget = plot_widget

    def _create_value_labels(self, values: Dict) -> None:
        """
        Create initial layout with static labels.

        Args:
            values: Dictionary of values to display
        """
        label_width = int(self.parent_width * config.header.label_width_ratio)
        label_height = int(self.parent_height * config.header.label_height_ratio)
        
        for i, (label, data) in enumerate(values.items()):
            if label not in self.static_labels:
                static_label = self._create_static_label(
                    label,
                    label_width,
                    label_height
                )
                value_label = self._create_value_label(
                    label_width,
                    label_height
                )
                
                row = i % (len(values) // 2 + len(values) % 2)
                col = i // (len(values) // 2 + len(values) % 2) * 2
                
                self.values_grid.setHorizontalSpacing(config.header.grid_horizontal_spacing)
                self.values_grid.setVerticalSpacing(config.header.grid_vertical_spacing)
                self.values_grid.addWidget(static_label, row, col)
                self.values_grid.addWidget(value_label, row, col + 1)
                
                self.static_labels[label] = static_label
                self.dynamic_values[label] = value_label

    def _create_static_label(
        self,
        label: str,
        width: int,
        height: int
    ) -> QLabel:
        """Create a static label widget."""
        static_label = QLabel(f"{label}:")
        static_label.setFixedSize(QSize(width // 2, height))
        static_label.setStyleSheet(
            f"""
            font-size: {config.font.value_label_size}px;
            color: {config.font.color};
            background-color: transparent;
            """
        )
        # Fix: Combine alignment flags with bitwise OR
        static_label.setAlignment(
            config.header.static_label_alignment[0] | config.header.static_label_alignment[1]
        )
        return static_label

    def _create_value_label(
        self,
        width: int,
        height: int
    ) -> QLabel:
        """Create a dynamic value label widget."""
        value_label = QLabel()
        value_label.setFixedSize(QSize(width // 2, height))
        value_label.setStyleSheet(
            f"""
            font-size: {config.font.value_label_size}px;
            background-color: transparent;
            """
        )
        # Fix: Combine alignment flags with bitwise OR
        value_label.setAlignment(
            config.header.value_label_alignment[0] | config.header.value_label_alignment[1]
        )
        return value_label

    def _format_number(
        self,
        value: float,
        units: Optional[str] = None
    ) -> str:
        """
        Format numbers with appropriate notation.

        Args:
            value: Number to format
            units: Optional units to append

        Returns:
            Formatted string representation
        """
        if units == '$':
            if value >= 1000000:
                return f"${config.header.million_format.format(value/1000000)}"
            elif value >= 1000:
                return f"${config.header.thousand_format.format(value/1000)}"
            else:
                return f"${config.header.decimal_format.format(value)}"
        else:
            if value >= 1000000:
                return f"{config.header.million_format.format(value/1000000)}{units if units else ''}"
            elif value >= 1000:
                return f"{config.header.thousand_format.format(value/1000)}{units if units else ''}"
            else:
                return f"{config.header.decimal_format.format(value)}{units if units else ''}"

    @Slot(dict)
    def update_values(self, values: Dict) -> None:
        """
        Update displayed values.

        Args:
            values: Dictionary of new values to display
        """
        if not self.connected_widget:
            return
            
        color_map = self.connected_widget.color_map
        
        if not self.static_labels:
            self._create_value_labels(values)
        
        for label, data in values.items():
            if label in self.dynamic_values:
                value = data['value']
                units = data['units']
                formatted_value = self._format_number(value, units)
                color = color_map.get(label, '#FFFFFF')
                
                self.dynamic_values[label].setStyleSheet(
                    f"""
                    font-size: {config.font.value_label_size}px;
                    color: {color};
                    background-color: transparent;
                    """
                )
                self.dynamic_values[label].setText(formatted_value)