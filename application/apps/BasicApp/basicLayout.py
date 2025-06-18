import os
import sys
import time
import re

import threading
from threading import Thread
from enum import Enum
from queue import Queue
from typing import List
from datetime import timedelta

from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from application.FrontEnd.C_Grouper.SpliterGroupConfiguration import *
from application.FrontEnd.C_Grouper.TabGroupConfigureation import *
from application.FrontEnd.C_Grouper.widgetGroupFrameworks import *

from application.FrontEnd.D_WindowFolder.windowConfigureation import *

from .widgets.chunkInput import ChunkInput
from .widgets.chunkHolder import ChunkHolder 


"""
When you press enter after you type it should either go to the category selection or the next text box below
"""
class BasicLayout(LayoutManager):

    label: QLabel
    chunk_holder: ChunkHolder
    add_btn: QPushButton
    remove_btn: QPushButton


    
    def __init__(self):
        super().__init__()
        self.init_widgets()

        example_text = """
        Step 1: Identify Each Character / Word
        Character/Word: ______ → What is it? (Kanji, kana, particle, verb form, etc.)
        Example: 猫 → Kanji for “cat”(List all components clearly)
        """
        self.label.setText(example_text)
        self.add_btn.setText("ADD")
        self.remove_btn.setText("REMOVE")



        layout_data = [

                "label",
                "chunk_holder",
                self.group("horizontal",["remove_btn", "add_btn"])
        ]
        
        
        self.apply_layout(layout_data )

        # self.add_widgets_to_window(
        #     self.label,
        #     self.chunk_holder,

        #     addOrRemoveGroup.add_widgets_to_group(
        #         self.remove_btn,
        #         self.add_btn,
        #         layout="H"
        #     )
        # )

    def init_widgets(self):
        for name, widget_type in self.__annotations__.items():
            widget = widget_type()
            setattr(self, name, widget)
