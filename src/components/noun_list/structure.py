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
            self.box("vertical", "Nouns", [
                    self.noun_spinbox,
                    self.noun_list,
                    self.noun_set_all_btn,
                    self.noun_random_btn,
                ]),
        ]

        self.apply_layout(component, self)


    def set_widgets(self):
        self.noun_set_all_btn.setText("SET ALL NOUNS")
        self.noun_random_btn.setText("RANDOM NOUNS")
        self.noun_spinbox.setValue(5)







