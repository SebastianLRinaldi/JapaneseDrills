from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

# from src.helpers import *
from .blueprint import Blueprint

class Logic(Blueprint):

    def __init__(self, component):
        super().__init__()
        self._map_widgets(component)

    def somefunction(self):
        print("HI")

    # def update_widget(self) -> None:
    #     self.ui.name_label.setText("Set Some Random Text")

    # def reset_widget(self) -> None:
    #     self.ui.name_label.setText("Reset to default")

    
