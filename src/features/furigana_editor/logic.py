from multiprocessing.reduction import duplicate
import pprint
import copy
import re
import os
from time import sleep
from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *
from enum import Enum
from collections import Counter

from src.components import stats_window
from src.core.event_handlers.enter_key_handler import EnterKeyHandler
from src.core.event_handlers.ime_handler import *
from src.core.event_handlers.space_key_handler import *
from src.helper_functions import *
from src.helper_classes import *
from .blueprint import Blueprint
from src.components import *
"""
Close methods
Ctrl+k + Ctrl+0

Open Methods 
Ctrl+k + Ctrl+J
"""

class TimerPreset(Enum):
    ZERO = 0
    TEST_FIVE = 5
    TEST_TEN = 10
    THIRTY = 30 * 60
    TWENTY_FIVE = 25 * 60
    FIFTEEN = 15 * 60
    TEN = 10 * 60


class MyHighlighter(QSyntaxHighlighter):
    def __init__(self, parent, recall_tracker: RecallTracker):
        super().__init__(parent)
        self.recall_tracker = recall_tracker

    def highlightBlock(self, text):
        whole = self.document().toPlainText()
        parsed_whole = whole.split()
        word_counts = Counter(parsed_whole)
        duplicates = {w for w, c in word_counts.items() if c > 1}
        non_unique = self.recall_tracker.master_words

        if duplicates:
            end = self.currentBlock().length()
            if text in duplicates:
                fmt = QTextCharFormat()
                fmt.setForeground(QColor("red"))
                self.setFormat(0, end, fmt)

        elif non_unique:
            end = self.currentBlock().length()
            if text in non_unique:
                fmt = QTextCharFormat()
                fmt.setForeground(QColor(173, 216, 230))
                self.setFormat(0, end, fmt)



"""
Need to add +/- 5 mins to timer
have default of 10-15-20-25-30 timers to choose from default to 15 or add settings for default
wpm avg

should show the increases in total recalled words, time spent, etc. after submit it pressed 
    (stats hidden after you press start on the timer then shown when stopped, so not to distract from recall)
    
Highest total of words and in what session
Highest total of unique words and in what session

A way to view stats over the sessions
A pop up after you submit a a session to show stats of session and maybe a simple compare to other sessions of improvement or decline 
would want to have an avg new words between sessions
would want avg word count per session

** Becauce the recall tracker is its own things now, we need to make a seperate app for the sentences and word writing with the [] for anki **

"""

class Logic(Blueprint):

    def __init__(self, component):
        super().__init__()
        self._map_widgets(component)
        self.component = component
        
        self.count_down_timer = QTimer()
        self.timer_count = TimerPreset.ZERO.value

        self.submitted_words = set()

        self.recall_tracker = RecallTracker()


    def get_time_str(self) -> str:
        minutes, seconds = divmod(self.timer_count, 60)
        return f"{minutes:02d}m:{seconds:02d}s" 

    def submit_session(self):
        self.prev_stats = copy.deepcopy(self.recall_tracker.master_stats)
        # QApplication.clipboard().setText(self.typing_area.toPlainText())

        self.recall_tracker.process_session( self.get_time_str())

        old_count, new_count = self.recall_tracker.get_session_word_type_count()
        msg = StatsWindow(self.component)
        msg.logic.prepare_stats(self.prev_stats, self.recall_tracker.master_stats)
        msg.logic.prepare_best_stats(self.prev_stats, new_count, old_count)
        msg.logic.build_table()
        msg.show()

        self.typing_area.clear()
        self.typing_history.clear()
        self.submitted_words.clear()
        self.recall_tracker.clear()

    def stop_timer(self):
        if self.count_down_timer.isActive():
            self.count_down_timer.stop()
            self.count_down_timer.timeout.disconnect(self.update_timer)
            self.toggle_timer_btn.setText("Start")

    def start_timer(self):
        if not self.count_down_timer.isActive():
            self.recall_tracker.make_blank_session()
            self.count_down_timer.start(1000)
            self.count_down_timer.timeout.connect(self.update_timer)
            self.toggle_timer_btn.setText("Stop")

    def update_timer(self):
        self.count_down_label.setText(self.get_time_str())
        if self.timer_count < TimerPreset.FIFTEEN.value:
            self.timer_count += 1
        else:
            self.reset_count_down_timer()
            msg = QMessageBox()
            msg.setWindowTitle("END OF SESSION")
            msg.setText("Time's up!")
            msg.setIcon(QMessageBox.Icon.Information)
            QTimer.singleShot(2000, msg.close)
            msg.exec()

    def toggle_timer(self):
        if self.count_down_timer.isActive():
            self.stop_timer()
        else:
            self.start_timer()

    def reset_count_down_timer(self):
        self.stop_timer()
        self.seconds_left = self.count_down_label.text()
        self.timer_count = TimerPreset.ZERO.value
        self.count_down_label.setText("Ready?")

    def add_word(self):
        word = self.typing_area.text()
        if word:
            item = QListWidgetItem(word)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            if word in self.recall_tracker.master_words:
                color = QColor(173, 216, 230)
            else:
                color = QColor("white")

            item.setForeground(QBrush(color))

            # Set large font
            font = QFont()
            font.setPointSize(16)
            font.setBold(True)
            item.setFont(font)

            # Add item
            self.typing_history.addItem(item)
            self.submitted_words.add(word)
            self.recall_tracker.add_event_to_session(self.timer_count, word)

            # Scroll to bottom automatically
            self.typing_history.scrollToBottom()
            self.typing_area.clear()

    def update_color(self, text: str):
        if text in self.submitted_words:
            self.typing_area.setStyleSheet("color:red")
        elif text in self.recall_tracker.master_words:
            self.typing_area.setStyleSheet(f"color: rgb(173, 216, 230);")
        else:
            self.typing_area.setStyleSheet("color:white")