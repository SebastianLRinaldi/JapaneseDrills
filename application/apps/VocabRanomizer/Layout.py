from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *


from application.FrontEnd.D_WindowFolder.windowConfigureation import *

# from .widgets.CUSTOMWIDGET import YOURWIDGET


class VocabRandomizerLayout(LayoutManager):
    grammar_label: QLabel
    noun_label: QLabel 
    verb_label: QLabel
    count_nouns_spinbox: QSpinBox       # lets user choose how many random words to grab
    count_verbs_spinbox: QSpinBox       # lets user choose how many random words to grab
    count_grammar_spinbox: QSpinBox       # lets user choose how many random words to grab

    grammar_list: QListWidget
    noun_list: QListWidget
    verb_list: QListWidget

    sync_btn: QPushButton
    randomize_btn: QPushButton
    

    
    def __init__(self):
        super().__init__()
        self.init_widgets()

        self.sync_btn.setText("SYNC")
        self.randomize_btn.setText("RANDOMIZE UNSELECTED")
        self.grammar_label.setText("GRAMMAR POINTS")
        self.noun_label.setText("NOUNS")
        self.verb_label.setText("VERBS")

        layout_data = [
            self.group("horizontal",["grammar_label", "noun_label", "verb_label"]),
            self.group("horizontal",["count_grammar_spinbox", "count_nouns_spinbox", "count_verbs_spinbox", ]),
            self.group("horizontal",["grammar_list", "noun_list", "verb_list"]),
            self.group("vertical",["randomize_btn","sync_btn"])
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