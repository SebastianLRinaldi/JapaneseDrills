from .Functions import*

class Connections:
    def __init__(self, ui: Layout, logic: Logic):
        self.ui = ui
        self.logic = logic

        self.ui.word_type_combo.currentTextChanged.connect(self.logic.update_labels)
        
        self.ui.good_btn.clicked.connect(self.logic.handle_good)
        self.ui.wrong_btn.clicked.connect(self.logic.handle_wrong)

        self.ui.randomize_btn.clicked.connect(self.logic.randomize)

        self.ui.input_field.textChanged.connect(self.logic.web_app_logic.send_input_to_web)
        
        self.ui.enter_handler.enterPressed.connect(self.handle_enter_pressed)

    def handle_enter_pressed(self):
        text = self.ui.input_field.text().strip()

        if not text:
            self.logic.randomize()
        else:
            self.logic.web_app_logic.enter_text()
            self.ui.input_field.clear()
            self.ui.input_field.setStyleSheet("")
