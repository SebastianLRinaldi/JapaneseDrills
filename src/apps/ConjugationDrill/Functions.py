from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from .Layout import Layout





        # Conjugation mappings for each category
# Your vocab and conjugations data
# vocab_map = {
#     "Godan": ["書く", "話す", "飲む"],
#     "Ichidan": ["食べる", "見る"],
#     "Irregular": ["する", "来る"],
#     "Godan + Ichidan": ["書く", "話す", "飲む", "食べる", "見る"],
#     "All Verb Types": ["書く", "話す", "飲む", "食べる", "見る", "する", "来る"],
#     "い-Adjective": ["高い", "速い"],
#     "な-Adjective": ["静か", "便利"],
#     "い-Adjective + な-Adjective": ["高い", "静か"],
# }

# vocab_map = {
#     "Godan": [
#         "書く",   # -く
#         "話す",   # -す
#         "飲む",   # -む
#         "待つ",   # -つ
#         "遊ぶ",   # -ぶ
#         "死ぬ",   # -ぬ
#         "泳ぐ",   # -ぐ
#         "買う",   # -う
#         "打つ",   # -つ
#         "要る",   # -る (Godan-る)
#     ],
#     "Ichidan": [
#         "食べる",  # -る Ichidan
#         "見る",    # -る Ichidan
#         "起きる",  # -る Ichidan
#     ],
#     "Irregular": [
#         "する",
#         "来る",
#         "勉強する",
#     ],
#     "Godan + Ichidan": [
#         "書く", "話す", "飲む", "待つ", "遊ぶ", "死ぬ", "泳ぐ", "買う", "打つ", "要る",
#         "食べる", "見る", "起きる"
#     ],
#     "All Verb Types": [
#         "書く", "話す", "飲む", "待つ", "遊ぶ", "死ぬ", "泳ぐ", "買う", "打つ", "要る",
#         "食べる", "見る", "起きる",
#         "する", "来る", "勉強する"
#     ],
#     "い-Adjective": [
#         "高い",    # high
#         "新しい",  # new
#         "美味しい" # delicious
#     ],
#     "な-Adjective": [
#         "静か",    # quiet
#         "便利",    # convenient
#         "有名"     # famous
#     ],
#     "い-Adjective + な-Adjective": [
#         "高い", "新しい", "美味しい",
#         "静か", "便利", "有名"
#     ],
# }



# vocab_map = {
#     "Godan": [],
#     "Ichidan": [],
#     "Irregular": ["する", "来る"],
#     "Godan + Ichidan": [],
#     "All Verb Types": [],
#     "い-Adjective": [],
#     "な-Adjective": [],
#     "い-Adjective + な-Adjective": [],
# }








verb_conjugations = [
    # "Dictionary Form",
    "ます Form/Polite",
    "て: Te-Form",
    "た : Past",
    "ない : Negative",
    "なかった : Past Negative",
    "ません : Polite Negative",
    "ました : Polite Past",
    "ませんでした : Polite Past Negative"
    # "Potential",
    # "Passive",
    # "Causative",
    # "Volitional",
    # "Imperative",
]

# CONJUGATION_TYPES = [
#     "present affirmative",
#     "present negative",
#     "past affirmative",
#     "past negative",
#     "te-form"
# ]

adj_conjugations = [
    # "Plain",
    "Negative",
    "Negative Past",
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



class ShuffleQueue:
    def __init__(self, items):
        self.items = items
        self.queue = []

    def refill(self):
        self.queue = self.items[:]
        random.shuffle(self.queue)

    def next(self):
        if not self.queue:
            self.refill()
        return self.queue.pop()

    def __repr__(self):
        return f"ShuffleQueue(size={len(self.queue)}, items={self.queue})"



import random

from .widgets.Web.Functions import Logic as webAppLogic

class Logic:
    def __init__(self, ui: Layout):
        self.ui = ui
        self.web_app_logic = webAppLogic(self.ui.web_app)

        # Lazy init of queues

        self.vocab_queues = {}

        self.conj_queues = {}

        self.vocab_map = {
        }


    def handle_good(self):
        self.ui.input_field.setStyleSheet("color: green")

    def handle_wrong(self):
        self.ui.input_field.setStyleSheet("color: red")


    def update_labels(self, selected_type):
        vocab_list = self.vocab_map.get(selected_type, [])
        conjugation_list = conjugations_map.get(selected_type, [])

        if not vocab_list or not conjugation_list:
            self.ui.vocab_label.setText("No vocab")
            self.ui.conjugation_label.setText("No conjugations")
            return

        if selected_type not in self.vocab_queues:
            self.vocab_queues[selected_type] = ShuffleQueue(vocab_list)
        if selected_type not in self.conj_queues:
            self.conj_queues[selected_type] = ShuffleQueue(conjugation_list)

        vocab = self.vocab_queues[selected_type].next()
        conj_type = self.conj_queues[selected_type].next()

        print(f"VQUE: {self.vocab_queues[selected_type]}")
        print(f"VQUE: {self.conj_queues[selected_type]}")

        self.ui.vocab_label.setText(vocab)
        self.ui.conjugation_label.setText(f"→ {conj_type}")
        self.ui.input_field.clear()
        self.ui.input_field.setStyleSheet("")

    def randomize(self):
        selected_type = self.ui.word_type_combo.currentText()

        vocab_list = self.vocab_map.get(selected_type, [])
        conjugation_list = conjugations_map.get(selected_type, [])

        if not vocab_list or not conjugation_list:
            self.ui.vocab_label.setText("No vocab")
            self.ui.conjugation_label.setText("No conjugations")
            return

        if selected_type not in self.vocab_queues:
            self.vocab_queues[selected_type] = ShuffleQueue(vocab_list)
        if selected_type not in self.conj_queues:
            self.conj_queues[selected_type] = ShuffleQueue(conjugation_list)

        vocab = self.vocab_queues[selected_type].next()
        conj_type = self.conj_queues[selected_type].next()

        print(f"VQUE: {self.vocab_queues[selected_type]}")
        print(f"VQUE: {self.conj_queues[selected_type]}")

        self.ui.vocab_label.setText(vocab)
        self.ui.conjugation_label.setText(f"→ {conj_type}")
        self.ui.input_field.clear()
        self.ui.input_field.setStyleSheet("")

