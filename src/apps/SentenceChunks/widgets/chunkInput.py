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



from src.core.GUI.UiManager import *

# class ChunkInput(UiManager):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Media Controls")
#         self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint)


#         self.input_field = QLineEdit()
#         font = self.input_field.font()
#         font.setPointSize(16)  # Or whatever size you want, 16+ is decent for visibility
#         self.input_field.setFont(font)

        
#         self.type_field = QComboBox()
#         self.type_field.setFont(font)
#         self.type_field.addItems(["Kanji", "Kana", "Particle", "Verb Form", "Adjective", "Other"])


#         identifyGroup = WidgetGroup(title="Identify")


#         # Close button
#         self.close_btn = QPushButton("X")
#         self.close_btn .setFixedSize(20, 20)
#         self.close_btn .clicked.connect(self.handle_close)

        

#         self.add_widgets_to_window(
#             identifyGroup.add_widgets_to_group(
#                 self.input_field,
#                 self.type_field, 
#                 layout="H"
#             ),
#         )


    # def handle_close(self):
    #     self.setParent(None)
    #     self.deleteLater()


class ChunkInput(UiManager):
    input_field: QLineEdit
    type_field: QComboBox
    partical_field: QComboBox
    close_btn: QPushButton

    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.set_widgets()

        layout_data = [
            self.box( "horizontal", "chunk", [
                "input_field",
                "partical_field"
            ]),
            # "type_field", 
            # "close_btn"
        ]

        self.apply_layout(layout_data)
        self.setStyleSheet("background-color: transparent;")

    def init_widgets(self):
        for name, widget_type in self.__annotations__.items():
            setattr(self, name, widget_type())



    def set_widgets(self):
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint)
        

        font = QFont()
        font.setPointSize(16)
        self.input_field.setFont(font)
        self.type_field.setFont(font)
        self.partical_field.setFont(font)
        self.partical_field.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

        self.type_field.addItems(["Kanji", "Kana", "Particle", "Verb Form", "Adjective", "Other"])
        self.partical_field.addItems(["は", "が", "を", "に", "へ", "で", "と", "の", "も", "や",  "から", "まで", "でも", "けど", "か", "ます", "、", ""])
        self.partical_field.setCurrentIndex(-1)
        # self.partical_field.setEditable(True)
        self.close_btn.setText("X")
        self.close_btn.setFixedSize(20, 20)
        self.close_btn.clicked.connect(self.handle_close)
        

    def handle_close(self):
        self.setParent(None)
        self.deleteLater()