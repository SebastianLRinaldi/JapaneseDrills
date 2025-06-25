from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.GUI.UiManager import *

# from .widgets.CUSTOMWIDGET import YOURWIDGET





class Layout(UiManager):

    question_label: QLabel
    word_type_combo: QComboBox

    vocab_label: QLabel
    conjugation_label: QLabel

    input_field: QLineEdit

    good_btn: QPushButton
    wrong_btn: QPushButton
    randomize_btn: QPushButton


    
    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.set_widgets()

        layout_data = [

            self.group("horizontal",["word_type_combo",]),
            
            self.box("horizontal","Word To Conjugation", ["vocab_label", "conjugation_label" ]),
            "input_field",
            self.box("horizontal","SUBMIT", ["good_btn", "wrong_btn" ]),
            "randomize_btn",

        ]

        self.apply_layout(layout_data)

    def init_widgets(self):
        annotations = getattr(self.__class__, "__annotations__", {})
        for name, widget_type in annotations.items():
            widget = widget_type()
            setattr(self, name, widget)


    def set_widgets(self):

        
        self.question_label.setText("Select word type and conjugation")
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)


        categories = [
            "Godan",
            "Ichidan",
            "Irregular",
            "Godan + Ichidan",
            "All Verb Types",
            "い-Adjective",
            "な-Adjective",
            "い-Adjective + な-Adjective",
        ]
        self.word_type_combo.addItems(categories)


        self.vocab_label.setText("VOCAB")
        self.vocab_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.conjugation_label.setText("CONJUGATION")
        self.conjugation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.input_field.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.good_btn.setText("GOOD")
        self.wrong_btn.setText("WRONG")
        self.randomize_btn.setText("RANDOMIZE")
