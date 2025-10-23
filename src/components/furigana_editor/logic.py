from multiprocessing.reduction import duplicate
import re
import os
from time import sleep
from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *
from enum import Enum
from collections import Counter

from src.core.event_handlers.enter_key_handler import EnterKeyHandler
from src.core.event_handlers.ime_handler import *
from src.core.event_handlers.space_key_handler import *
from src.helper_functions import *
from src.helper_classes import *
from .blueprint import Blueprint

"""
Close methods
Ctrl+k + Ctrl+0

Open Methods 
Ctrl+k + Ctrl+J
"""

class TimerPreset(Enum):
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

"""


class Logic(Blueprint):

    def __init__(self, component):
        super().__init__()
        self._map_widgets(component)
        self.component = component
        self.ime_handler = None
        self.space_handler = None
        self.set_handler()
        
        self._last_kana = ""
        font = self.typing_area.font()
        font.setPointSize(32)  
        self.typing_area.setFont(font)
        
        self.count_down_timer = QTimer()
        self.timer_count = TimerPreset.FIFTEEN.value

        self.recall_tracker = RecallTracker()
        self.my_highlighter = MyHighlighter(self.typing_area.document(), self.recall_tracker)


    def update_line_count(self):
        count = self.typing_area.document().lineCount()
        self.line_count_label.setText(f"Line: {count}")


    def get_time_str(self) -> str:
        minutes, seconds = divmod(self.timer_count, 60)
        return f"{minutes:02d}m:{seconds:02d}s" 


    def submit_session(self):
        text = self.typing_area.toPlainText()
        QApplication.clipboard().setText(self.typing_area.toPlainText())
        self.recall_tracker.process_session(text, self.get_time_str())
        self.typing_area.clear()


    def stop_timer(self):
        if self.count_down_timer.isActive():
            self.count_down_timer.stop()
            self.count_down_timer.timeout.disconnect(self.update_timer)
            self.toggle_timer_btn.setText("Start")


    def start_timer(self):
        if not self.count_down_timer.isActive():
            self.count_down_timer.start(1000)
            self.count_down_timer.timeout.connect(self.update_timer)
            self.toggle_timer_btn.setText("Stop")


    def update_timer(self):
        self.count_down_label.setText(self.get_time_str())
        if self.timer_count > 0:
            self.timer_count -= 1
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
        self.timer_count = TimerPreset.FIFTEEN.value
        self.count_down_label.setText("Ready?")
        






    def on_ime_event1(self, event: QInputMethodEvent):
        attrs = event.attributes()
        commit_text = event.commitString()
        preedit_text = event.preeditString()

        if preedit_text and not contains_kanji(preedit_text):
                self._last_kana = preedit_text

        # self.handle_chunk_conversion(event)
        # print("commit:", commit_text, "preedit:", preedit_text, "lastKana:", self._last_kana)

    def handle_chunk_conversion(self, event: QInputMethodEvent):
        commit_text = event.commitString()
        preedit_text = event.preeditString()
        
        if commit_text:
            
            if contains_kanji(commit_text) and self._last_kana:
                kana_pattern = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\uFF65-\uFF9F]+')
                kanji_pattern = re.compile(r'[\u4E00-\u9FFF\u3400-\u4DBF\uF900-\uFAFF]+')
                
                jap_chars_commited = re.findall(r'[一-龯]+|[^一-龯]+', commit_text)
                jap_chars_lastkana = re.findall(r'[一-龯]+|[^一-龯]+', self._last_kana)
                
                kana_list_commited = [x for x in jap_chars_commited  if kana_pattern.fullmatch(x)]
                kana_list_lastkana = [x for x in jap_chars_lastkana  if kana_pattern.fullmatch(x)]

                kanji_list = [x for x in jap_chars_commited if kanji_pattern.fullmatch(x)]
                extrated_kana_list = extract_kana_chunks(commit_text,self._last_kana)
                print("Committed Chunks:", jap_chars_commited)
                print("lastkana Chunks:", jap_chars_lastkana)

                print("Kana (Committed):", kana_list_commited)
                print("Kana (extrated_kana ):", extrated_kana_list)

                print("Kanji:", kanji_list)
                

                """
                commit text = 真っ直ぐ
                pred_text = まっすぐ
                chunks will be = [ま, す]


                for char in commit text
                    if kanji append first chunk in list then pop from list with "kanji_chunk[hiragana_chunk]"

                """

                # new_str = commit_text
                # for kanji, kana in zip(kanji_list, extrated_kana_list):
                #     new_str = new_str.replace(kanji, f"{kanji}[{kana}]", 1)

                new_str = ""
                for char in commit_text:
                    if kanji_list and char in kanji_list[0]:
                        kanji_chunk = kanji_list.pop(0)
                        print(f"kanji_chunk={kanji_chunk}")
                        kana_chunk = extrated_kana_list.pop(0)
                        print(f"kana_chunk={kana_chunk}")
                        new_str += f"{kanji_chunk}[{kana_chunk}]"
                    elif contains_kanji(char):
                        pass
                    else:
                        new_str += char
                    print(new_str)
                    
                        
                event.setCommitString(f"{new_str}")

                # i = 0
                # new_str = ""
                # while i < len(commit_text):
                #     c = commit_text[i]
                #     if kanji_re.match(c):
                #         start = i
                #         while i < len(commit_text) and kanji_re.match(commit_text[i]):
                #             i += 1
                #         # cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.MoveAnchor, i - start)
                #         if chunk_index < len(chunks):
                #             # cursor.insertText(f"[{chunks[chunk_index]}]")
                #             new_str = new_str + f"[{chunks[chunk_index]}]"
                #             chunk_index += 1
                #     else:
                #         # cursor.movePosition(QTextCursor.MoveOperation.Right)
                #         i += 1

                # event.setCommitString(f"{new_str}")

                # cursor.movePosition(QTextCursor.MoveOperation.End)
                # self.typing_area.setTextCursor(cursor)

            self._last_kana = ""  # Reset after commit


    def set_handler(self):
        self.ime_handler = IMEHandler(self.typing_area)
        self.typing_area.installEventFilter(self.ime_handler)
        self.ime_handler.imeEventReceived.connect(self.on_ime_event1)


    def on_ime_event(self, event: QInputMethodEvent):
        # self.on_ime_event1(event)

        commit_text = event.commitString()
        preedit_text = event.preeditString()

        print("commit:", commit_text, "preedit:", preedit_text, "lastKana:", self._last_kana)


    def on_ime_event2(self, event: QInputMethodEvent):
        commit_text = event.commitString()
        preedit_text = event.preeditString()

        # Store preedit kana if it's only kana (no kanji)
        if preedit_text and not contains_kanji(preedit_text):
            self._last_kana = preedit_text

        if commit_text:
            # Let Qt handle the default commit first
            self.typing_area.inputMethodEvent(event)
            if contains_kanji(commit_text) and self._last_kana:
                chunks = extract_kana_chunks(commit_text, self._last_kana)
                chunk_index = 0
                kanji_re = re.compile(r'[\u4e00-\u9fff]')

                cursor = self.typing_area.textCursor()
                cursor.movePosition(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.MoveAnchor, len(commit_text))

                i = 0
                while i < len(commit_text):
                    c = commit_text[i]
                    if kanji_re.match(c):
                        start = i
                        while i < len(commit_text) and kanji_re.match(commit_text[i]):
                            i += 1
                        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.MoveAnchor, i - start)
                        if chunk_index < len(chunks):
                            cursor.insertText(f"[{chunks[chunk_index]}]")
                            chunk_index += 1
                    else:
                        cursor.movePosition(QTextCursor.MoveOperation.Right)
                        i += 1

                cursor.movePosition(QTextCursor.MoveOperation.End)
                self.typing_area.setTextCursor(cursor)

            self._last_kana = ""  # Reset after commit
        else:
            # Allow Qt to show preedit underline and live IME text
            self.typing_area.inputMethodEvent(event)

        self.update_preview(self.typing_area.toPlainText())

        print("commit:", commit_text, "preedit:", preedit_text, "lastKana:", self._last_kana)

    def keyPressEvent(self, event):
        self.typing_area.keyPressEvent(event)
        self.update_preview(self.typing_area.toPlainText())

    def update_preview(self, text):
        ruby_html = convert_brackets(text)
        ruby_html = ruby_html.replace('\n', '<br>')
        self.viewer.setHtml(wrap_in_html(ruby_html))
