from application.apps.VocabRanomizer.Functions import*

class VocabRandomizerConnections:
    def __init__(self, ui: VocabRandomizerLayout, logic: VocabRandomizerLogic):
        self.ui = ui
        self.logic = logic

        self.ui.randomize_btn.clicked.connect(self.logic.update_list_random)
        self.ui.sync_btn.clicked.connect(self.logic.update_lists)