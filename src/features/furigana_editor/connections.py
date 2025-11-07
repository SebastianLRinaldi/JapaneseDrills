from .logic import Logic
from .blueprint import Blueprint

class Connections(Blueprint):
    def __init__(self, component, logic: Logic):
        super().__init__()
        self._map_widgets(component)
        self.logic = logic


        
        self.logic.undo_handler.undoPressed.connect(self.logic.remove_word_from_history)
        self.typing_area.returnPressed.connect(self.logic.add_word)


        """
        Want to figure out which would be best as teh signal
        """
        self.typing_area.textChanged.connect(self.logic.update_color)
        
        # self.typing_area.selectionChanged.connect(self.logic.update_color)
        # self.typing_area.editingFinished.connect(self.logic.update_color)
        # self.typing_area.returnPressed.connect(self.logic.update_color)
        # self.typing_area.cursorPositionChanged.connect(self.logic.update_color)
        # self.typing_area.textEdited.connect(self.logic.update_color)







        


        
        self.session_submit_btn.pressed.connect(self.logic.submit_session)

        self.toggle_timer_btn.pressed.connect(self.logic.toggle_timer)
        self.reset_timer_btn.pressed.connect(self.logic.reset_count_down_timer)
 

