import sys
import os
import importlib

from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from .blueprint import Blueprint

class Logic(Blueprint):

    def __init__(self, component: QMainWindow):
        self.component = component
        self._map_widgets(component)
