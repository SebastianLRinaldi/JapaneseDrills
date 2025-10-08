import random

from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src_old.apps.VocabRanomizer.WordTypeFunctions.AnkiGrabber import AnkiGrabberLogic


from src_old.apps.VocabRanomizer.Layout import Layout


class GrammarLogic(AnkiGrabberLogic):
    def __init__(self, ui: Layout):
        self.ui = ui

    def get_known_grammar_from_anki(self):
        tag = "grammar"
        custom = "notesct>13"
        field_name = "jap_vocab_from_sentence"
        
        note_ids = self.get_notes_with_tag_and_mastery(tag, custom)
        fields_data = self.get_fields(note_ids, field_name)
        cleaned = list(map(self.clean_html, fields_data.values()))
        ruby_removed = list(map(self.remove_anki_ruby, cleaned))
        return ruby_removed 

    def get_grammar(self):
        grammar_points = self.get_known_grammar_from_anki()
        return grammar_points



    def set_grammar(self, grammar_points):
        self.ui.grammar_list.clear()
        self.ui.grammar_list.addItems(grammar_points)


    def update_grammar(self):
        self.fetch_from_anki(self.get_grammar, self.set_grammar)


    def set_random_grammar(self, grammar_points):
        self.ui.grammar_list.clear()
        count = self.ui.count_grammar_spinbox.value()
        count = min(count, len(grammar_points))
        random_grammar = random.sample(grammar_points, count)
        self.ui.grammar_list.addItems(random_grammar)


    def update_grammar_random(self):
        self.fetch_from_anki(self.get_grammar, self.set_random_grammar)









    