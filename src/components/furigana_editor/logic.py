import re

from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.event_handlers.ime_handler import *
from src.core.event_handlers.space_key_handler import *
from src.helper_functions import *
from .blueprint import Blueprint

"""
Close methods
Ctrl+k + Ctrl+0

Open Methods 
Ctrl+k + Ctrl+J
"""


from PyQt6.QtCore import QObject, pyqtSignal, QEvent
from PyQt6.QtGui import QKeyEvent

class KeyPressSignalEmitter(QObject):
    keyPressed = pyqtSignal(int, str)          # key code, key text
    imePreedit = pyqtSignal(str)               # preedit string (composing)
    imeCommit = pyqtSignal(str)                # commit string (IME confirmed)

    def __init__(self, parent=None):
        super().__init__(parent)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            key_event: QKeyEvent = event
            key_code = key_event.key()
            key_text = key_event.text()
            self.keyPressed.emit(key_code, key_text)
            print(f"[KeyPress] code: {key_code}, text: '{key_text}'")
            return False  # let event pass through

        elif event.type() == QEvent.Type.InputMethod:
            ime_event: QInputMethodEvent = event
            preedit = ime_event.preeditString()
            commit = ime_event.commitString()
            if preedit:
                self.imePreedit.emit(preedit)
                print(f"[IME Preedit] '{preedit}'")
            if commit:
                self.imeCommit.emit(commit)
                print(f"[IME Commit] '{commit}'")
            return False  # let QTextEdit handle the input normally

        return False  # allow all other events



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

    def on_ime_event1(self, event: QInputMethodEvent):
        attrs = event.attributes()
        print(attrs)
        
        # if attrs and attrs[0].type == QInputMethodEvent.AttributeType.Cursor:
        #     cursor_attr = attrs[0]
        #     print(f"Cursor attribute start position: {cursor_attr.start}")
        # else:
        #     print("Cursor attribute not at index 0 or no attributes")


    def on_space_event(self):
        print("SPACE")



    def set_handler(self):
        self.ime_handler = IMEHandler(self.typing_area)
        self.typing_area.installEventFilter(self.ime_handler)
        self.ime_handler.imeEventReceived.connect(self.on_ime_event1)

        # self.space_handler = SpaceKeyHandler(self.typing_area)
        # self.typing_area.installEventFilter(self.space_handler)
        # self.space_handler.spacePressed.connect(self.on_space_event)


        # key_emitter = KeyPressSignalEmitter(self.typing_area)

        # # Install the filter on the widget
        # self.typing_area.installEventFilter(key_emitter)

        # # Connect to print any key pressed
        # key_emitter.keyPressed.connect(lambda code, text: print(f"Key code: {code}, text: '{text}'"))



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
