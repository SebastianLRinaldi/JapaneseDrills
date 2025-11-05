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
            self.box("vertical", "Adjectives", [
                    self.adjective_spinbox,
                    self.adjective_list,
                    self.adjective_set_all_btn,
                    self.adjective_random_btn,
                ]),
        ]

        self.apply_layout(component, self)


    def set_widgets(self):
        self.adjective_set_all_btn.setText("SET ALL ADJECTIVES")
        self.adjective_random_btn.setText("RANDOM ADJECTIVES")
        self.adjective_spinbox.setValue(5)







