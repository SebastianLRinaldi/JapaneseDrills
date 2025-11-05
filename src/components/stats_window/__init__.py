from PyQt6.QtWidgets import QDialog

from .structure import Structure
from .logic import Logic
from .connections import Connections
from .blueprint import Blueprint

class Component(QDialog, Blueprint):
    """
    Shows stats comparing current and prev free recall session
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_widgets(self)
        
        self.structure = Structure(self)
        self.logic = Logic(self)
        self.connection = Connections(self, self.logic)

    def resizeEvent(self, event):
        print(f"Window resized: width={self.width()}, height={self.height()}")
        super().resizeEvent(event)

