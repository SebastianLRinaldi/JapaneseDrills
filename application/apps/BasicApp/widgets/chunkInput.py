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
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *

from application.FrontEnd.C_Grouper.SpliterGroupConfiguration import *
from application.FrontEnd.C_Grouper.TabGroupConfigureation import *
from application.FrontEnd.C_Grouper.widgetGroupFrameworks import *

from application.FrontEnd.D_WindowFolder.windowConfigureation import *

class ChunkInput(LayoutManager):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Media Controls")
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint)


        self.input_field = QLineEdit()
        font = self.input_field.font()
        font.setPointSize(16)  # Or whatever size you want, 16+ is decent for visibility
        self.input_field.setFont(font)

        
        self.type_field = QComboBox()
        self.type_field.setFont(font)
        self.type_field.addItems(["Kanji", "Kana", "Particle", "Verb Form", "Adjective", "Other"])


        identifyGroup = WidgetGroup(title="Identify")


        # Close button
        self.close_btn = QPushButton("X")
        self.close_btn .setFixedSize(20, 20)
        self.close_btn .clicked.connect(self.handle_close)

        

        self.add_widgets_to_window(
            identifyGroup.add_widgets_to_group(
                self.input_field,
                self.type_field, 
                layout="H"
            ),
        )


    def handle_close(self):
        self.setParent(None)
        self.deleteLater()