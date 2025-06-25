import sys, re


from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from PyQt6.QtWebEngineWidgets import QWebEngineView

from src.core.GUI.UiManager import *

# from .widgets.CUSTOMWIDGET import YOURWIDGET


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


"""
only issue that that when we type and dont commit with spcae and it converts to kanji then we typ eagain we get the kanji converted [g] or whatever the next key press is
"""


"""
TEST SUCCESS 

にほんご　=　日本語[にほんご]
たべます　=　食[た]べます
まっすぐ　=　真[ま]っ直[す]ぐ
おみせ　=　お店[みせ]
とうきょうたわー　=　東京[とうきょう]タワー

"""

class FuriganaEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        self._last_kana = ""
        self.viewer = None
        # self.preview_callback = preview_callback

    def set_viewer(self, viewer: QWebEngineView):
        self.viewer = viewer

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


        self.update_preview(self.toPlainText())

        # print("commit:", commit_text, "preedit:", preedit_text, "lastKana:", self._last_kana)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        self.update_preview(self.toPlainText())

    def update_preview(self, text):
        ruby_html = convert_brackets(text)
        ruby_html = ruby_html.replace('\n', '<br>')
        self.viewer.setHtml(wrap_in_html(ruby_html))







class Layout(UiManager):

    editor:  FuriganaEditor
    viewer: QWebEngineView
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Furigana IME Editor with QTextEdit")
        self.init_widgets()
        self.set_widgets()

        layout_data = [
            self.splitter('vertical',[
                "editor",
                "viewer"
            ]),
    
        ]

        self.apply_layout(layout_data)

    def init_widgets(self):
        annotations = getattr(self.__class__, "__annotations__", {})
        for name, widget_type in annotations.items():
            widget = widget_type()
            setattr(self, name, widget)

    def set_widgets(self):
        self.editor.set_viewer(self.viewer)
        



    # def __init__(self):
    #     super().__init__()
    #     self.setWindowTitle("Furigana IME Editor with QTextEdit")

    #     layout = QVBoxLayout(self)

    #     self.editor = FuriganaEditor()
    #     self.viewer = QWebEngineView()

    #     layout.addWidget(self.editor)
    #     layout.addWidget(self.viewer)










    

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