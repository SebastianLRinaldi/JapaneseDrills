import re

from src.apps.TextEditor.Functions import*

class Connections:
    def __init__(self, ui: Layout, logic: Logic):
        self.ui = ui
        self.logic = logic


        self.ui.editor.textChanged.connect(self.send_input)
        
        self.ui.enter_handler.enterPressed.connect(self.handle_enter_pressed)

    def handle_enter_pressed(self):
        self.logic.web_app_logic.enter_text()


    def send_input(self):
        text = self.ui.editor.toPlainText()
        text_stripped = re.sub(r"\[[^\]]*\]", "", text)
        self.logic.web_app_logic.send_input_to_web(text_stripped)
