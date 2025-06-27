from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *


from src.core.GUI.UiManager import *

# from .widgets.CUSTOMWIDGET import YOURWIDGET


class Layout(UiManager):
    count_nouns_spinbox: QSpinBox       # lets user choose how many random words to grab
    count_verbs_spinbox: QSpinBox       # lets user choose how many random words to grab
    count_grammar_spinbox: QSpinBox       # lets user choose how many random words to grab
    count_adjectives_spinbox: QSpinBox 
    
    noun_list: QListWidget
    adjective_list: QListWidget
    grammar_list: QListWidget
    verb_list: QListWidget

    grammar_set_all_btn: QPushButton
    grammar_random_btn: QPushButton

    noun_set_all_btn: QPushButton
    noun_random_btn: QPushButton

    adjective_set_all_btn: QPushButton
    adjective_random_btn: QPushButton

    verb_set_all_btn: QPushButton
    verb_random_btn: QPushButton

    get_all_btn: QPushButton
    randomize_btn: QPushButton

    
    

    
    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.set_widgets()

        layout_data = [
            self.splitter("horizontal", [
                self.box("vertical", "Nouns", [
                    "count_nouns_spinbox",
                    "noun_list",
                    "noun_set_all_btn",
                    "noun_random_btn",
                ]),

                self.box("vertical", "Adjectives", [
                    "count_adjectives_spinbox",
                    "adjective_list",
                    "adjective_set_all_btn",
                    "adjective_random_btn",
                ]),

                self.box("vertical", "Verbs", [
                    "count_verbs_spinbox",
                    "verb_list",
                    "verb_set_all_btn",
                    "verb_random_btn",
                ]),

                self.box("vertical", "Grammar", [
                    "count_grammar_spinbox",
                    "grammar_list",
                    "grammar_set_all_btn",
                    "grammar_random_btn",
                ]),

            ]),
            self.group("vertical", [
                "get_all_btn",
                "randomize_btn"
            ])
        ]

        self.apply_layout(layout_data)


    def init_widgets(self):
        for name, widget_type in self.__annotations__.items():
            widget = widget_type()
            if isinstance(widget, QListWidget):
                # widget.setFlow(QListWidget.Flow.LeftToRight)
                # widget.setWrapping(True)
                widget.setResizeMode(QListWidget.ResizeMode.Adjust)
                widget.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
            setattr(self, name, widget)

    def set_widgets(self):
        self.get_all_btn.setText("SET ALL")
        self.randomize_btn.setText("RANDOMIZE ALL")

        self.grammar_set_all_btn.setText("SET ALL GRAMMAR POINTS")
        self.grammar_random_btn.setText("RANDOM GRAMMAR POINTS")

        self.noun_set_all_btn.setText("SET ALL NOUNS")
        self.noun_random_btn.setText("RANDOM NOUNS")


        self.adjective_set_all_btn.setText("SET ALL ADJECTIVES")
        self.adjective_random_btn.setText("RANDOM ADJECTIVES")



        self.verb_set_all_btn.setText("SET ALL VERBS")
        self.verb_random_btn.setText("RANDOM VERBS")

        self.count_nouns_spinbox.setValue(5)
        self.count_verbs_spinbox.setValue(5)
        self.count_grammar_spinbox.setValue(5)
        self.count_adjectives_spinbox.setValue(5)