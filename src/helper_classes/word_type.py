import random
from PyQt6.QtWidgets import QListWidget, QSpinBox
from .anki_grabber import AnkiGrabber

class WordType(AnkiGrabber):
    
    def __init__(self, component, word_type:str):
        self.word_type = word_type
        self.word_list_raw = []
        self.word_dict_tagged = {}
        self.word_list: QListWidget = getattr(component, f"{self.word_type}_list")
        self.word_spinbox: QSpinBox = getattr(component, f"{self.word_type}_spinbox")
        
    def get_known_words_from_anki(self):
        custom = ""
        field_name = "jap_vocab_from_sentence"
        note_ids = self.get_notes_with_tag_and_mastery(self.word_type, custom)
        fields_data = self.get_field(note_ids, field_name)
        cleaned = list(map(self.clean_html, fields_data.values()))
        ruby_removed = list(map(self.remove_anki_ruby, cleaned))
        return ruby_removed 

    def get_known_words_with_tags_from_anki(self):
        """
        Returns a list of tuples: (word, verb_type)
        using tags returned by modified get_fields.
        """
        field_name = "jap_vocab_from_sentence"
        note_ids = self.get_notes_with_tag_and_mastery("verb", custom="")

        if not note_ids:
            return []

        fields_data = self.get_fields(note_ids, field_name)

        word_tagged = []
        for note_id, data in fields_data.items():
            word = self.clean_html(data["value"])
            word = self.remove_anki_ruby(word)

            verb_type = None
            for tag in data["tags"]:
                if tag.startswith("verb::"):
                    verb_type = tag.split("::")[1]
                    break

            word_tagged.append((word, verb_type))

        return word_tagged

    def get_words(self):
        words = self.get_known_words_from_anki()
        return words

    def set_words_tagged(self, words):
        self.word_dict_tagged = words

    def set_words(self, words):
        self.word_list.clear()
        self.word_list.addItems(words)
        self.word_list_raw.clear()
        self.word_list_raw = words

    def update_words(self):
        return self.fetch_from_anki(self.get_words, self.set_words)

    def set_random_words(self, words):
        self.word_list.clear()
        count = self.word_spinbox.value()
        count = min(count, len(words))
        random_words = random.sample(words, count)
        self.word_list.addItems(random_words)
        self.word_list_raw.clear()
        self.word_list_raw = words


    def update_words_random(self):
        return self.fetch_from_anki(self.get_words, self.set_random_words)

    def update_words_taged(self):
        return self.fetch_from_anki(self.get_known_words_with_tags_from_anki, self.set_words_tagged)
        

