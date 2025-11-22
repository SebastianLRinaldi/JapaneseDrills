from .logic import Logic
from .blueprint import Blueprint

class Connections(Blueprint):
    def __init__(self, component, logic: Logic):
        super().__init__()
        self._map_widgets(component)
        self.logic = logic



        self.typing_area.returnPressed.connect(self.logic.make_conjugation)
        self.typing_area.textChanged.connect(self.logic.update_color)

    #     self.word_type_combo.currentTextChanged.connect(self.logic.update_labels)
        
    #     self.good_btn.clicked.connect(self.logic.handle_good)
    #     self.wrong_btn.clicked.connect(self.logic.handle_wrong)

    #     self.randomize_btn.clicked.connect(self.logic.randomize)

    #     # self.input_field.textChanged.connect(self.logic.web_app_logic.send_input_to_web)
        
    #     # self.enter_handler.enterPressed.connect(self.handle_enter_pressed)

    # def handle_enter_pressed(self):
    #     text = self.typing_area.text().strip()

    #     if not text:
    #         self.logic.randomize()
    #     else:
    #         # self.logic.web_app_logic.enter_text()
    #         self.typing_area.clear()
    #         self.typing_area.setStyleSheet("")

