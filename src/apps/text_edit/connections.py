from .logic import Logic
from .blueprint import Blueprint

class Connections(Blueprint):
    def __init__(self, component, logic: Logic):
        super().__init__()
        self._map_widgets(component)
        self.logic = logic

        # self.ui.editor.textChanged.connect(self.send_input)
        
        # self.ui.enter_handler.enterPressed.connect(self.handle_enter_pressed)


