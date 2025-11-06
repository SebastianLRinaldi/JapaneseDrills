import pprint
from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.helper_functions import compare_prev_to_current, format_duration
from .blueprint import Blueprint

"""
Close methods
Ctrl+k + Ctrl+0

Open Methods 
Ctrl+k + Ctrl+J
"""


class Logic(Blueprint):

    def __init__(self, component:QWidget):
        super().__init__()
        self._map_widgets(component)
        self.component = component
        self.stats = {}
        self.best_stats = {}
        self.DIFF_MAP = {1: ("green", "+"), -1: ("red", "-"), 0: ("white", "")}

    def close(self):
        self.component.close()

    def prepare_stats(self, prev_stats:dict, current_stats:dict):
        self.stats = {
            "Total Sessions": (prev_stats["total_sessions"], current_stats["total_sessions"]),
            "Total Recall Time": (prev_stats["total_recall_time"], current_stats["total_recall_time"]),
            "Total Words": (prev_stats["total_words"], current_stats["total_words"]),
            "Total Recall Count": (prev_stats["total_recall_count"], current_stats["total_recall_count"])
        }

    def prepare_best_stats(self, prev_stats:dict,  current_session_old_word_count, current_session_new_word_count,):
        self.best_stats = {
            "Best Total Count": (prev_stats["best_total_word_count"]["count"], current_session_old_word_count + current_session_new_word_count),
            "Best New Count": (prev_stats["best_new_word_count"]["count"], current_session_new_word_count),
            "Best Old Count": (prev_stats["best_old_word_count"]["count"], current_session_old_word_count),
        }

    def create_item(self, text="") -> QTableWidgetItem:
        return QTableWidgetItem(str(text))

    def compute_diff(self, name, prev, current):
        if name == "Total Recall Time":
            diff_value =  compare_prev_to_current(prev, current)
            diff_text = format_duration(abs(diff_value))
        else:
            diff_value = current - prev
            diff_text = abs(diff_value)
        return diff_value, diff_text

    def create_diff_item(self, name:str, prev:int, current:int):
        diff_item = self.create_item()
        diff_value, diff_text = self.compute_diff(name, prev, current)
        key = (diff_value > 0) - (diff_value < 0)
        color, sign = self.DIFF_MAP[key]
        diff_item.setForeground(QColor(color))
        diff_item.setText(f"{sign}{diff_text}")
        return diff_item

    def build_table(self):
        self.combo_stats = self.stats | self.best_stats
        for row, (name, (prev, current)) in enumerate(self.combo_stats.items()):
            name_item = self.create_item(name)
            prev_item = self.create_item(prev)
            diff_item = self.create_diff_item(name, prev, current)
            current_item = self.create_item(current)

            items: list[QTableWidgetItem] = [name_item, prev_item, diff_item, current_item]

            for col, item in enumerate(items):
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.stats_table.setItem(row, col, item)

