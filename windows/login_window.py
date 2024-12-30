from PySide6 import QtWidgets
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIcon
from utils.app_requests import login, Token
from config import config


class LoginWindow(QtWidgets.QWidget):
    login_successful = Signal(Token)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("harmonic login")
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the login window UI elements."""
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 40)  # Reduced top margin from 40 to 20
        layout.setSpacing(20)
        
        # Title
        title = QtWidgets.QLabel("harmonic")
        title.setStyleSheet(f"""
            color: {config.font.color};
            font-size: 24px;
            font-weight: bold;
            font-family: {config.font.family};
        """)
        title.setAlignment(Qt.AlignCenter)
        
        # Username input
        self.le_username = QtWidgets.QLineEdit()
        self.le_username.setPlaceholderText("Username")
        self.le_username.setMinimumHeight(36)  # Add minimum height
        
        # Password input
        self.le_password = QtWidgets.QLineEdit()
        self.le_password.setPlaceholderText("Password")
        self.le_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.le_password.setMinimumHeight(36)  # Add minimum height
        
        # Login button
        self.bt_login = QtWidgets.QPushButton("Login")
        self.bt_login.setCursor(Qt.PointingHandCursor)
        self.bt_login.clicked.connect(self.check_login)
        
        # Error label (hidden by default)
        self.error_label = QtWidgets.QLabel()
        self.error_label.setStyleSheet("color: #ff5555;")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.hide()
        
        # Close button
        close_button = QtWidgets.QPushButton("×")
        close_button.clicked.connect(self.close)
        close_button.setFixedSize(30, 30)
        close_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #666666;
                font-size: 20px;
            }
            QPushButton:hover {
                color: #ff5555;
            }
        """)
        
        # Add widgets to layout
        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)  # Remove header margins
        header_layout.setSpacing(0)  # Remove spacing
        header_layout.addStretch()
        header_layout.addWidget(close_button)
        
        layout.addLayout(header_layout)
        layout.setSpacing(10)  # Reduce spacing between header and title
        
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(self.le_username)
        layout.addWidget(self.le_password)
        layout.addWidget(self.bt_login)
        layout.addWidget(self.error_label)
        layout.addStretch()
        
        # Style the window and widgets
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {config.canvas_bar.background_color};
            }}
            QLineEdit {{
                padding: 0 10px;  /* Horizontal padding only */
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                color: {config.font.color};
                background: #2b2b2b;
                font-size: 13px;
                line-height: 36px;  /* Match the minimum height */
            }}
            QLineEdit:focus {{
                border: 1px solid #666666;
            }}
            QPushButton#bt_login {{
                padding: 10px;
                background-color: {config.draggable.selected_color};
                border: none;
                border-radius: 4px;
                color: white;
                font-size: 14px;
            }}
            QPushButton#bt_login:hover {{
                background-color: #4010e3;
            }}
        """)
        
        # Set object names for specific styling
        self.bt_login.setObjectName("bt_login")
        
    def check_login(self):
        """Handle login attempt with error handling."""
        try:
            username = self.le_username.text()
            password = self.le_password.text()
            
            if not username or not password:
                self.show_error("Please enter both username and password")
                return
            
            token = login(username, password)
            if token:
                # Ensure token is valid before emitting
                if token:
                    self.login_successful.emit(token)
                    return
                self.show_error("Invalid token received")
            else:
                self.show_error("Invalid credentials")
        except Exception as e:
            print(f"Login error: {str(e)}")
            self.show_error("Connection error")
    
    def show_error(self, message):
        """Display error message."""
        self.error_label.setText(message)
        self.error_label.show()
    
    def mousePressEvent(self, event):
        """Enable window dragging."""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Handle window dragging."""
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()