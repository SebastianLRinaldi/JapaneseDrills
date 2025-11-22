from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

class Blueprint:
    question_label: QLabel
    word_type_combo: QComboBox

    vocab_label: QLabel
    conjugation_label: QLabel

    typing_area: QLineEdit

    grade_btn: QPushButton

    good_btn: QPushButton
    wrong_btn: QPushButton
    randomize_btn: QPushButton
    sync_btn: QPushButton

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