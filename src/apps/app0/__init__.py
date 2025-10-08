from PyQt6.QtWidgets import QWidget

from .structure import Structure
from .logic import Logic
from .connections import Connections
from .blueprint import BluePrint

class Component(QWidget, BluePrint):
    def __init__(self):
        super().__init__()
        self._init_widgets()
        
        self.structure = Structure(self)
        self.logic = Logic(self)
        self.connection = Connections(self, self.logic)

