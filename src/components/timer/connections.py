from .logic import Logic
from .blueprint import Blueprint

class Connections(Blueprint):
    def __init__(self, component, logic: Logic):
        super().__init__()
        self._map_widgets(component)
        self.logic = logic        

        self.toggle_timer_btn.pressed.connect(self.logic.toggle_timer)
        self.reset_timer_btn.pressed.connect(self.logic.reset_count_down_timer)

