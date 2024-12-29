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

    def __init__(self, tab_id: str, name: str = "new canvas", is_home: bool = False, is_add_button: bool = False):
        super().__init__()
        self.tab_id = tab_id
        self.active = False
        self.is_home = is_home
        self.is_add_button = is_add_button
        self.highlight_color = random.choice(config.chart.color_palette) if not is_add_button else None
        self.original_text = name  # Store original text
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0 if is_home else 0, 0, 0, 0)  # Zero left margin for home tab
        layout.setSpacing(0)  # Reduced from 4 to 2

        if is_add_button:
            # Special case for add button tab
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)  # Remove all margins from add button
            self.add_btn = QPushButton("+")
            self.add_btn.setFixedSize(config.canvas_bar.button_size, config.canvas_bar.button_size)
            layout.addWidget(self.add_btn)
            self._apply_base_styles()  # Changed from _apply_add_button_style to _apply_base_styles
        else:
            # Normal tab setup
            self.name_label = QLabel(name)
            #self.name_label.setMinimumWidth(20)  # Minimum width for visibility
            available_width = config.canvas_bar.tab_width - (24 if not is_home else 8)
            self.name_label.setMaximumWidth(available_width)  # Leave space for close button
            # Enable text elision
            self.name_label.setTextFormat(Qt.PlainText)
            self.name_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self._update_elided_text(name)
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

        # Set home tab color explicitly
        if is_home:
            self.highlight_color = "#0066FF"  # Dark blue for home tab

    def _apply_base_styles(self):
        """Apply base styles to the widget based on its type"""
        if self.is_add_button:
            style = f"""
                QWidget {{
                    background: {config.canvas_bar.background_color};
                }}
                QPushButton {{
                    background: {config.canvas_bar.background_color};
                    border: none;
                    color: {config.font.color};
                    font-family: {config.canvas_bar.tab_font_family};
                    font-size: {config.canvas_bar.tab_font_size}px;
                    font-weight: {config.canvas_bar.tab_font_weight};
                    padding: 0;
                }}
                QPushButton:hover {{
                    color: {config.canvas_bar.close_button_hover};
                }}
            """
        else:
            base_style = f"""
                QWidget {{
                    background: transparent;
                    color: {config.font.color};
                    font-family: {config.canvas_bar.tab_font_family};
                    font-size: {config.canvas_bar.tab_font_size}px;
                    font-weight: {config.canvas_bar.tab_font_weight};
                }}
            """
        self.setStyleSheet(style if self.is_add_button else base_style)

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
        
        # Update label with elided text
        metrics = self.name_label.fontMetrics()
        elidedText = metrics.elidedText(text, Qt.ElideRight, self.name_label.maximumWidth())
        self.name_label.setText(elidedText)
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
        if self.is_home:
            if active:
                bg_color = f"rgba(48, 0, 179, 0.5)"  # Dark blue with 50% opacity when active
            else:
                bg_color = config.canvas_bar.background_color  # Same as bar background when inactive
        elif active:
            r = int(self.highlight_color[1:3], 16)
            g = int(self.highlight_color[3:5], 16)
            b = int(self.highlight_color[5:7], 16)
            bg_color = f"rgba({r}, {g}, {b}, {config.canvas_bar.tab_active_opacity})"
        else:
            bg_color = "rgba(0, 0, 0, 0)"
        
        # Force immediate update with complete style refresh
        self.setStyleSheet(f"""
            QWidget {{
                background: {bg_color};
                color: {config.font.color};
                font-size: {config.font.size}px;
            }}
        """)
        self.update()  # Force redraw

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

    def _update_elided_text(self, text: str):
        """Update the label with ... if text is too long"""
        if hasattr(self, 'name_label'):
            metrics = self.name_label.fontMetrics()
            available_width = self.name_label.maximumWidth() - 4
            if metrics.horizontalAdvance(text) > available_width:
                self.name_label.setText("...")
            else:
                self.name_label.setText(text)

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
        # Add color management
        self.available_colors = list(config.chart.color_palette)
        self.used_colors = {}
        self.setFixedHeight(config.canvas_bar.height)
        self.MAX_TABS = config.canvas_bar.max_tabs
        self.TAB_WIDTH = config.canvas_bar.tab_width
        
        # Initialize tabs dict before anything that might use it
        self.tabs = {}
        self.active_tab = None
        
        # Create scroll area for tabs
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)
        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background: {config.canvas_bar.background_color};
                border: none;
            }}
        """)
        
        # Container for tabs
        self.tab_container = QWidget()
        self.tab_layout = QHBoxLayout()
        self.tab_layout.setContentsMargins(0, 0, 0, 0)
        self.tab_layout.setSpacing(0)
        self.tab_layout.addStretch()
        self.tab_container.setLayout(self.tab_layout)
        
        # Add tab container to scroll area
        self.scroll_area.setWidget(self.tab_container)
        
        # Create add button as a special tab
        self.add_tab = CanvasTab("add_button", "+", is_add_button=True)
        self.add_tab.add_btn.clicked.connect(self._on_new_btn_clicked)
        self._update_add_button_state()  # Initial state check
        
        # Create navigation buttons
        self.prev_btn = QPushButton("<")
        self.next_btn = QPushButton(">")
        for btn in (self.prev_btn, self.next_btn):
            btn.setFixedSize(20, config.canvas_bar.button_size)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {config.canvas_bar.background_color};
                    border: none;
                    color: {config.font.color};
                    font-size: 14px;
                    padding: 0;
                }}
                QPushButton:hover {{
                    color: {config.canvas_bar.close_button_hover};
                }}
            """)

        # Connect scroll buttons
        self.prev_btn.clicked.connect(self._scroll_left)
        self.next_btn.clicked.connect(self._scroll_right)
        
        # Create spacer widgets with same background color
        spacer1 = QWidget()
        spacer2 = QWidget()
        spacer3 = QWidget()
        for spacer in (spacer1, spacer2, spacer3):
            spacer.setFixedWidth(5)
            spacer.setStyleSheet(f"background: {config.canvas_bar.background_color};")
        
        # Setup layout with navigation and consistent background color
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)  # No spacing, we'll use our custom spacers
        main_layout.addWidget(self.scroll_area, stretch=1)
        main_layout.addWidget(spacer1)
        main_layout.addWidget(self.prev_btn)
        main_layout.addWidget(self.next_btn)
        main_layout.addWidget(spacer2)
        main_layout.addWidget(self.add_tab)
        main_layout.addWidget(spacer3)
        self.setLayout(main_layout)
        
        self.setStyleSheet(f"""
            QWidget {{
                background: {config.canvas_bar.background_color};
            }}
            QWidget#tab_container {{
                border: none;
            }}
        """)
        
        # Make the tab container have an object name for styling
        self.tab_container.setObjectName("tab_container")
        
        self.tabs = {}
        self.active_tab = None
        
        # Create home tab immediately
        home_id = "home"
        self.addCanvas(home_id, "home", is_home=True)

    def _get_unique_color(self, tab_id: str) -> str:
        """Get a unique color from the palette"""
        if not self.available_colors:
            self.available_colors = list(config.chart.color_palette)
        color = self.available_colors.pop(0)
        self.used_colors[tab_id] = color
        return color

    def _recycle_color(self, tab_id: str):
        """Return a color to the available pool"""
        if tab_id in self.used_colors:
            color = self.used_colors.pop(tab_id)
            self.available_colors.append(color)

    def _on_new_btn_clicked(self):
        """Handle new tab button click"""
        self._counter += 1
        new_id = f"tab_{self._counter}"
        self.addCanvas(new_id)
        # Emit signal after creating the tab
        self.new_canvas_requested.emit()

    def _update_add_button_state(self):
        """Update add button enabled state based on number of tabs"""
        is_enabled = len(self.tabs) < self.MAX_TABS
        self.add_tab.add_btn.setEnabled(is_enabled)
        self.add_tab.add_btn.setStyleSheet(f"""
            QPushButton {{
                background: {config.canvas_bar.background_color};
                border: none;
                color: {config.font.color if is_enabled else '#555555'};
                font-size: 16px;
                padding: 0;
            }}
            QPushButton:hover {{
                color: {config.canvas_bar.close_button_hover if is_enabled else '#555555'};
            }}
        """)

    def addCanvas(self, tab_id: str = None, name: str = "new canvas", is_home: bool = False):
        """Add a new canvas tab"""
        if len(self.tabs) >= self.MAX_TABS:
            return
        # ...existing code...
        if tab_id is None:
            self._counter += 1
            tab_id = f"tab_{self._counter}"  # Generate string ID
            
        tab = CanvasTab(tab_id, name, is_home=is_home)
        tab.highlight_color = self._get_unique_color(tab_id)  # Assign unique color
        tab.setFixedWidth(self.TAB_WIDTH)
        tab.clicked.connect(self._on_tab_clicked)
        tab.renamed.connect(self.canvas_renamed.emit)
        tab.closed.connect(self._on_tab_closed)
        
        # Insert before the stretch
        self.tab_layout.insertWidget(self.tab_layout.count() - 1, tab)
        self.tabs[tab_id] = tab
        
        # Activate the new tab
        self.setActiveCanvas(tab_id)
        self._update_add_button_state()  # Update button state after adding tab

    def _resize_tabs(self):
        """No longer needed since tabs have fixed width"""
        pass

    def _on_tab_closed(self, tab_id: str):
        """Handle tab closure"""
        if tab_id in self.tabs and tab_id != "home":
            self._recycle_color(tab_id)
            tab = self.tabs.pop(tab_id)
            self.tab_layout.removeWidget(tab)
            tab.deleteLater()
            
            # Always activate home tab when closing a tab
            self.setActiveCanvas("home")
            self.canvas_closed.emit(tab_id)
            self._update_add_button_state()  # Update button state after removing tab

    def _on_tab_clicked(self, tab_id: str):
        """Handle tab selection"""
        self.setActiveCanvas(tab_id)
        self.canvas_selected.emit(tab_id)
        
    def setActiveCanvas(self, tab_id: str):
        """Set the active canvas tab"""
        # Deactivate all tabs first
        for tab in self.tabs.values():
            tab.setActive(False)
            
        # Activate the selected tab
        if tab_id in self.tabs:
            self.tabs[tab_id].setActive(True)
            self.active_tab = tab_id
            self.update()  # Force redraw of the widget

    def sizeHint(self):
        # Add size hint for Layer system
        return QSize(self.width(), 25)
        
    def raise_(self):
        # Ensure widget stays on top
        super().raise_()
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

    def _scroll_left(self):
        """Scroll tabs left"""
        current_pos = self.scroll_area.horizontalScrollBar().value()
        new_pos = max(0, current_pos - self.TAB_WIDTH)
        self.scroll_area.horizontalScrollBar().setValue(new_pos)

    def _scroll_right(self):
        """Scroll tabs right"""
        current_pos = self.scroll_area.horizontalScrollBar().value()
        max_pos = self.scroll_area.horizontalScrollBar().maximum()
        new_pos = min(max_pos, current_pos + self.TAB_WIDTH)
        self.scroll_area.horizontalScrollBar().setValue(new_pos)
