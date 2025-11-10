from PyQt6.QtWidgets import QWidget

from .structure import Structure
from .logic import Logic
from .connections import Connections
from .blueprint import Blueprint

class Component(QWidget, Blueprint):
    """
    Has the functionality for start, stop, and reseting a timer
    - you can get the timer value returned as its going
    """
    def __init__(self):
        super().__init__()
        self._init_widgets()
        
        self.structure = Structure(self)
        self.logic = Logic(self)
        self.connection = Connections(self, self.logic)

