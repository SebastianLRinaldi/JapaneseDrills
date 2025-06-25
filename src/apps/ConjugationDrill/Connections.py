from .Functions import*

class Connections:
    def __init__(self, ui: Layout, logic: Logic):
        self.ui = ui
        self.logic = logic

        self.ui.word_type_combo.currentTextChanged.connect(self.logic.update_labels)
        
        self.ui.good_btn.clicked.connect(self.logic.handle_good)
        self.ui.wrong_btn.clicked.connect(self.logic.handle_wrong)

        self.ui.randomize_btn.clicked.connect(self.logic.randomize)