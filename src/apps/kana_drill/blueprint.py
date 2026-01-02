from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.components import *

class Blueprint:
    timer: Timer
    question_count_label: QLabel
    pass_fail_label: QLabel
    question_label: QLabel
    script_combo: QComboBox
    word_type_combo: QComboBox
    vowel_selector: QListWidget
    typing_area: QLineEdit

    def _map_widgets(self, source):
        """
        Copy existing widget instances from source to self.
        """
        # source is some object that already has the widgets as attributes
        for name in self.__annotations__:
            setattr(self, name, getattr(source, name))

    def _init_widgets(self):
        """
        Instantiate all widgets defined in type hints.
        Call this manually when you want actual widget instances.
        """
        for name, typ in self.__annotations__.items():
            setattr(self, name, typ())