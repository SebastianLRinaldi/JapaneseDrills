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
            self.typing_history,
            self.typing_area, 
            self.timer,
            self.word_count_label,
            self.group("horizontal", [
                    self.session_start_btn, 
                    self.session_submit_btn
            ]),
        ]

        self.apply_layout(component, self)


    def set_widgets(self):
        self.timer.logic.disable_all()
        self.session_start_btn.setText("Start Session")
        self.session_submit_btn.setText("Submit Session")
        self.session_submit_btn.setDisabled(True)
        self.typing_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.typing_area.setMinimumHeight(250)
        
        self.typing_history.setFlow(QListWidget.Flow.TopToBottom)
        self.typing_history.setWrapping(True)
        self.typing_history.setMinimumHeight(165+5)
        self.typing_history.setMaximumHeight(165*2+5) # 165 +5 = 170 which is 5 items at 16 font size 
        self.typing_history.setSpacing(0) # words closer together
        self.typing_history.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.typing_history.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.typing_area.setStyleSheet("font-size: 64pt;")






