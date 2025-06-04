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
    def __init__(self):
        super().__init__()

        example_text = """
        Step 1: Identify Each Character / Word
        Character/Word: ______ → What is it? (Kanji, kana, particle, verb form, etc.)
        Example: 猫 → Kanji for “cat”(List all components clearly)
        """
        
        self.label = QLabel(example_text)
        
        self.chunk_holder = ChunkHolder()

        addOrRemoveGroup = WidgetGroup(title="Add / Remove")

        self.add_btn = QPushButton("Add")
        self.remove_btn = QPushButton("Delete")

        self.add_widgets_to_window(
            self.label,
            self.chunk_holder,

            addOrRemoveGroup.add_widgets_to_group(
                self.remove_btn,
                self.add_btn,
                layout="H"
            )
        )
