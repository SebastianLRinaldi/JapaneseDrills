import requests
import re
import html
import random

from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *


from src_old.apps.VocabRanomizer.WordTypeFunctions.AnkiGrabber import AnkiGrabberLogic


from src_old.apps.VocabRanomizer.Layout import Layout

class VerbsLogic(AnkiGrabberLogic):
    def __init__(self, ui: Layout):
        self.ui = ui

            
        # godan_verbs = self.get_verbs_by_type("godan")
        # ichidan_verbs = self.get_verbs_by_type("ichidan")
        # irregular_verbs = self.get_verbs_by_type("irregular")

    def get_known_verbs_from_anki(self):
        tag = "verb"
        custom = "notesct>13"
        field_name = "jap_vocab_from_sentence"

        note_ids = self.get_notes_with_tag_and_mastery(tag, custom)
        fields_data = self.get_fields(note_ids, field_name)

        """
        Cleaned does not return with a note_id just the vocab
        """
        cleaned = list(map(self.clean_html, fields_data.values()))
        ruby_removed = list(map(self.remove_anki_ruby, cleaned))
        return ruby_removed 

    def get_verbs(self):
        verbs = self.get_known_verbs_from_anki()
        return verbs




    def set_verbs(self, verbs):
        self.ui.verb_list.clear()
        self.ui.verb_list.addItems(verbs)

    def update_verbs(self):
        self.fetch_from_anki(self.get_verbs, self.set_verbs)




    def set_random_verbs(self, verbs):
        self.ui.verb_list.clear()
        count = self.ui.count_verbs_spinbox.value()
        count = min(count, len(verbs))
        random_verbs = random.sample(verbs, count)
        self.ui.verb_list.addItems(random_verbs)

    def update_verbs_random(self):
        self.fetch_from_anki(self.get_verbs, self.set_random_verbs)





    def get_verbs_by_type(self, verb_type: str):
        tag = f"verb::{verb_type}"  # e.g., "verb::godan"
        custom = "notesct>13"
        field_name = "jap_vocab_from_sentence"

        note_ids = self.get_notes_with_tag_and_mastery(tag, custom)
        fields_data = self.get_fields(note_ids, field_name)

        cleaned = list(map(self.clean_html, fields_data.values()))
        return list(map(self.remove_anki_ruby, cleaned))


    def update_verbs_map(self):
        self.fetch_from_anki(self.get_verbs, self.set_random_verbs)



        