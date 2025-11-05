from .logic import Logic
from .blueprint import Blueprint

class Connections(Blueprint):
    def __init__(self, component, logic: Logic):
        self._map_widgets(component)
        self.logic = logic


        self.btn1.clicked.connect(self.logic.update_widget)
        self.btn2.clicked.connect(self.logic.reset_widget)

