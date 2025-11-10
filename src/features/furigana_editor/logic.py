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



from src.core.event_handlers.undo_key_handler import UndoKeyHandler
from src.core.event_handlers.start_key_handler import StartKeyHandler
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

WORD_COLOR_MAP = {
    True: QColor(173, 216, 230),  # old word color
    False: QColor("white"),      # new word color
}

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

    def __init__(self, component:QWidget):
        super().__init__()
        self._map_widgets(component)
        self.component = component

        self.submitted_words = set()

        self.recall_tracker = RecallTracker()
        
        self.undo_handler = UndoKeyHandler(self.typing_area)
        self.typing_area.installEventFilter(self.undo_handler)

        self.start_handler = StartKeyHandler(self.typing_area)
        self.component.installEventFilter(self.start_handler)

    def start_session(self):
        self.recall_tracker.make_blank_session()
        self.session_start_btn.setDisabled(True)
        self.session_submit_btn.setDisabled(False)
        self.timer.logic.start_timer()
        self.timer.logic.enable_all()
        self.typing_area.setFocus()

    def end_session(self):
        self.session_start_btn.setDisabled(False)
        self.session_submit_btn.setDisabled(True)
        self.timer.logic.disable_all()

    def show_stats_window(self):
        old_count, new_count = self.recall_tracker.get_session_word_type_count()
        msg = StatsWindow(self.component)
        msg.logic.prepare_stats(self.prev_stats, self.recall_tracker.master_stats)
        msg.logic.prepare_best_stats(self.prev_stats,  old_count, new_count)
        msg.logic.build_table()
        msg.show()

    def submit_session(self):
        self.prev_stats = copy.deepcopy(self.recall_tracker.master_stats)

        # TODO add back in something like "\n".join(self.typing_area.text())
        # QApplication.clipboard().setText(self.typing_area.toPlainText())

        self.recall_tracker.process_session( self.timer.logic.get_time_str())

        self.show_stats_window()

        self.typing_area.clear()
        self.typing_history.clear()
        self.submitted_words.clear()
        self.recall_tracker.clear()
        self.end_session()


    def add_word(self):
        if self.timer.logic.time.isActive() and (word := self.typing_area.text()):

            already_in_history = word in self.submitted_words
            print(f"already_in_history={already_in_history}")

            ACTION_MAP = {
                True: self.shake_line_edit,
                False: self.add_word_to_history
            }
            ACTION_MAP[already_in_history]()


    def add_word_to_history(self):
        # Only create item when adding
        word = self.typing_area.text()
        is_old_word = word in self.recall_tracker.master_words
        color = WORD_COLOR_MAP[is_old_word]
        
        item = QListWidgetItem(word)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setForeground(QBrush(color))

        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        item.setFont(font)

        # Add item and finalize
        self.typing_history.addItem(item)
        self.submitted_words.add(word)
        self.recall_tracker.add_event_to_session(self.timer.logic.timer_duration, word)
        self.typing_history.scrollToBottom()
        self.typing_area.clear()
        self.update_history_word_count()

    def remove_word_from_history(self):
        count = self.typing_history.count()
        if count == 0:
            return  # nothing to undo
        
        # Get the last item
        last_item = self.typing_history.item(count - 1)
        word = last_item.text()
        self.submitted_words.discard(word)
        print(f"REMOVING: {word}")
        
        # Remove from QListWidget
        self.typing_history.takeItem(count - 1)

        self.recall_tracker.remove_event_from_session(word)
        self.update_color()
        self.update_history_word_count()


    def shake_line_edit(self):
        """
        Shakes the text inside a QLineEdit horizontally for a short animation effect.
        """
        # Define the horizontal shake pattern
        # shake_offsets = [0, 4, -4, 4, -4, 2, -2, 0] # OG
        shake_offsets = [0, 16, -16, 16, -16, 6, -6, 0]
        
        # Create a QVariantAnimation to animate the text margins
        animation = QVariantAnimation()
        animation.setDuration(300)  # total duration in milliseconds
        animation.setStartValue(0)
        animation.setEndValue(len(shake_offsets) - 1)
        animation.setEasingCurve(QEasingCurve.Type.InOutSine)

        # Update the left margin of the text for each animation step
        def on_value_changed(value):
            index = int(value)
            offset = shake_offsets[index]
            self.typing_area.setTextMargins(offset, 0, 0, 0)

        animation.valueChanged.connect(on_value_changed)

        # Reset margins to zero at the end
        animation.finished.connect(lambda: self.typing_area.setTextMargins(0, 0, 0, 0))

        # Start the animation and keep a reference alive
        animation.start()
        self.typing_area._animation = animation
                

    def update_color(self):
        text = self.typing_area.text()
        if text in self.submitted_words:
            self.typing_area.setStyleSheet("color:red; font-size: 64pt;")
        elif text in self.recall_tracker.master_words:
            self.typing_area.setStyleSheet(f"color: rgb(173, 216, 230); ; font-size: 64pt;")
        else:
            self.typing_area.setStyleSheet("color:white; font-size: 64pt;")

    def update_history_word_count(self):
        count = self.typing_history.count()
        self.word_count_label.setText(f"Word Count: {count}")