import re

from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

# from src.helpers import *
from .blueprint import Blueprint

"""
Close methods
Ctrl+k + Ctrl+0

Open Methods 
Ctrl+k + Ctrl+J
"""
class Logic(Blueprint):

    def __init__(self, component):
        super().__init__()
        self._map_widgets(component)
        self.component = component

    def handle_enter_pressed(self):
        self.logic.web_app_logic.enter_text()


    def send_input(self):
        text = self.ui.editor.toPlainText()
        text_stripped = re.sub(r"\[[^\]]*\]", "", text)
        self.logic.web_app_logic.send_input_to_web(text_stripped)
