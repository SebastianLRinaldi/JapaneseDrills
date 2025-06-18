import requests
import re
import html
import random

from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from application.apps.VocabRanomizer.Layout import VocabRandomizerLayout












class VocabRandomizerLogic:
    def __init__(self, ui: VocabRandomizerLayout):
        self.ui = ui

    def get_notes_with_tag_and_mastery(self, tag, custom):
        payload = {
            "action": "findNotes",
            "version": 6,
            "params": {
                "query": f'tag:{tag} (tag:status:understandable OR prop:cdn:{custom})'
            }
        }
        response = requests.post("http://localhost:8765", json=payload)
        response.raise_for_status()
        return response.json().get("result", [])

    def get_fields(self, note_ids, field_name):
        if not note_ids:
            return {}

        payload = {
            "action": "notesInfo",
            "version": 6,
            "params": {
                "notes": note_ids
            }
        }
        response = requests.post("http://localhost:8765", json=payload)
        response.raise_for_status()
        notes_info = response.json().get("result", [])

        # Extract the field values
        result = {}
        for note in notes_info:
            fields = note.get("fields", {})
            if field_name in fields:
                result[note["noteId"]] = fields[field_name]["value"]
        return result

    def clean_html(self, raw_html, remove_spaces=True):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        cleantext = html.unescape(cleantext)  # converts &nbsp; to space
        if remove_spaces:
            cleantext = cleantext.replace(' ', '')
        return cleantext

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
        return cleaned
        # print(len(note_ids))
        # for note_id, vocab in fields_data.items():
        #     print(f"{self.clean_html(vocab)}")

    def get_known_nouns_from_anki(self):
        tag = "noun"
        custom = "notesct>13"
        field_name = "jap_vocab_from_sentence"

        note_ids = self.get_notes_with_tag_and_mastery(tag, custom)
        fields_data = self.get_fields(note_ids, field_name)
        cleaned = list(map(self.clean_html, fields_data.values()))
        return cleaned

    def get_known_grammar_from_anki(self):
        tag = "noun"
        custom = "notesct>13"
        field_name = "jap_vocab_from_sentence"
        print('START FIND NOUNS')
        note_ids = self.get_notes_with_tag_and_mastery(tag, custom)
        fields_data = self.get_fields(note_ids, field_name)
        cleaned = list(map(self.clean_html, fields_data.values()))
        print("NOUNS FOUND")
        return cleaned

    def get_grammar(self):
        grammar_points = self.get_known_grammar_from_anki()
        return grammar_points

    def get_verbs(self):
        verbs = self.get_known_verbs_from_anki()
        return verbs

    def get_nouns(self):
        nouns = self.get_known_nouns_from_anki()
        return nouns

    def set_grammar(self, grammar_points):
        self.ui.grammar_list.clear()
        self.ui.grammar_list.addItems(grammar_points)

    def set_verbs(self, verbs):
        self.ui.verb_list.clear()
        self.ui.verb_list.addItems(verbs)

    def set_nouns(self, nouns):
        self.ui.noun_list.clear()
        self.ui.noun_list.addItems(nouns)

    def fetch_from_anki(self, func, callback):
        thread = QThread()
        fetcher = Fetcher(func)
        fetcher.moveToThread(thread)

        def cleanup():
            fetcher.deleteLater()
            thread.deleteLater()
            self._threads.remove((thread, fetcher))

        thread.started.connect(fetcher.run)
        fetcher.finished.connect(callback)
        fetcher.finished.connect(thread.quit)
        thread.finished.connect(cleanup)

        if not hasattr(self, '_threads'):
            self._threads = []
        self._threads.append((thread, fetcher))

        thread.start()

    def update_lists(self):
        self.fetch_from_anki(self.get_nouns, self.set_nouns)
        self.fetch_from_anki(self.get_verbs, self.set_verbs)
        self.fetch_from_anki(self.get_grammar, self.set_grammar)


    def set_random_nouns(self, nouns):
        self.ui.noun_list.clear()
        count = self.ui.count_nouns_spinbox.value()
        random_nouns = random.sample(nouns, count)
        self.ui.noun_list.addItems(random_nouns)

    def set_random_verbs(self, verbs):
        self.ui.verb_list.clear()
        count = self.ui.count_verbs_spinbox.value()
        random_verbs = random.sample(verbs, count)
        self.ui.verb_list.addItems(random_verbs)
        
    def set_random_grammar(self, grammar_points):
        self.ui.grammar_list.clear()
        count = self.ui.count_grammar_spinbox.value()
        random_grammar = random.sample(grammar_points, count)
        self.ui.grammar_list.addItems(random_grammar)

    def update_list_random(self):
        self.fetch_from_anki(self.get_nouns, self.set_random_nouns)
        self.fetch_from_anki(self.get_verbs, self.set_random_verbs)
        self.fetch_from_anki(self.get_grammar, self.set_random_grammar)

        







class Fetcher(QObject):
    finished = pyqtSignal(object)  # emit whatever the function returns

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        result = self.func(*self.args, **self.kwargs)
        self.finished.emit(result)

