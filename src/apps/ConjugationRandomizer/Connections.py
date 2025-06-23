from src.apps.ConjugationRandomizer.Functions import*

class Connections:
    def __init__(self, ui: Layout, logic: Logic):
        self.ui = ui
        self.logic = logic

        # Update all buttons
        self.ui.randomize_btn.clicked.connect(self.logic.update_list_random)
        self.ui.get_all_btn.clicked.connect(self.logic.update_lists)

        self.ui.auxiliaries_set_all_btn.clicked.connect(self.logic.set_auxiliaries)
        self.ui.auxiliaries_random_btn.clicked.connect(self.logic.set_auxiliaries_random)

        self.ui.inflections_set_all_btn.clicked.connect(self.logic.set_inflections)
        self.ui.inflections_random_btn.clicked.connect(self.logic.set_inflections_random)

        self.ui.conjugations_set_all_btn.clicked.connect(self.logic.set_conjugations)
        self.ui.conjugations_random_btn.clicked.connect(self.logic.set_conjugations_random)
