from .logic import Logic
from .blueprint import Blueprint

class Connections(Blueprint):
    def __init__(self, component, logic: Logic):
        super().__init__()
        self._map_widgets(component)
        self.logic = logic



        # self.typing_area.cursorPositionChanged.connect(self.logic.update_line_count)
        # self.typing_area.textChanged.connect(self.logic.update_line_count)

        self.typing_area.returnPressed.connect(self.logic.add_word)
        self.typing_area.textChanged.connect(self.logic.update_color)


        
        self.session_submit_btn.pressed.connect(self.logic.submit_session)

        self.toggle_timer_btn.pressed.connect(self.logic.toggle_timer)
        self.reset_timer_btn.pressed.connect(self.logic.reset_count_down_timer)
        # self.logic.count_down_timer.timeout.connect(self.logic.update_timer)
        # self.logic.count_down_timer.start(1000)  # tick every second

        # self.typing_area.cursorPositionChanged.connect(lambda: print(self.typing_area.textCursor().position()))

