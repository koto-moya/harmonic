from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton
from PySide6.QtCore import Qt, Slot
from models.asset_payload import AssetPayload
from scenes.infinite_canvas import InfiniteCanvas

class Controller(QWidget):
    """Widget for accepting text commands and controlling the canvas."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_canvas = None
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Command input
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Enter command...")
        self.command_input.returnPressed.connect(self.process_command)
        
        # Execute button
        self.execute_btn = QPushButton("Execute")
        self.execute_btn.clicked.connect(self.process_command)
        
        layout.addWidget(self.command_input)
        layout.addWidget(self.execute_btn)
        
        self.setFixedWidth(300)
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #3d3d3d;
                border-radius: 3px;
            }
            QPushButton {
                padding: 5px;
                background-color: #3d3d3d;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
        """)
    
    @Slot()
    def process_command(self):
        """Process the entered command and create appropriate payload."""
        if not self.current_canvas:
            return
            
        command = self.command_input.text().strip()
        if not command:
            return
            
        # Clear input after processing
        self.command_input.clear()
        
        # TODO: Implement command processing
        # For now, just create a dummy chart payload
        payload = AssetPayload(
            type="chart",
            x_values=[],
            data_series=[],
            is_datetime=True
        )
        
        # Pass payload to canvas
        self.execute_payload(payload)
    
    def execute_payload(self, payload: AssetPayload):
        """Execute the payload on the current canvas."""
        if self.current_canvas:
            self.current_canvas.create_draggable_object(
                title="New Object",
                payload=payload
            )
    
    @Slot(InfiniteCanvas)
    def set_current_canvas(self, canvas: InfiniteCanvas):
        """Update the current canvas reference."""
        self.current_canvas = canvas
