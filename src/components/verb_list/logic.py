from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.helper_classes import WordType
from .blueprint import Blueprint

"""
Close methods
Ctrl+k + Ctrl+0

Open Methods 
Ctrl+k + Ctrl+J
"""
class Logic(WordType, Blueprint):

    def __init__(self, component):
        WordType.__init__(self, component, "verb")
        
        self._map_widgets(component)
        self.component = component
