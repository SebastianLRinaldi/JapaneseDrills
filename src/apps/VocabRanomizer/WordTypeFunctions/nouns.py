import requests
import re
import html
import random

from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *


from src.apps.VocabRanomizer.WordTypeFunctions.AnkiGrabber import AnkiGrabberLogic

from src.apps.VocabRanomizer.Layout import Layout

class NounsLogic(AnkiGrabberLogic):
    def __init__(self, ui: Layout):
        self.ui = ui


    def get_known_nouns_from_anki(self):
        tag = "noun"
        custom = "notesct>13"
        field_name = "jap_vocab_from_sentence"

        note_ids = self.get_notes_with_tag_and_mastery(tag, custom)
        fields_data = self.get_fields(note_ids, field_name)
        cleaned = list(map(self.clean_html, fields_data.values()))
        ruby_removed = list(map(self.remove_anki_ruby, cleaned))
        return ruby_removed 

    def get_nouns(self):
        nouns = self.get_known_nouns_from_anki()
        return nouns

    def set_nouns(self, nouns):
        self.ui.noun_list.clear()
        self.ui.noun_list.addItems(nouns)

    def update_nouns(self):
        self.fetch_from_anki(self.get_nouns, self.set_nouns)

    def set_random_nouns(self, nouns):
        self.ui.noun_list.clear()
        count = self.ui.count_nouns_spinbox.value()
        count = min(count, len(nouns))
        random_nouns = random.sample(nouns, count)
        self.ui.noun_list.addItems(random_nouns)


    def update_nouns_random(self):
        self.fetch_from_anki(self.get_nouns, self.set_random_nouns)













        