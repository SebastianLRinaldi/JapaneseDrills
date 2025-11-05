from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src_old.apps.ConjugationGrid.Layout import Layout

class Logic:
    def __init__(self, ui: Layout):
        self.ui = ui

    def update_widget(self) -> None:
        self.ui.name_label.setText("Set Some Random Text")

    def reset_widget(self) -> None:
        self.ui.name_label.setText("Reset to default")

    
