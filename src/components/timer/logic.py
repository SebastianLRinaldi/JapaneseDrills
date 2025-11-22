from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from enum import Enum

# from src.helpers import *
from .blueprint import Blueprint

"""
Close methods
Ctrl+k + Ctrl+0

Open Methods 
Ctrl+k + Ctrl+J
"""

class TimeValues(Enum):
    THIRTY = 30 * 60
    TWENTY_FIVE = 25 * 60
    FIFTEEN = 15 * 60
    TEN = 10 * 60
    FIVE = 5 * 60
    ZERO = 0

class TimerDirection(Enum):
    COUNT_DOWN = True # 15min -> 0
    COUNT_UP = False # 0 -> 15min

class Logic(Blueprint):

    def __init__(self, component):
        super().__init__()
        self._map_widgets(component)
        self.component = component
        
        self.time = QTimer()

        self.timer_duration = TimeValues.FIFTEEN.value
        self.timer_direction = TimerDirection.COUNT_UP
        self.remaining_time = TimeValues.ZERO.value

    def set_timer_duration(self, minutes: int = 0, seconds: int = 0):
        total_seconds = minutes * 60 + seconds
        if total_seconds <= 0:
            raise ValueError("Timer duration must be positive")
        self.timer_duration = total_seconds

    def set_timer_direction(self, count_down: bool):
        if count_down:
            self.timer_direction = TimerDirection.COUNT_DOWN
        else:
            self.timer_direction = TimerDirection.COUNT_UP

    def get_time_str(self) -> str:
        minutes, seconds = divmod(self.get_time_raw(), 60)
        return f"{minutes:02d}m:{seconds:02d}s" 

    def get_time_raw(self) -> int:
        return self.remaining_time 

    def stop_timer(self):
        if self.time.isActive():
            self.time.timeout.disconnect(self.update_tick)
            self.update_timer_label()
            self.time.stop()
            self.toggle_timer_btn.setText("Start")

    def start_timer(self):
        if not self.time.isActive():
            self.time.timeout.connect(self.update_tick)
            self.update_timer_label()
            self.time.start(1000)
            self.toggle_timer_btn.setText("Stop")

    def toggle_timer(self):
        if self.time.isActive():
            self.stop_timer()
        else:
            self.start_timer()

    def reset_count_down_timer(self):
        if self.timer_direction.value:
            self.remaining_time = self.timer_duration
        else:
            self.remaining_time = 0
        self.stop_timer()
        self.count_down_label.setText("Ready?")

    def update_tick(self):
        if self.timer_direction.value:  # COUNT_DOWN
            self.remaining_time -= 1
            self.update_timer_label()
            if self.remaining_time < 0:
                self.reset_count_down_timer()
                self.end_timer_msg()
        else:  # COUNT_UP
            self.remaining_time += 1
            self.update_timer_label()
            if self.remaining_time > self.timer_duration:
                self.reset_count_down_timer()
                self.end_timer_msg()

    def update_timer_label(self):
        self.count_down_label.setText(self.get_time_str())
        
    def end_timer_msg(self):
        msg = QMessageBox()
        msg.setWindowTitle("END OF SESSION")
        msg.setText("Time's up!")
        msg.setIcon(QMessageBox.Icon.Information)
        QTimer.singleShot(2000, msg.close)
        msg.exec()

    def disable_all(self):
        self.toggle_timer_btn.setDisabled(True)
        self.reset_timer_btn.setDisabled(True)
        self.count_down_label.setText("")

    def enable_all(self):
        self.toggle_timer_btn.setDisabled(False)
        self.reset_timer_btn.setDisabled(False)
        self.count_down_label.setText("Ready")
