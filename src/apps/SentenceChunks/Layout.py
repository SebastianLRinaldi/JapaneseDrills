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



from src.core.GUI.UiManager import *

from .widgets.chunkInput import ChunkInput
from .widgets.chunkHolder import ChunkHolder 


"""
When you press enter after you type it should either go to the category selection or the next text box below
"""
class Layout(UiManager):

    example_label: QLabel
    sentence_structure_combo: QComboBox  # Added QComboBox
    chunk_holder: ChunkHolder
    add_btn: QPushButton
    remove_btn: QPushButton


    
    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.set_widgets()


        layout_data = [

                "example_label",
                "sentence_structure_combo",
                "chunk_holder",
                self.group("horizontal",["remove_btn", "add_btn"])
        ]
        
        
        self.apply_layout(layout_data )


    def init_widgets(self):
        for name, widget_type in self.__annotations__.items():
            widget = widget_type()
            setattr(self, name, widget)
            
    def set_widgets(self):

        example_text = """
        Step 1: Identify Each Character / Word
        Character/Word: ______ → What is it? (Kanji, kana, particle, verb form, etc.)
        Example: 猫 → Kanji for “cat”(List all components clearly)
        """
        self.example_label.setText(example_text)

        
        # Sentence structure options
        sentence_structures = [
            "Basic: [Time] + [Place] + [Subject] + [Object] + [How/Why] + [Verb]",
            "Omission: [Object] + [Verb] (subject/time/place dropped)",
            "WH-Question: [Subject] + [WH-Object] + [Verb]",
            "Yes/No Question: [Subject] + [Object] + [Verb] + (question particle)",
            "Command: [Verb]",
            "Command (with object): [Object] + [Verb]",
            "Description/State: [Time] + [Subject] + [How]",
            "Cause-Effect: [Why] + [Subject] + [Object] + [Verb]",
            "Relative Clause: [Clause: Time + Subject + Verb] + [Object (modified)] + [Verb]",
            "Nominalization: [Action + のは/ことは] + [How/Why] + [Verb]",
            "Emphasis/Inversion: [Object] + [Verb] + のは + [Subject] + だ",
            "Compound Sentences: [Clause 1 (any structure)] + [Conjunction] + [Clause 2 (any structure)]",
            "Passive/Causative: [Subject] + [Agent に] + [Verb (passive/causative form)]",
            "Embedded Quotation Clause: [Clause: Time + Subject + Object + How/Why + Verb] + と + [Verb of saying/thinking]",
            "Conditionals: [Clause (condition)] + [Main clause]",
            "Concessive: [Clause 1] + が/けれど/のに + [Clause 2]",
            "Simultaneous Actions: [Action 1 〜ながら/つつ] + [Action 2]",
            "Relative Clauses Nesting: [Clause 1] + [Clause 2] + [Noun] + [Verb]"
        ]
        self.sentence_structure_combo.addItems(sentence_structures)
        self.sentence_structure_combo.setEditable(False)


        self.add_btn.setText("ADD CHUNK")
        self.remove_btn.setText("REMOVE SELECTED CHUNK")