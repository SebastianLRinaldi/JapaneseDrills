from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.apps.TextEditor.Layout import Layout

class Logic:
    def __init__(self, ui: Layout):
        self.ui = ui