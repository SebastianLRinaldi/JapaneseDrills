import requests
import re
import html
import random

from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

"""
! Need to make it warn if anki is not open
! Need to make it auto open if not open
! Need to add option to where anki.exe is to open it
"""

class AnkiGrabber:
    def __init__(self):
        pass


    def get_notes_with_tag_and_mastery(self, tag, custom):
        payload = {
            "action": "findNotes",
            "version": 6,
            "params": {
                # "query": f'tag:{tag} (tag:status::understandable OR prop:cdn:{custom})'
                "query": f'"deck:Jap Mastery::Graduated" tag:{tag}'
            }
        }
        response = requests.post("http://localhost:8765", json=payload)
        response.raise_for_status()
        return response.json().get("result", [])



    def get_field(self, note_ids, field_name):
        if not note_ids:
            return {}

        payload = {
            "action": "notesInfo",
            "version": 6,
            "params": {
                "notes": note_ids
            }
        }
        response = requests.post("http://localhost:8765", json=payload)
        response.raise_for_status()
        notes_info = response.json().get("result", [])

        # Extract the field values
        result = {}
        for note in notes_info:
            fields = note.get("fields", {})
            if field_name in fields:
                result[note["noteId"]] = fields[field_name]["value"]
        return result

    def get_fields(self, note_ids, field_name):
            """
            Returns a dict mapping note_id -> {"value": field_value, "tags": note_tags}
            """
            if not note_ids:
                return {}

            payload = {
                "action": "notesInfo",
                "version": 6,
                "params": {
                    "notes": note_ids
                }
            }
            response = requests.post("http://localhost:8765", json=payload)
            response.raise_for_status()
            notes_info = response.json().get("result", [])

            result = {}
            for note in notes_info:
                fields = note.get("fields", {})
                if field_name in fields:
                    result[note["noteId"]] = {
                        "value": fields[field_name]["value"],
                        "tags": note.get("tags", [])
                    }
            return result

    def remove_anki_ruby(self, text):
        return re.sub(r'\[.*?\]', '', text)

    # def remove_anki_ruby(self, text):
    #     # Remove optional space + [furigana] after kanji
    #     return re.sub(r'(?<=[\u4e00-\u9fff])\s*\[[^\[\]]*?\]', '', text)
    def clean_html(self, raw_html, remove_spaces=True):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        cleantext = html.unescape(cleantext)  # converts &nbsp; to space
        if remove_spaces:
            cleantext = cleantext.replace(' ', '')
        return cleantext



    def fetch_from_anki(self, func, callback):
        thread = QThread()
        fetcher = Fetcher(func)
        fetcher.moveToThread(thread)

        def cleanup():
            fetcher.deleteLater()
            thread.deleteLater()
            self._threads.remove((thread, fetcher))

        thread.started.connect(fetcher.run)
        fetcher.finished.connect(callback)
        fetcher.finished.connect(thread.quit)
        thread.finished.connect(cleanup)

        if not hasattr(self, '_threads'):
            self._threads = []
        self._threads.append((thread, fetcher))

        thread.start()
        return fetcher


class Fetcher(QObject):
    finished = pyqtSignal(object)  # emit whatever the function returns

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        result = self.func(*self.args, **self.kwargs)
        self.finished.emit(result)
