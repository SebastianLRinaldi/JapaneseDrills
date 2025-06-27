import requests
import re
import html
import random

from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *


from src.apps.VocabRanomizer.WordTypeFunctions.AnkiGrabber import AnkiGrabberLogic


from src.apps.VocabRanomizer.Layout import Layout

class AdjectivesLogic(AnkiGrabberLogic):
    def __init__(self, ui: Layout):
        self.ui = ui


    def get_known_adjectives_from_anki(self):
        tag = "adjective"
        custom = "notesct>13"
        field_name = "jap_vocab_from_sentence"

        note_ids = self.get_notes_with_tag_and_mastery(tag, custom)
        fields_data = self.get_fields(note_ids, field_name)
        cleaned = list(map(self.clean_html, fields_data.values()))
        ruby_removed = list(map(self.remove_anki_ruby, cleaned))
        return ruby_removed

    def get_adjectives(self):
        return self.get_known_adjectives_from_anki()




    def set_adjectives(self, adjectives):
        self.ui.adjective_list.clear()
        self.ui.adjective_list.addItems(adjectives)


    def update_adjectives(self):
        self.fetch_from_anki(self.get_adjectives, self.set_adjectives)





    def set_random_adjectives(self, adjectives):
        self.ui.adjective_list.clear()
        count = self.ui.count_adjectives_spinbox.value()
        count = min(count, len(adjectives))
        random_adjs = random.sample(adjectives, count)
        self.ui.adjective_list.addItems(random_adjs)

    def update_adjectives_random(self):
        self.fetch_from_anki(self.get_adjectives, self.set_random_adjectives)





    def get_adjectives_by_type(self, adj_type: str):
        tag = f"adjective::{adj_type}"  # e.g., "adj::i"
        custom = "notesct>13"
        field_name = "jap_vocab_from_sentence"

        note_ids = self.get_notes_with_tag_and_mastery(tag, custom)
        fields_data = self.get_fields(note_ids, field_name)

        cleaned = list(map(self.clean_html, fields_data.values()))
        return list(map(self.remove_anki_ruby, cleaned))













    