from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

# from src.helpers import *
from .blueprint import BluePrint

"""
Close methods
Ctrl+k + Ctrl+0

Open Methods 
Ctrl+k + Ctrl+J
"""
class Logic(BluePrint):

    def __init__(self, component):
        self._map_widgets(component)

    def update_lists(self):
        self.noun_list.logic.update_words()
        self.adjective_list.logic.update_words()
        self.verb_list.logic.update_words()
        self.adverb_list.logic.update_words()

    def update_list_random(self):
        self.noun_list.logic.update_words_random()
        self.adjective_list.logic.update_words_random()
        self.verb_list.logic.update_words_random()
        self.adverb_list.logic.update_words_random()

