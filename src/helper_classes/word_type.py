import random
from PyQt6.QtWidgets import QListWidget, QSpinBox
from .anki_grabber import AnkiGrabber

class WordType(AnkiGrabber):
    
    def __init__(self, component, word_type:str):
        self.word_type = word_type
        self.word_list: QListWidget = getattr(component, f"{self.word_type}_list")
        self.word_spinbox: QSpinBox = getattr(component, f"{self.word_type}_spinbox")
        
    def get_known_words_from_anki(self):
        custom = ""
        field_name = "jap_vocab_from_sentence"
        note_ids = self.get_notes_with_tag_and_mastery(self.word_type, custom)
        fields_data = self.get_fields(note_ids, field_name)
        cleaned = list(map(self.clean_html, fields_data.values()))
        ruby_removed = list(map(self.remove_anki_ruby, cleaned))
        return ruby_removed 

    def get_words(self):
        words = self.get_known_words_from_anki()
        return words

    def set_words(self, words):
        self.word_list.clear()
        self.word_list.addItems(words)

    def update_words(self):
        self.fetch_from_anki(self.get_words, self.set_words)

    def set_random_words(self, words):
        self.word_list.clear()
        count = self.word_spinbox.value()
        count = min(count, len(words))
        random_words = random.sample(words, count)
        self.word_list.addItems(random_words)

    def update_words_random(self):
        self.fetch_from_anki(self.get_words, self.set_random_words)

