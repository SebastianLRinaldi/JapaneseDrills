from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.GUI.UiManager import *

# from .widgets.CUSTOMWIDGET import YOURWIDGET




from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPlainTextEdit, QTextEdit
import sys, re


from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPlainTextEdit
from PyQt6.QtWebEngineWidgets import QWebEngineView
import sys, re

def convert_brackets(text):
    return re.sub(r'([\u4e00-\u9fff]+)\[(.+?)\]', r'<ruby>\1<rt>\2</rt></ruby>', text)

def convert_braces(text):
    return re.sub(r'([\u4e00-\u9fff]+)\{(.+?)\}', r'<ruby>\1<rt>\2</rt></ruby>', text)

def convert_caret(text):
    return re.sub(r'([\u4e00-\u9fff]+)\^(.+?)', r'<ruby>\1<rt>\2</rt></ruby>', text)

def convert_aozora(text):
    return re.sub(r'｜([\u4e00-\u9fff]+)《(.+?)》', r'<ruby>\1<rt>\2</rt></ruby>', text)



def is_kana(text):
    return re.fullmatch(r'[ぁ-んァ-ンー]+', text)

def contains_kanji(text):
    return re.search(r'[\u4e00-\u9fff]', text)

def convert_curly_to_ruby(text):
    return re.sub(r'([\u4e00-\u9fff]+)\{(.+?)\}', r'<ruby>\1<rt>\2</rt></ruby>', text)

def wrap_in_html(ruby_body):
    return f"""
    <html><head><meta charset="UTF-8"><style>
    body {{ font-size: 24px; line-height: 2; }}
    ruby rt {{ font-size: 0.5em; }}
    </style></head><body>{ruby_body}</body></html>
    """


# def get_kana_for_kanji(commit_text, last_kana):
#     kanji_regex = re.compile(r'[\u4e00-\u9fff]')
#     kanji_chars = [c for c in commit_text if kanji_regex.match(c)]

#     # Extremely naive: divide kana evenly per kanji
#     # Assumes 1 kanji == 1+ kana reading
#     if not kanji_chars or not last_kana:
#         return []

#     kana_per_kanji = max(1, len(last_kana) // len(kanji_chars))
#     chunks = []
#     i = 0
#     for k in kanji_chars:
#         chunk = last_kana[i:i+kana_per_kanji]
#         chunks.append((k, chunk))
#         i += kana_per_kanji

#     return chunks

"""
Doesnt work with katakana
"""
def extract_kana_chunks(preedit, last_kana):
    chunks = []
    kanji_re = re.compile(r'[\u4e00-\u9fff]')
    i = 0  # index in last_kana
    current_chunk = ''

    for c in preedit:
        if kanji_re.match(c):
            # Start new chunk
            current_chunk = ''
            while i < len(last_kana):
                k = last_kana[i]
                if k in preedit:
                    break
                current_chunk += k
                i += 1
            if current_chunk:
                chunks.append(current_chunk)
        else:
            # Non-kanji in preedit, just move past it in kana
            if i < len(last_kana) and c == last_kana[i]:
                i += 1

    return chunks



"""
WORKS
"""
# def extract_kana_chunks(preedit, last_kana):
#     chunks = []
#     kanji_re = re.compile(r'[\u4e00-\u9fff\u30a0-\u30ff]')  # kanji + katakana #re.compile(r'[\u4e00-\u9fff]')
#     i = 0  # index in last_kana
#     current_chunk = ''

#     for c in preedit:
#         if kanji_re.match(c):
#             # Start new chunk
#             current_chunk = ''
#             while i < len(last_kana):
#                 k = last_kana[i]
#                 if k in preedit:
#                     break
#                 current_chunk += k
#                 i += 1
#             if current_chunk:
#                 chunks.append(current_chunk)
#         else:
#             # Non-kanji in preedit, just move past it in kana
#             if i < len(last_kana) and c == last_kana[i]:
#                 i += 1

#     return chunks







def _katakana_to_hiragana(s):
    out = ''
    for ch in s:
        code = ord(ch)
        # Katakana block → subtract 0x60
        if 0x30A1 <= code <= 0x30F3:
            out += chr(code - 0x60)
        else:
            out += ch
    return out

def extract_kana_chunks(preedit, last_kana):
    kanji = re.compile(r'[\u4e00-\u9fff]')
    # 1) Segment preedit into runs of Kanji vs non-Kanji
    segs = []
    cur = preedit[0]
    is_k = bool(kanji.match(cur))
    for ch in preedit[1:]:
        if bool(kanji.match(ch)) == is_k:
            cur += ch
        else:
            segs.append((is_k, cur))
            cur = ch
            is_k = not is_k
    segs.append((is_k, cur))

    # 2) Build (isKanji, text, translit) list
    proc = []
    for is_k, txt in segs:
        if not is_k:
            proc.append((False, txt, _katakana_to_hiragana(txt)))
        else:
            proc.append((True, txt, None))

    # 3) Walk through, slicing last_kana at each non-Kanji translit
    chunks = []
    pos = 0
    for idx, (is_k, txt, translit) in enumerate(proc):
        if is_k:
            # Kanji run: take everything up to the next translit boundary
            if idx+1 < len(proc) and proc[idx+1][2]:
                b = proc[idx+1][2]
                j = last_kana.find(b, pos)
                chunk = last_kana[pos:j]
                pos = j
            else:
                chunk = last_kana[pos:]
                pos = len(last_kana)
            if chunk:
                chunks.append(chunk)
        else:
            # Non-Kanji: skip its translit length
            pos += len(translit)

    return chunks





# def extract_kana_chunks(preedit, last_kana):
#     chunks = []
#     kanji_re = re.compile(r'[\u4e00-\u9fff]')
#     kana_re = re.compile(r'[\u3040-\u309f\u30a0-\u30ff]')  # hiragana + katakana
#     i = 0  # index in last_kana

#     for c in preedit:
#         if kanji_re.match(c):
#             current_chunk = ''
#             # accumulate kana chunk corresponding to this kanji
#             while i < len(last_kana):
#                 k = last_kana[i]
#                 # Stop if next last_kana char is kanji (unlikely) or when next char in preedit matches kana
#                 if kanji_re.match(k):
#                     break
#                 # Stop accumulating if next preedit char is kana or kanji? No, just accumulate all kana here
#                 # It's safer to stop accumulating if next preedit char is kanji or end of last_kana
#                 # So just accumulate until next kanji or end
#                 current_chunk += k
#                 i += 1
#             chunks.append(current_chunk)
#         elif kana_re.match(c):
#             # skip kana char in last_kana index as well
#             if i < len(last_kana) and last_kana[i] == c:
#                 i += 1
#         else:
#             # For other chars (punctuation, spaces), skip if matches
#             if i < len(last_kana) and last_kana[i] == c:
#                 i += 1

#     return chunks

"""
TEST SUCCESS 

にほんご　=　日本語[にほんご]
たべます　=　食[た]べます
まっすぐ　=　真[ま]っ直[す]ぐ
おみせ　=　お店[みせ]
とうきょうたわー　=　東京[とうきょう]タワー

"""

class FuriganaEditor(QTextEdit):
    def __init__(self, preview_callback):
        super().__init__()
        self._last_kana = ""
        self.preview_callback = preview_callback

    def inputMethodEvent(self, event: QInputMethodEvent):
        commit_text = event.commitString()
        preedit_text = event.preeditString()

        # Store preedit kana if it's only kana (no kanji)
        if preedit_text and not contains_kanji(preedit_text):
            self._last_kana = preedit_text

        if commit_text:
            # Let Qt handle the default commit first
            super().inputMethodEvent(event)
            print("1")
            if contains_kanji(commit_text) and self._last_kana:
                # Move cursor to end to avoid overwriting
                # cursor = self.textCursor()
                # cursor.movePosition(QTextCursor.MoveOperation.End)
                # self.setTextCursor(cursor)
                # # Insert just the {kana}
                # # Change the brackets here we change the converter for ruby
                # print(f"C: {commit_text} | P:{preedit_text} | LK:{self._last_kana}")
                # self.textCursor().insertText(f"[{self._last_kana}]")
                """
                WORKS
                """
                # cursor = self.textCursor()
                # for chunk in extract_kana_chunks(commit_text, self._last_kana):
                #     self.textCursor().insertText(f"[{chunk}]")
                #     print(chunk)
                
                # cursor.movePosition(QTextCursor.MoveOperation.End)
                # self.setTextCursor(cursor)

                """
                Works on singles kanji[tabe] + hiri not on groups (kanji+kanji+hiri)=kanji[tabetabe]+kanji+hiri
                """
                # chunks = extract_kana_chunks(commit_text, self._last_kana)
                # chunk_index = 0
                # kanji_re = re.compile(r'[\u4e00-\u9fff]')

                # cursor = self.textCursor()
                # # Move to beginning of commit_text
                # cursor.movePosition(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.MoveAnchor, len(commit_text))

                # for c in commit_text:
                #     cursor.movePosition(QTextCursor.MoveOperation.Right)
                #     if kanji_re.match(c) and chunk_index < len(chunks):
                #         cursor.insertText(f"[{chunks[chunk_index]}]")
                #         chunk_index += 1

                # # Finally, move cursor to end
                # cursor.movePosition(QTextCursor.MoveOperation.End)
                # self.setTextCursor(cursor)


                """
                Works on groups
                """
                chunks = extract_kana_chunks(commit_text, self._last_kana)
                chunk_index = 0
                kanji_re = re.compile(r'[\u4e00-\u9fff]')

                cursor = self.textCursor()
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
                self.setTextCursor(cursor)

            self._last_kana = ""  # Reset after commit
        else:
            # Allow Qt to show preedit underline and live IME text
            super().inputMethodEvent(event)


        self.preview_callback(self.toPlainText())

        # print("commit:", commit_text, "preedit:", preedit_text, "lastKana:", self._last_kana)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        self.preview_callback(self.toPlainText())







class Layout(UiManager):



    def __init__(self):
        super().__init__()
        self.setWindowTitle("Furigana IME Editor with QTextEdit")

        layout = QVBoxLayout(self)

        self.editor = FuriganaEditor(self.update_preview)
        self.viewer = QWebEngineView()

        layout.addWidget(self.editor)
        layout.addWidget(self.viewer)

        self.update_preview("")

    def update_preview(self, text):
        ruby_html = convert_brackets(text)
        self.viewer.setHtml(wrap_in_html(ruby_html))






    

    # name : QWidget
    
    # def __init__(self):
    #     super().__init__()
    #     self.init_widgets()

    #     layout_data = [
    
    #     ]

    #     self.apply_layout(layout_data)

    # def init_widgets(self):
    #     annotations = getattr(self.__class__, "__annotations__", {})
    #     for name, widget_type in annotations.items():
    #         widget = widget_type()
    #         setattr(self, name, widget)