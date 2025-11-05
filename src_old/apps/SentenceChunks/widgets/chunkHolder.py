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


from src_old.core.GUI.UiManager import *

from src_old.core.EventHandlers.delete_key_handler import DeleteKeyHandler

class ChunkHolder(QListWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chunk Holder")

        self.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.setFlow(QListView.Flow.LeftToRight)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        self.delete_handler = DeleteKeyHandler(self)
        self.installEventFilter(self.delete_handler)


