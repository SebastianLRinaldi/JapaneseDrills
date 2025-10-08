from .logic import Logic
from .blueprint import Blueprint

class Connections(Blueprint):
    def __init__(self, component, logic: Logic):
        super().__init__()
        self._map_widgets(component)
        self.logic = logic

        # Noun buttons
        self.noun_set_all_btn.clicked.connect(self.logic.update_words)
        self.noun_random_btn.clicked.connect(self.logic.update_words_random)

