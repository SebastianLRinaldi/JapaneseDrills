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
            self.group("horizontal",[self.script_combo, self.word_type_combo, self.vowel_selector]),

            self.timer, 
            
            self.question_label,
            self.typing_area,

            self.group("horizontal",[self.question_count_label, self.pass_fail_label]),
        ]

        self.apply_layout(component, self)


    def set_widgets(self):
        self.typing_area.setMinimumHeight(250)
        self.vowel_selector.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.vowel_selector.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.vowel_selector.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.vowel_selector.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)



        font = QFont()
        font.setPointSize(24)  # increase the number to make text bigger
        # font.setBold(True)      # optional, makes text bold

        self.set_widgets_font(font, [
            self.question_count_label,
            self.pass_fail_label,
            self.script_combo,
            self.word_type_combo,
            self.vowel_selector,
            self.typing_area,
        ])

        font = QFont()
        font.setPointSize(128)  # increase the number to make text bigger
        font.setBold(True)      # optional, makes text bold

        self.set_widgets_font(font, [
            self.question_label,
        ])

        self.set_widget_alignment(Qt.AlignmentFlag.AlignCenter, [
            self.question_count_label,
            self.pass_fail_label,
            self.question_label,
            self.typing_area,
        ])


    def set_widgets_font(self, font: QFont, widgets: list[QWidget]):
        for w in widgets:
            w.setFont(font)

    def set_widget_alignment(self, alignment:Qt.AlignmentFlag, widgets: list[QWidget]):
        for w in widgets:
            w.setAlignment(alignment)




