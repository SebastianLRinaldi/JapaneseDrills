from .logic import Logic
from .blueprint import Blueprint

class Connections(Blueprint):
    def __init__(self, component, logic: Logic):
        super().__init__()
        self._map_widgets(component)
        self.logic = logic



        self.typing_area.returnPressed.connect(self.logic.check_conjugation_to_input)
        self.sync_btn.pressed.connect(self.logic.grab_vocab_words)
        self.randomize_btn.pressed.connect(self.logic.next_conjugation)
        self.grade_btn.clicked.connect(self.logic.make_conjugation)

