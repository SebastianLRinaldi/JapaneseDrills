from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.gui.layout_builder import LayoutBuilder
from .blueprint import Blueprint

class Structure(LayoutBuilder, Blueprint):
    """
    Where you arrange and decorate the widgets
    """

    def __init__(self, component):
        super().__init__()
        
        self._map_widgets(component)
        self.set_widgets()
        
        self.layout_data = [

            self.splitter("horizontal",[

            self.group("vertical", [
                "sync_btn",
                self.group("horizontal",["word_type_combo"]),
                self.box("horizontal","Word To Conjugation", ["vocab_label", "conjugation_label" ]),
                self.typing_area,
                "randomize_btn",
                # self.box("horizontal","SUBMIT", ["wrong_btn", "good_btn" ]),
                
            ]),


            ]),
            

        ]

        self.apply_layout(component, self)


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

        self.typing_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.good_btn.setText("GOOD")
        self.wrong_btn.setText("WRONG")
        self.randomize_btn.setText("RANDOMIZE")
        self.sync_btn.setText("Sync With Anki")


        # self.enter_handler = EnterKeyHandler(self)
        # self.installEventFilter(self.enter_handler)







