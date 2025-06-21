from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.apps.SecondApp.mySecondWindowLayout import SecondLayout

class SecondLogic:
    def __init__(self, ui: SecondLayout):
        self.ui = ui

    def update_widget(self) -> None:
        self.ui.name_label.setText("Set Some Random Text")

    def reset_widget(self) -> None:
        self.ui.name_label.setText("Reset to default")

    
