from PySide6.QtWidgets import (QWidget, QHBoxLayout, QPushButton, 
                             QScrollArea, QSizePolicy, QLineEdit, QGraphicsItem, QLabel)
from PySide6.QtCore import Qt, Signal, QSize
from config import config
import random

class CanvasTab(QWidget):
    """Individual tab in the canvas bar"""
    clicked = Signal(str)  # Change to str to avoid integer overflow
    renamed = Signal(str, str)  # Change first parameter to str
    closed = Signal(str)  # Change to str to avoid integer overflow

    def __init__(self, tab_id: str, name: str = "New Canvas", is_home: bool = False, is_add_button: bool = False):
        super().__init__()
        self.tab_id = tab_id
        self.active = False
        self.is_home = is_home
        self.is_add_button = is_add_button
        self.highlight_color = random.choice(config.chart.color_palette) if not is_add_button else None
        
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 2, 8, 2)
        layout.setSpacing(4)

        if is_add_button:
            # Special case for add button tab
            self.add_btn = QPushButton("+")
            self.add_btn.setFixedSize(config.canvas_bar.button_size, config.canvas_bar.button_size)
            layout.addWidget(self.add_btn)
            self._apply_base_styles()  # Changed from _apply_add_button_style to _apply_base_styles
        else:
            # Normal tab setup
            self.name_label = QLabel(name)
            self._apply_base_styles()
            
            if not is_home:
                self.name_label.mouseDoubleClickEvent = self._label_double_clicked
                
                # Create close button
                self.close_btn = QPushButton("×")
                self.close_btn.setFixedSize(config.canvas_bar.close_button_size, config.canvas_bar.close_button_size)
                self.close_btn.clicked.connect(lambda: self.closed.emit(str(self.tab_id)))
                self._apply_button_styles(self.close_btn)
            
            # Text editor (initially hidden)
            self.name_editor = QLineEdit(name)
            self.name_editor.setStyleSheet(self.name_label.styleSheet().replace('QLabel', 'QLineEdit'))
            self.name_editor.editingFinished.connect(self._convert_to_label)
            self.name_editor.hide()
            
            # Add name label and editor first
            layout.addWidget(self.name_label)
            layout.addWidget(self.name_editor)
            
            # Close button - only add if not home tab, and add it last
            if not is_home:
                self.close_btn = QPushButton("×")
                self.close_btn.setFixedSize(16, 16)  # Fix width to be larger
                self.close_btn.clicked.connect(lambda: self.closed.emit(str(self.tab_id)))  # Make sure to convert to str
                self.close_btn.setStyleSheet(f"""
                    QPushButton {{
                        background: transparent;
                        border: none;
                        color: {config.font.color};
                    }}
                    QPushButton:hover {{
                        color: #ff5555;
                    }}
                """)
                layout.addWidget(self.close_btn)
        
        self.setLayout(layout)
        self._apply_base_styles()

    def _apply_base_styles(self):
        """Apply base styles to the widget based on its type"""
        if self.is_add_button:
            style = f"""
                QWidget {{
                    background: transparent;
                }}
                QPushButton {{
                    color: {config.font.color};
                    font-size: 16px;
                }}
                QPushButton:hover {{
                    background: rgba(255, 255, 255, {config.canvas_bar.tab_hover_opacity});
                }}
            """
            self.setStyleSheet(style)
        else:
            base_style = f"""
                QWidget {{
                    background: {config.canvas_bar.tab_background};
                    border: 1px solid {config.canvas_bar.border_color};
                    border-radius: {config.canvas_bar.tab_border_radius};
                    color: {config.font.color};
                    font-size: {config.font.size}px;
                }}
            """
            self.setStyleSheet(base_style)

    def mousePressEvent(self, event):
        self.clicked.emit(str(self.tab_id))  # Convert to string
        self.setActive(True)
        super().mousePressEvent(event)
        
    def _convert_to_label(self):
        text = self.name_editor.text().strip()
        if not text:
            # Get next available letter if text is empty
            text = CanvasBarWidget._get_next_letter()
            self.name_editor.setText(text)
        
        self.name_label.setText(text)
        self.name_editor.hide()
        self.name_label.show()
        self._on_rename()

    def _label_double_clicked(self, event):
        """Handle double click on label"""
        self.name_editor.setText(self.name_label.text())
        self.name_label.hide()
        self.name_editor.show()
        self.name_editor.setFocus()
        event.accept()

    def _on_rename(self):
        self.renamed.emit(str(self.tab_id), self.name_editor.text())  # Convert to string
        
    def setActive(self, active: bool):
        """Set active state with highlight color"""
        self.active = active
        if active:
            r = int(self.highlight_color[1:3], 16)
            g = int(self.highlight_color[3:5], 16)
            b = int(self.highlight_color[5:7], 16)
            bg_color = f"rgba({r}, {g}, {b}, {config.canvas_bar.tab_active_opacity})"
        else:
            bg_color = config.canvas_bar.tab_background
            
        self.setStyleSheet(self.styleSheet().replace(
            "background:", f"background: {bg_color};"))

    def _apply_button_styles(self, button):
        """Apply styles to buttons"""
        button.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                color: {config.font.color};
            }}
            QPushButton:hover {{
                color: {config.canvas_bar.close_button_hover};
            }}
        """)

class CanvasBarWidget(QWidget):
    # Define all signals at the class level
    new_canvas_requested = Signal()
    canvas_selected = Signal(str)  # Change to str
    canvas_renamed = Signal(str, str)  # Change first parameter to str
    canvas_closed = Signal(str)  # Change to str
    
    _counter = 0  # Add counter for generating unique IDs

    # Add class variable to track last used letter
    _last_letter = ord('A') - 1  # Start with the character before 'A'

    @classmethod
    def _get_next_letter(cls):
        """Get next available letter, wrapping from Z to AA, AB, etc."""
        cls._last_letter += 1
        if cls._last_letter > ord('Z'):
            cls._last_letter = ord('A')
        return chr(cls._last_letter)

    def __init__(self):
        super().__init__()
        self.setFixedHeight(config.canvas_bar.height)
        self.MAX_TABS = config.canvas_bar.max_tabs
        self.TAB_WIDTH = config.canvas_bar.tab_width
        
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Container for tabs (no scroll area)
        self.tab_container = QWidget()
        self.tab_layout = QHBoxLayout()
        self.tab_layout.setContentsMargins(4, 0, 4, 0)
        self.tab_layout.setSpacing(2)
        self.tab_layout.addStretch()
        self.tab_container.setLayout(self.tab_layout)
        
        # Create add button as a special tab
        self.add_tab = CanvasTab("add_button", "+", is_add_button=True)
        self.add_tab.add_btn.clicked.connect(self._on_new_btn_clicked)
        
        # Setup layout directly without scroll area
        main_layout.addWidget(self.tab_container, stretch=1)  # Give tabs area stretch priority
        main_layout.addWidget(self.add_tab)
        self.setLayout(main_layout)
        
        self.setStyleSheet(f"""
            QWidget {{
                background: {config.canvas_bar.background_color};
                border-top: 1px solid {config.canvas_bar.border_color};
            }}
        """)
        
        self.tabs = {}
        self.active_tab = None
        
        # Create home tab immediately
        home_id = "home"
        self.addCanvas(home_id, "Home", is_home=True)

    def _on_new_btn_clicked(self):
        """Handle new tab button click"""
        self._counter += 1
        new_id = f"tab_{self._counter}"
        self.addCanvas(new_id)
        # Emit signal after creating the tab
        self.new_canvas_requested.emit()

    def addCanvas(self, tab_id: str = None, name: str = "New Canvas", is_home: bool = False):
        """Add a new canvas tab"""
        if len(self.tabs) >= self.MAX_TABS:
            return  # Don't add more than MAX_TABS
            
        if tab_id is None:
            self._counter += 1
            tab_id = f"tab_{self._counter}"  # Generate string ID
            
        tab = CanvasTab(tab_id, name, is_home=is_home)
        tab.setFixedWidth(self.TAB_WIDTH)
        tab.clicked.connect(self._on_tab_clicked)
        tab.renamed.connect(self.canvas_renamed.emit)
        tab.closed.connect(self._on_tab_closed)
        
        # Insert before the stretch
        self.tab_layout.insertWidget(self.tab_layout.count() - 1, tab)
        self.tabs[tab_id] = tab
        
        # Activate the new tab
        self.setActiveCanvas(tab_id)

    def _resize_tabs(self):
        """No longer needed since tabs have fixed width"""
        pass

    def resizeEvent(self, event):
        """No longer needs to adjust tab sizes"""
        super().resizeEvent(event)

    def _on_tab_clicked(self, tab_id: str):
        """Handle tab selection"""
        self.setActiveCanvas(tab_id)
        self.canvas_selected.emit(tab_id)
        
    def _on_tab_closed(self, tab_id: str):
        """Handle tab closure"""
        if tab_id in self.tabs and tab_id != "home":  # Prevent closing home tab
            tab = self.tabs.pop(tab_id)
            self.tab_layout.removeWidget(tab)
            tab.deleteLater()
            
            # Always activate home tab when closing a tab
            self.setActiveCanvas("home")
            self.canvas_closed.emit(tab_id)

    def setActiveCanvas(self, tab_id: str):
        """Set the active canvas tab"""
        if self.active_tab and self.active_tab in self.tabs:  # Add safety check
            self.tabs[self.active_tab].setActive(False)
        if tab_id in self.tabs:
            self.tabs[tab_id].setActive(True)
            self.active_tab = tab_id

    def sizeHint(self):
        # Add size hint for Layer system
        return QSize(self.width(), 25)
        
    def raise_(self):
        # Ensure widget stays on top
        super().raise_()
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
