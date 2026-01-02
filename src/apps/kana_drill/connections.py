from .logic import Logic
from .blueprint import Blueprint

from src.globals.global_signals import global_signal_manager

class Connections(Blueprint):
    def __init__(self, component, logic: Logic):
        super().__init__()
        self._map_widgets(component)
        self.logic = logic
        self.logic.start_handler.startPressed.connect(self.logic.toggle_session)
        self.script_combo.currentIndexChanged.connect(self.logic.get_selected_kana)
        self.word_type_combo.currentIndexChanged.connect(self.logic.get_selected_kana)
        self.vowel_selector.itemSelectionChanged.connect(self.logic.get_selected_kana)

