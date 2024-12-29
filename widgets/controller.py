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
        
        # Create container widget for labels
        label_container = QWidget()
        label_container.setFixedHeight(24)  # Fixed height for consistent spacing
        label_layout = QVBoxLayout(label_container)
        label_layout.setContentsMargins(0, 0, 0, 0)
        label_layout.setSpacing(0)
        
        # Initialize context label
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
                opacity: 0;
            }
        """)
        
        # Spacer label
        self.spacer_label = QLabel()
        self.spacer_label.setStyleSheet("background: transparent;")
        
        # Add labels to container
        label_layout.addWidget(self.context_label)
        
        # Command input setup remains the same
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText(config.controller.placeholder_text)
        self.command_input.returnPressed.connect(self.process_command)
        
        # Setup completer
        completer = QCompleter(config.controller.commands)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.command_input.setCompleter(completer)
        
        # Add to main layout
        layout.addWidget(label_container)
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
                self.context_label.setText(command)
                self.context_label.setStyleSheet(f"""
                    QLabel {{
                        color: #ffffff;
                        font-size: 12px;
                        padding: 2px 6px;
                        background-color: {self.get_next_color()};
                        border-radius: 2px;
                        margin-bottom: 2px;
                        opacity: 1;
                    }}
                """)
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
                self.context_label.setText("")  # Clear the text
                self.context_label.setStyleSheet("""
                    QLabel {
                        opacity: 0;
                    }
                """)
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

