from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from .blueprint import BluePrint
from src.core.gui.layout_builder import LayoutBuilder

class Structure(LayoutBuilder, BluePrint):
    def __init__(self, component):
        super().__init__()
        self._map_widgets(component)
        self.set_widgets()


        self.layout_data = [
            self.box("vertical", "Apps Widgets", [self.btn1]),

            self.box("vertical", "External App", [self.another_widget]),

            self.box("vertical", "WEB", [self.web_widget]),
        ]

        self.apply_layout(component, self)


    def set_widgets(self):
        self.btn1.setText("Push Me!")
        
