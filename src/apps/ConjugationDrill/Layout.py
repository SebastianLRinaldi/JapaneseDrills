from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.GUI.UiManager import *
from src.core.EventHandlers.enter_key_handler import EnterKeyHandler
from .widgets.Web.Layout import Layout as webAppLayout



class Layout(UiManager):
    web_app: webAppLayout
    question_label: QLabel
    word_type_combo: QComboBox

    vocab_label: QLabel
    conjugation_label: QLabel

    input_field: QLineEdit

    grade_btn: QPushButton

    good_btn: QPushButton
    wrong_btn: QPushButton
    randomize_btn: QPushButton
    sync_btn: QPushButton


    
    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.set_widgets()

        layout_data = [

            self.splitter("horizontal",[

            self.group("vertical", [
                "sync_btn",
                self.group("horizontal",["word_type_combo"]),
                self.box("horizontal","Word To Conjugation", ["vocab_label", "conjugation_label" ]),
                "input_field",
                "randomize_btn",
                # self.box("horizontal","SUBMIT", ["wrong_btn", "good_btn" ]),
                
            ]),

            "web_app",


            ]),
            

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
        self.vocab_label.setStyleSheet("font-size: 32px;")

        self.conjugation_label.setText("CONJUGATION")
        self.conjugation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.conjugation_label.setStyleSheet("font-size: 32px;")

        self.input_field.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.good_btn.setText("GOOD")
        self.wrong_btn.setText("WRONG")
        self.randomize_btn.setText("RANDOMIZE")
        self.sync_btn.setText("Sync With Anki")


        self.enter_handler = EnterKeyHandler(self)
        self.installEventFilter(self.enter_handler)
