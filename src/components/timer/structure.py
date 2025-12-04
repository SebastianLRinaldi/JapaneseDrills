from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.gui.layout_builder import LayoutBuilder
from .blueprint import Blueprint

class Structure(LayoutBuilder, Blueprint):
    """
    Where you arrange and decorate the widgets
    """

    def __init__(self, component):
        super().__init__()
        
        self._map_widgets(component)
        self.set_widgets()
        
        self.layout_data = [
            self.frame("horizontal",[
                self.toggle_timer_btn,
                self.count_down_label, 
                self.reset_timer_btn,
            ]),
        ]

        self.apply_layout(component, self)


    def set_widgets(self):
        self.toggle_timer_btn.setText("Start")
        self.reset_timer_btn.setText("Reset")
        self.count_down_label.setAlignment(Qt.AlignmentFlag.AlignCenter)


        self.set_widgets_font([
            self.toggle_timer_btn,
            self.reset_timer_btn, 
            self.count_down_label,

        ])


    def set_widgets_font(self, widgets: list[QWidget]):
        font = QFont()
        font.setPointSize(16)  # increase the number to make text bigger
        # font.setBold(True)      # optional, makes text bold
        
        for w in widgets:
            w.setFont(font)








