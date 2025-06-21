import requests
import re
import html
import random

from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.apps.ConjugationRandomizer.Layout import ConjugationRandomizerLayout


class ConjugationRandomizerLogic:
    def __init__(self, ui: ConjugationRandomizerLayout):
        self.ui = ui


    # for inflection in inflections:
    #     item = QListWidgetItem(inflection)
    #     item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
    #     item.setCheckState(Qt.CheckState.Unchecked)
    #     self.inflections.addItem(item)

    # for auxiliary in auxiliaries:
    #     item = QListWidgetItem(auxiliary)
    #     item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
    #     item.setCheckState(Qt.CheckState.Unchecked)
    #     self.auxiliaries.addItem(item)

    # for conjugation in conjugations:
    #     item = QListWidgetItem(conjugation)
    #     item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
    #     item.setCheckState(Qt.CheckState.Unchecked)
    #     self.conjugations.addItem(item)


    
        self.conjugations_known = [
            "て: Te-Form",
            "た : Past",
            "ない : Negative",
            "なかった : Past Negative",
            "ます : Polite",
            "ません : Polite Negative",
            "ました : Polite Past",
            "ませんでした : Polite Past Negative"
        ]

        self.inflections_known = [
            "〜う / 〜よう : Volitional", # Can stack aux phrases
            "〜ば : Conditional", # Can stack aux
            "〜ろ / 〜よ : Imperative" # Can not Stack
        ]

        self.auxiliaries_known = [
            "〜れる / 〜られる : Potential / Passive",
            "〜たい : Want to do",
            # "〜させる : Causative",
            
            "〜ている : Progressive / Resultative",
            # "〜てしまう : Regret / Completion",
            # "〜てある : Resulting state (intentional)",
            # "〜ていく : Going to do (from now)",
            # "〜てくる : Came to do / gradual start",
            
            # "〜ことがある : Past experience",
            # "〜つもりだ : Plan to do",
        ]



    def set_conjugations(self):
        self.ui.conjugations_list.clear()
        self.ui.conjugations_list.addItems(self.conjugations_known)

    def set_inflections(self):
        self.ui.inflections_list.clear()
        self.ui.inflections_list.addItems(self.inflections_known)

    def set_auxiliaries(self):
        self.ui.auxiliaries_list.clear()
        self.ui.auxiliaries_list.addItems(self.auxiliaries_known)

    def update_lists(self):
        self.set_inflections()
        self.set_conjugations()
        self.set_auxiliaries()

    def set_conjugations_random(self):
        self.ui.conjugations_list.clear()
        count = self.ui.count_conjugations_spinbox.value()
        count = min(count, len(self.conjugations_known))
        random_conjugations = random.sample(self.conjugations_known, count)
        self.ui.conjugations_list.addItems(random_conjugations)

    def set_inflections_random(self):
        self.ui.inflections_list.clear()
        count = self.ui.count_inflections_spinbox.value()
        count = min(count, len(self.inflections_known))
        random_inflections = random.sample(self.inflections_known, count)
        self.ui.inflections_list.addItems(random_inflections)

    def set_auxiliaries_random(self):
        self.ui.auxiliaries_list.clear()
        count = self.ui.count_auxiliaries_spinbox.value()
        count = min(count, len(self.auxiliaries_known))
        random_auxiliaries = random.sample(self.auxiliaries_known, count)
        self.ui.auxiliaries_list.addItems(random_auxiliaries)

    def update_list_random(self):
        self.set_conjugations_random()
        self.set_inflections_random()
        self.set_auxiliaries_random()

