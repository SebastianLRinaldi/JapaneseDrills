from src.apps.VocabRanomizer.Functions import*

class Connections:
    def __init__(self, ui: Layout, logic: Logic):
        self.ui = ui
        self.logic = logic

        # Update all buttons
        self.ui.randomize_btn.clicked.connect(self.logic.update_list_random)
        self.ui.get_all_btn.clicked.connect(self.logic.update_lists)

        # Grammar buttons
        self.ui.grammar_set_all_btn.clicked.connect(self.logic.grammar_logic.update_grammar)
        self.ui.grammar_random_btn.clicked.connect(self.logic.grammar_logic.update_grammar_random)

        # Noun buttons
        self.ui.noun_set_all_btn.clicked.connect(self.logic.nouns_logic.update_nouns)
        self.ui.noun_random_btn.clicked.connect(self.logic.nouns_logic.update_nouns_random)

        # Verb buttons
        self.ui.verb_set_all_btn.clicked.connect(self.logic.verbs_logic.update_verbs)
        self.ui.verb_random_btn.clicked.connect(self.logic.verbs_logic.update_verbs_random)