from .logic import Logic
from .blueprint import BluePrint

class Connections(BluePrint):
    def __init__(self, component, logic: Logic):
        self._map_widgets(component)
        self.logic = logic

