from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src_old.apps.TextEditor.Layout import Layout
from .widgets.Web.Functions import Logic as webAppLogic

class Logic:
    def __init__(self, ui: Layout):
        self.ui = ui
        self.web_app_logic = webAppLogic(self.ui.web_app)