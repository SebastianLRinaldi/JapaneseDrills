import requests
import re
import html
import random

from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from .Layout import Layout


class Logic:
    def __init__(self, ui: Layout):
        self.ui = ui

    def get_notes_with_tag_and_mastery(self, tag, custom):
        payload = {
            "action": "findNotes",
            "version": 6,
            "params": {
                "query": f'tag:{tag} (tag:status::understandable OR prop:cdn:{custom})'
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

    def remove_anki_ruby(self, text):
        return re.sub(r'\[.*?\]', '', text)

    # def remove_anki_ruby(self, text):
    #     # Remove optional space + [furigana] after kanji
    #     return re.sub(r'(?<=[\u4e00-\u9fff])\s*\[[^\[\]]*?\]', '', text)
    def clean_html(self, raw_html, remove_spaces=True):
        print(raw_html)
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        cleantext = html.unescape(cleantext)  # converts &nbsp; to space
        if remove_spaces:
            cleantext = cleantext.replace(' ', '')
        return cleantext


    def get_known_nouns_from_anki(self):
        tag = "noun"
        custom = "notesct>13"
        field_name = "jap_vocab_from_sentence"

        note_ids = self.get_notes_with_tag_and_mastery(tag, custom)
        fields_data = self.get_fields(note_ids, field_name)
        cleaned = list(map(self.clean_html, fields_data.values()))
        ruby_removed = list(map(self.remove_anki_ruby, cleaned))
        return ruby_removed 

    def get_known_adjectives_from_anki(self):
        tag = "adjective"
        custom = "notesct>13"
        field_name = "jap_vocab_from_sentence"

        note_ids = self.get_notes_with_tag_and_mastery(tag, custom)
        fields_data = self.get_fields(note_ids, field_name)
        cleaned = list(map(self.clean_html, fields_data.values()))
        ruby_removed = list(map(self.remove_anki_ruby, cleaned))
        return ruby_removed

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

    def get_known_grammar_from_anki(self):
        tag = "grammar"
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

    def get_adjectives(self):
        return self.get_known_adjectives_from_anki()

    def get_verbs(self):
        verbs = self.get_known_verbs_from_anki()
        return verbs

    def get_grammar(self):
        grammar_points = self.get_known_grammar_from_anki()
        return grammar_points


    def set_nouns(self, nouns):
        self.ui.noun_list.clear()
        self.ui.noun_list.addItems(nouns)

    def set_adjectives(self, adjectives):
        self.ui.adjective_list.clear()
        self.ui.adjective_list.addItems(adjectives)

    def set_verbs(self, verbs):
        self.ui.verb_list.clear()
        self.ui.verb_list.addItems(verbs)

    def set_grammar(self, grammar_points):
        self.ui.grammar_list.clear()
        self.ui.grammar_list.addItems(grammar_points)


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


    def update_nouns(self):
        self.fetch_from_anki(self.get_nouns, self.set_nouns)

    def update_adjectives(self):
        self.fetch_from_anki(self.get_adjectives, self.set_adjectives)

    def update_verbs(self):
        self.fetch_from_anki(self.get_verbs, self.set_verbs)

    def update_grammar(self):
        self.fetch_from_anki(self.get_grammar, self.set_grammar)


    def update_lists(self):
        self.update_nouns()
        self.update_adjectives()
        self.update_verbs()
        self.update_grammar()


    def set_random_nouns(self, nouns):
        self.ui.noun_list.clear()
        count = self.ui.count_nouns_spinbox.value()
        count = min(count, len(nouns))
        random_nouns = random.sample(nouns, count)
        self.ui.noun_list.addItems(random_nouns)

    def set_random_adjectives(self, adjectives):
        self.ui.adjective_list.clear()
        count = self.ui.count_adjectives_spinbox.value()
        count = min(count, len(adjectives))
        random_adjs = random.sample(adjectives, count)
        self.ui.adjective_list.addItems(random_adjs)

    def set_random_verbs(self, verbs):
        self.ui.verb_list.clear()
        count = self.ui.count_verbs_spinbox.value()
        count = min(count, len(verbs))
        random_verbs = random.sample(verbs, count)
        self.ui.verb_list.addItems(random_verbs)
        
    def set_random_grammar(self, grammar_points):
        self.ui.grammar_list.clear()
        count = self.ui.count_grammar_spinbox.value()
        count = min(count, len(grammar_points))
        random_grammar = random.sample(grammar_points, count)
        self.ui.grammar_list.addItems(random_grammar)


    def update_nouns_random(self):
        self.fetch_from_anki(self.get_nouns, self.set_random_nouns)

    def update_adjectives_random(self):
        self.fetch_from_anki(self.get_adjectives, self.set_random_adjectives)

    def update_verbs_random(self):
        self.fetch_from_anki(self.get_verbs, self.set_random_verbs)

    def update_grammar_random(self):
        self.fetch_from_anki(self.get_grammar, self.set_random_grammar)


    def update_list_random(self):
        self.update_nouns_random()
        self.update_adjectives_random()
        self.update_verbs_random()
        self.update_grammar_random()


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

