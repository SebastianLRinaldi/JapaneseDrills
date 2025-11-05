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
            self.splitter("horizontal", [
                self.noun_list,
                self.verb_list,
                self.adjective_list,
                self.adverb_list,
            ]),
            
            self.group("vertical", [
                "get_all_btn",
                "randomize_btn"
            ])
        ]

        self.apply_layout(component, self)

    def set_widgets(self):
        self.get_all_btn.setText("SET ALL")
        self.randomize_btn.setText("RANDOMIZE ALL")

        
