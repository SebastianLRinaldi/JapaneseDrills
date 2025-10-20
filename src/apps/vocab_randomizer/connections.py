from .logic import Logic
from .blueprint import BluePrint

class Connections(BluePrint):
    def __init__(self, component, logic: Logic):
        self._map_widgets(component)
        self.logic = logic

        # # Update all buttons
        self.randomize_btn.clicked.connect(self.logic.update_list_random)
        self.get_all_btn.clicked.connect(self.logic.update_lists)

