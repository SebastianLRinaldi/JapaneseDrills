from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys

class GridCell(QLabel):
    def __init__(self, char='', preview=False):
        super().__init__(char)
        self.setFont(QFont("Arial", 20))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.setFixedSize(24, 32)
        self.state = None  # None, 'remove', 'mod'
        
        self.setMouseTracking(True)
        # self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        if preview:
            self.setStyleSheet("border: 1px solid gray; color: blue; font-style: italic; padding: 0px; margin: 0px;")
        else:
            self.setStyleSheet("border: 1px solid gray; color: black; padding: 0px; margin: 0px;")


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.toggle_state()
            event.accept()
        else:
            super().mousePressEvent(event)


    def toggle_state(self):
        if self.state is None:
            self.state = 'remove'
            bg_color = '#ffcccc'  # light red background
            text_color = 'black'
        elif self.state == 'remove':
            self.state = 'mod'
            bg_color = '#ccffff'  # light cyan background
            text_color = 'black'
        else:
            self.state = None
            bg_color = ''
            text_color = 'black'
            
        self.setStyleSheet(f"""
            border: 1px solid gray;
            background-color: {bg_color};
            color: {text_color};
        """)