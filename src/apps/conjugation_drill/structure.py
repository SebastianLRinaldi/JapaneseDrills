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
            self.group("horizontal", [
                    self.vocab_label,                
                    self.group("vertical",[
                        self.verb_class_combo,
                        self.polarity_combo,
                        self.base_form_combo,
                        ]),
                    ]),
            self.word_count_label,
            
            self.typing_area,


            # self.grade_btn,
            # self.randomize_btn,
            # self.sync_btn,

        ]

        self.apply_layout(component, self)


    def set_widgets(self):
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
        self.vocab_label.setStyleSheet("font-size: 128px;")

        self.conjugation_label.setText("CONJUGATION")
        self.conjugation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)


        self.typing_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.randomize_btn.setText("RANDOMIZE")
        self.sync_btn.setText("Sync With Anki")



        self.word_count_label.setText("COUNT")
        self.word_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font = QFont()
        font.setPointSize(32)  # increase the number to make text bigger
        font.setBold(True)      # optional, makes text bold

        self.set_widgets_font(font, [
            self.word_count_label,
            self.verb_class_combo,
            self.base_form_combo,
            self.polarity_combo,
            self.formality_combo,
        ])


    def set_widgets_font(self, font: QFont, widgets: list[QWidget]):
        for w in widgets:
            w.setFont(font)










