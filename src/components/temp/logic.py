from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

# from src.helpers import *
from .blueprint import Blueprint

class Logic(Blueprint):

    def __init__(self, component):
        self._map_widgets(component)

    def update_widget(self) -> None:
        self.label1.setText("Im on 1, I have been updated by 1!")

    def reset_widget(self) -> None:
        self.label1.setText("Im on 1, I have been reset by 1!")


        
        