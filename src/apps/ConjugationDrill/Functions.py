from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from .Layout import Layout

ADJECTIVES = ["たかい", "おおきい", "ちいさい", "あたらしい", "ふるい"]

CONJUGATION_TYPES = [
    "present affirmative",
    "present negative",
    "past affirmative",
    "past negative",
    "te-form"
]

        # Conjugation mappings for each category
# Your vocab and conjugations data
vocab_map = {
    "Godan": ["書く", "話す", "飲む"],
    "Ichidan": ["食べる", "見る"],
    "Irregular": ["する", "来る"],
    "Godan + Ichidan": ["書く", "話す", "飲む", "食べる", "見る"],
    "All Verb Types": ["書く", "話す", "飲む", "食べる", "見る", "する", "来る"],
    "い-Adjective": ["高い", "速い"],
    "な-Adjective": ["静か", "便利"],
    "い-Adjective + な-Adjective": ["高い", "静か"],
}

verb_conjugations = [
    # "Dictionary Form",
    "ます Form",
    "て: Te-Form",
    "た : Past",
    "ない : Negative",
    "なかった : Past Negative",
    # "ます : Polite",
    # "ません : Polite Negative",
    # "ました : Polite Past",
    # "ませんでした : Polite Past Negative"
    # "Potential",
    # "Passive",
    # "Causative",
    # "Volitional",
    # "Imperative",
]

adj_conjugations = [
    # "Plain",
    "Negative",
    "Past",
    "Te-form",
    "Adverbial",
]

conjugations_map = {
    "Godan": verb_conjugations,
    "Ichidan": verb_conjugations,
    "Irregular": ["する", "来る"],
    "Godan + Ichidan": verb_conjugations,
    "All Verb Types": verb_conjugations,
    "い-Adjective": adj_conjugations,
    "な-Adjective": adj_conjugations,
    "い-Adjective + な-Adjective": adj_conjugations,
}

import random
class Logic:
    def __init__(self, ui: Layout):
        self.ui = ui

    def handle_good(self):
        self.ui.input_field.setStyleSheet("color: green")

    def handle_wrong(self):
        self.ui.input_field.setStyleSheet("color: red")


    def update_labels(self, selected_type):
        vocab_list = vocab_map.get(selected_type, [])
        conjugation_list = conjugations_map.get(selected_type, [])

        if not vocab_list or not conjugation_list:
            self.ui.vocab_label.setText("No vocab")
            self.ui.conjugation_label.setText("No conjugations")
            return

        vocab = random.choice(vocab_list)
        conj_type = random.choice(conjugation_list)

        self.ui.vocab_label.setText(vocab)
        self.ui.conjugation_label.setText(f"→ {conj_type}")
        self.ui.input_field.clear()
        self.ui.input_field.setStyleSheet("")

    def randomize(self):
        selected_type = self.ui.word_type_combo.currentText()

        vocab_list = vocab_map.get(selected_type, [])
        conjugation_list = conjugations_map.get(selected_type, [])

        if not vocab_list or not conjugation_list:
            self.ui.vocab_label.setText("No vocab")
            self.ui.conjugation_label.setText("No conjugations")
            return

        vocab = random.choice(vocab_list)
        conj_type = random.choice(conjugation_list)

        self.ui.vocab_label.setText(vocab)
        self.ui.conjugation_label.setText(f"→ {conj_type}")
        self.ui.input_field.clear()
        self.ui.input_field.setStyleSheet("")

        
