from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QCompleter, QSizePolicy
from PySide6.QtCore import Qt, Slot
import random
from models.asset_payload import AssetPayload, ChartAssetPayload
from scenes.infinite_canvas import InfiniteCanvas
from widgets.draggable_object import DraggableObject
from config import config
import numpy as np

class Controller(QWidget):
    """Widget for accepting text commands and controlling the canvas."""
    
    def __init__(self, parent=None):
        self.current_color_index = 0  # Add color index tracking
        super().__init__(parent)
        self.current_canvas = None
        self.command_mode = True
        self.current_command = None
        self.setup_ui()
        
    def get_next_color(self) -> str:
        """Get next color from the palette and cycle through."""
        color = config.chart.color_palette[self.current_color_index]
        self.current_color_index = (self.current_color_index + 1) % len(config.chart.color_palette)
        return color

    def setup_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            config.controller.margin,
            config.controller.margin,
            config.controller.margin,
            config.controller.margin
        )
        
        # Initialize empty command context label to reserve space
        self.context_label = QLabel()
        self.context_label.setAlignment(Qt.AlignLeft)
        self.context_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.context_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 12px;
                padding: 2px 6px;
                border-radius: 2px;
                margin-bottom: 2px;
            }
        """)
        self.context_label.hide()
        
        # Spacer label to maintain consistent height
        self.spacer_label = QLabel()
        self.spacer_label.setFixedHeight(self.context_label.sizeHint().height())
        self.spacer_label.setStyleSheet("background: transparent;")
        
        # Command input with completer
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText(config.controller.placeholder_text)
        self.command_input.returnPressed.connect(self.process_command)
        
        # Setup completer
        completer = QCompleter(config.controller.commands)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.command_input.setCompleter(completer)
        
        # Add to layout
        layout.addWidget(self.spacer_label)  # Add spacer first
        layout.addWidget(self.context_label)  # Add label (hidden initially)
        layout.addWidget(self.command_input)
        
        self.setFixedWidth(config.controller.width)
        self.setStyleSheet(config.controller.style)
    
    @Slot()
    def process_command(self):
        """Process the entered command and create appropriate payload."""
        if not self.current_canvas:
            return
        if self.command_mode: 
            command = self.command_input.text().strip()
            self.current_command = command
            if command in config.controller.commands:
            # Set context and show label with random color
                self.context_label.setText(command)
                self.context_label.setStyleSheet(f"""
                    QLabel {{
                        color: #ffffff;
                        font-size: 12px;
                        padding: 2px 6px;
                        background-color: {self.get_next_color()};
                        border-radius: 2px;
                        margin-bottom: 2px;
                    }}
                """)
                self.spacer_label.hide()
                self.context_label.show()
                self.context_label.adjustSize()
                
                self.command_input.clear()
                self.command_input.setPlaceholderText("describe content...")
                self.command_mode = False
        else:
            # Create payload and execute
            if self.current_command == "/chart":
                model_query = self.command_input.text().strip()
                self.current_request = ChartAssetPayload(
                    title="command test",
                    x_values=np.random.rand(10),
                    y_label_left=model_query,
                    y_values_left=[np.random.rand(10)])
                self.execute_payload()
                self.command_input.clear()
                self.command_input.setPlaceholderText(config.controller.placeholder_text)
                self.context_label.hide()
                self.command_mode = True

    def execute_payload(self):
        if self.current_canvas:
           new_window = self.create_draggable_object(self.current_request)
           self.current_canvas.add_window(new_window)

    @Slot(InfiniteCanvas)
    def set_current_canvas(self, canvas: InfiniteCanvas):
        self.current_canvas = canvas

    def create_draggable_object(self, payload: AssetPayload) -> DraggableObject:
        return DraggableObject(payload)

