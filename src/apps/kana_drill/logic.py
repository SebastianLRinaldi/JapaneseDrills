from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

import json
from time import perf_counter
from src.helper_classes import kana_recall_tracker
from src.helper_classes.kana_recall_tracker import KanaRecallTracker
from src.helper_classes.shuffle_que import ShuffleQueue
from src.core.event_handlers.start_key_handler import StartKeyHandler
from .blueprint import Blueprint

"""
Close methods
Ctrl+k + Ctrl+0

Open Methods 
Ctrl+k + Ctrl+J
"""
"""
HIRIGANA 
KATAKANA
ALL KANA
- MAIN KANA, DAKUTEN KANA, COMBINATION KANA
- AIEUO
- MOST MISSED/LEAST MISSED    
"""

KANA = {
    "HIRAGANA": {
        "ALL KANA": {
            "MAIN KANA": {
                "A": {"あ":"a","か":"ka","さ":"sa","た":"ta","な":"na","は":"ha","ま":"ma","や":"ya","ら":"ra","わ":"wa"},
                "I": {"い":"i","き":"ki","し":"shi","ち":"chi","に":"ni","ひ":"hi","み":"mi","り":"ri"},
                "U": {"う":"u","く":"ku","す":"su","つ":"tsu","ぬ":"nu","ふ":"fu","む":"mu","ゆ":"yu","る":"ru"},
                "E": {"え":"e","け":"ke","せ":"se","て":"te","ね":"ne","へ":"he","め":"me","れ":"re"},
                "O": {"お":"o","こ":"ko","そ":"so","と":"to","の":"no","ほ":"ho","も":"mo","よ":"yo","ろ":"ro","を":"wo"},
                "N": {"ん":"n"}
            },

            "DAKUTEN KANA": {
                "A": {"が":"ga","ざ":"za","だ":"da","ば":"ba","ぱ":"pa"},
                "I": {"ぎ":"gi","じ":"ji","ぢ":"ji","び":"bi","ぴ":"pi"},
                "U": {"ぐ":"gu","ず":"zu","づ":"zu","ぶ":"bu","ぷ":"pu"},
                "E": {"げ":"ge","ぜ":"ze","で":"de","べ":"be","ぺ":"pe"},
                "O": {"ご":"go","ぞ":"zo","ど":"do","ぼ":"bo","ぽ":"po"}
            },

            "COMBINATION KANA": {
                "A": {
                    "きゃ":"kya","しゃ":"sha","ちゃ":"cha","にゃ":"nya","ひゃ":"hya",
                    "みゃ":"mya","りゃ":"rya","ぎゃ":"gya","じゃ":"ja","びゃ":"bya","ぴゃ":"pya"
                },
                "U": {
                    "きゅ":"kyu","しゅ":"shu","ちゅ":"chu","にゅ":"nyu","ひゅ":"hyu",
                    "みゅ":"myu","りゅ":"ryu","ぎゅ":"gyu","じゅ":"ju","びゅ":"byu","ぴゅ":"pyu"
                },
                "O": {
                    "きょ":"kyo","しょ":"sho","ちょ":"cho","にょ":"nyo","ひょ":"hyo",
                    "みょ":"myo","りょ":"ryo","ぎょ":"gyo","じょ":"jo","びょ":"byo","ぴょ":"pyo"
                }
            }
        }
    },

    "KATAKANA": {
        "ALL KANA": {
            "MAIN KANA": {
                "A": {"ア":"a","カ":"ka","サ":"sa","タ":"ta","ナ":"na","ハ":"ha","マ":"ma","ヤ":"ya","ラ":"ra","ワ":"wa"},
                "I": {"イ":"i","キ":"ki","シ":"shi","チ":"chi","ニ":"ni","ヒ":"hi","ミ":"mi","リ":"ri"},
                "U": {"ウ":"u","ク":"ku","ス":"su","ツ":"tsu","ヌ":"nu","フ":"fu","ム":"mu","ユ":"yu","ル":"ru"},
                "E": {"エ":"e","ケ":"ke","セ":"se","テ":"te","ネ":"ne","ヘ":"he","メ":"me","レ":"re"},
                "O": {"オ":"o","コ":"ko","ソ":"so","ト":"to","ノ":"no","ホ":"ho","モ":"mo","ヨ":"yo","ロ":"ro","ヲ":"wo"},
                "N": {"ン":"n"}
            },

            "DAKUTEN KANA": {
                "A": {"ガ":"ga","ザ":"za","ダ":"da","バ":"ba","パ":"pa"},
                "I": {"ギ":"gi","ジ":"ji","ヂ":"ji","ビ":"bi","ピ":"pi"},
                "U": {"グ":"gu","ズ":"zu","ヅ":"zu","ブ":"bu","プ":"pu"},
                "E": {"ゲ":"ge","ゼ":"ze","デ":"de","ベ":"be","ペ":"pe"},
                "O": {"ゴ":"go","ゾ":"zo","ド":"do","ボ":"bo","ポ":"po"}
            },

            "COMBINATION KANA": {
                "A": {
                    "キャ":"kya","シャ":"sha","チャ":"cha","ニャ":"nya","ヒャ":"hya",
                    "ミャ":"mya","リャ":"rya","ギャ":"gya","ジャ":"ja","ビャ":"bya","ピャ":"pya"
                },
                "U": {
                    "キュ":"kyu","シュ":"shu","チュ":"chu","ニュ":"nyu","ヒュ":"hyu",
                    "ミュ":"myu","リュ":"ryu","ギュ":"gyu","ジュ":"ju","ビュ":"byu","ピュ":"pyu"
                },
                "O": {
                    "キョ":"kyo","ショ":"sho","チョ":"cho","ニョ":"nyo","ヒョ":"hyo",
                    "ミョ":"myo","リョ":"ryo","ギョ":"gyo","ジョ":"jo","ビョ":"byo","ピョ":"pyo"
                }
            }
        }
    }
}



# class Logic(Blueprint):

#     def __init__(self, component:QWidget):
#         super().__init__()
#         self._map_widgets(component)
#         self.filename = "kana_mastery_progress.json"
#         self.progress = self.load_progress()  # keep in memory
#         self.component = component
#         self.question_count = 0
#         self.total_questions = 0
#         self.correct_question_count = 0
#         self.wrong_question_count = 0 
#         self.selected_kana_pairs = []
#         self.kana_recall_tracker = KanaRecallTracker()
#         self.current_kana_pair = None
#         # self.current_word_tag = ""
#         # self.current_conjugation = ""

#         self.question_queue:ShuffleQueue = ShuffleQueue([])
#         # self.base_form_queue = []
#         # self.polarity_queue = []

#         # self.base_form_idx = 0
#         # self.polarity_idx = 0
        
#         self.populate_script_combo()
#         self.populate_word_type_combo()
#         self.populate_vowel_selector()
#         self.get_selected_kana()
#         self.reset_typing_area()
#         self.start_handler = StartKeyHandler(self.typing_area)
#         self.component.installEventFilter(self.start_handler)

#     def reset_typing_area(self):
#         self.typing_area.setStyleSheet(f"color: white; font-size: 128pt;")
#         self.typing_area.clear()

    
#     def start_session(self):
#         # self.recall_tracker.make_blank_session()
#         # self.session_start_btn.setDisabled(True)
#         # self.session_submit_btn.setDisabled(False)
#         self.timer.logic.set_endurance_timer(True)
#         self.timer.logic.start_timer()
#         self.timer.logic.enable_all()
#         self.typing_area.setFocus()

#     def end_session(self):
#         # self.session_start_btn.setDisabled(False)
#         # self.session_submit_btn.setDisabled(True)
#         self.timer.logic.disable_all()

#     def populate_vowel_selector(self):
#         # Add the vowels
#         # self.vowel_selector.setItemAlignment(Qt.AlignmentFlag.AlignCenter)
#         for vowel in ["A","I","U","E","O","N"]:
#             item = QListWidgetItem(vowel)
#             item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
#             self.vowel_selector.addItem(item)


#     # --- Load progress from file ---
#     def load_progress(self):
        
#         try:
#             with open(self.filename, "r", encoding="utf-8") as f:
#                 return json.load(f)
#         except FileNotFoundError:
#             return {}

#     # --- Save progress to file ---
#     def save_progress(self):
#         with open(self.filename, "w", encoding="utf-8") as f:
#             json.dump(self.progress, f, ensure_ascii=False, indent=2)

        

#     # --- Update stats for a kana ---
#     def mark_kana(self, kana, correct=True):
#         if kana not in self.progress:
#             # initialize entry if missing
#             self.progress[kana] = {
#                 "meta": {"script": "", "category": "", "vowel": ""},
#                 "stats": {"correct": 0, "wrong": 0, "history": []}
#             }
#         stats = self.progress[kana]["stats"]
#         if correct:
#             stats["correct"] += 1
#             stats["history"].append(1)
#         else:
#             stats["wrong"] += 1
#             stats["history"].append(0)

#         self.save_progress()  # optional: can save less frequently for performance

#     # --- Access stats ---
#     def get_stats(self, kana):
#         return self.progress.get(kana, {"meta": {}, "stats": {}})

    
#     def populate_script_combo(self):
#         self.script_combo.clear()
#         self.script_combo.addItems(["ALL", "HIRAGANA", "KATAKANA"])

#     def populate_word_type_combo(self):
#         self.word_type_combo.clear()
#         self.word_type_combo.addItems(["ALL", "MAIN KANA", "DAKUTEN KANA","COMBINATION KANA"])


#     def get_selected_kana(self):
#         """
#         Returns a flat list of (kana, romaji) from the current selections:
#         - script_combo: "ALL", "HIRAGANA", "KATAKANA"
#         - word_type_combo: "ALL", "MAIN KANA", "DAKUTEN KANA", "COMBINATION KANA"
#         - text_input: vowel selector string e.g. "AIUEO"
#         """
#         items = []

#         # 1. Read current selections
#         script_sel = self.script_combo.currentText()                            # "ALL", "HIRAGANA", "KATAKANA"
#         category_sel = self.word_type_combo.currentText()                       # "ALL", "MAIN KANA", etc.
#         vowels = [item.text() for item in self.vowel_selector.selectedItems()]  # e.g., "AIUEO"

#         # 2. Determine which scripts to use
#         scripts = ["HIRAGANA", "KATAKANA"] if script_sel == "ALL" else [script_sel]

#         for script in scripts:
#             all_kana = KANA.get(script, {}).get("ALL KANA", {})

#             # 3. Determine which categories to use
#             categories = all_kana.keys() if category_sel == "ALL" else [category_sel]

#             for cat in categories:
#                 vowel_dicts = all_kana.get(cat, {})

#                 for vowel in vowels:
#                     group = vowel_dicts.get(vowel)
#                     if not group:
#                         continue
#                     # Add all kana/romaji in this vowel group
#                     items.extend(group.items())
#         self.selected_kana_pairs = items
#         self.update_questions()


#     def check_kana_to_input(self):
#         kana, eng = self.current_kana_pair
#         input_text = self.typing_area.text()
#         if input_text == eng:
#             self.question_count += 1 
#             self.correct_question_count += 1
#             self.mark_kana(kana, True)
#             self.update_question_count()
#             self.correct_anwser_animation()
#         else:
#             self.question_count += 1 
#             self.wrong_question_count += 1
#             self.mark_kana(kana, False)
#             self.update_question_count()
#             self.wrong_anwser_animation()


#     def update_question_count(self):
#         # Initialize percentages
#         pass_percent = fail_percent = 0.0

#         # Avoid division by zero
#         if self.question_count > 0:
#             pass_percent = (self.correct_question_count / self.question_count) * 100
#             fail_percent = (self.wrong_question_count / self.question_count) * 100

#         # Format the label text with 1 decimal place
#         self.pass_fail_label.setText(
#             f"PASS: {self.correct_question_count}/{self.question_count} ({pass_percent:.1f}%) | "
#             f"FAIL: {self.wrong_question_count}/{self.question_count} ({fail_percent:.1f}%)"
#         )
#         total = len(self.selected_kana_pairs)
#         self.question_count_label.setText(f"{self.question_count}/{total}")
        
        
    
#     def update_questions(self):
#         self.set_question_queue()
#         self.set_first_question()
#         self.update_question_count()

#     def set_question_queue(self):
#         if self.selected_kana_pairs:
#             self.question_queue = ShuffleQueue(self.selected_kana_pairs)

#     def set_first_question(self):
#         if self.question_queue.items:
#             self.set_next_question()

#     def set_next_question(self):
#         self.current_kana_pair = self.question_queue.next()
#         self.set_question_label()

#     def set_question_label(self):
#         kana, eng = self.current_kana_pair
#         self.question_label.setText(kana)
    
    
#     def wrong_anwser_animation(self):
#         """
#         Shows red text, performs a shake animation,
#         then restores white text and normal margins.
#         """
#         # Turn text red immediately
#         self.typing_area.setStyleSheet("color: red; font-size: 128pt;")

#         shake_offsets = [0, 16, -16, 16, -16, 6, -6, 0]

#         animation = QVariantAnimation()
#         animation.setDuration(300)
#         animation.setStartValue(0)
#         animation.setEndValue(len(shake_offsets) - 1)
#         animation.setEasingCurve(QEasingCurve.Type.InOutSine)

#         def on_value_changed(value):
#             index = int(value)
#             offset = shake_offsets[index]
#             self.typing_area.setTextMargins(offset, 0, 0, 0)

#         animation.valueChanged.connect(on_value_changed)

#         # Cleanup occurs AFTER shake
#         def cleanup():
#             self.reset_typing_area()
#             self.set_next_question()

#         animation.finished.connect(cleanup)

#         animation.start()
#         self.typing_area._wrong_animation = animation


#     def correct_anwser_animation(self):
#         """
#         Fast green flash + tiny pulse for a correct answer.
#         """
#         base_size = 128
#         peak_size = 134  # small pulse, very quick

#         animation = QVariantAnimation()
#         animation.setDuration(400)  
#         animation.setStartValue(0.0)
#         animation.setEndValue(1.0)
#         animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

#         def on_value_changed(v):
#             # v = 0.0 → 1.0
#             # Interpolate font size
#             size = base_size + (peak_size - base_size) * v

#             self.typing_area.setStyleSheet(
#                 f"color: green; font-size: {int(size)}pt;"
#             )

#         animation.valueChanged.connect(on_value_changed)

#         # Reverse at the end (returns to base size + white)
#         def reverse_animation():
#             rev = QVariantAnimation()
#             rev.setDuration(140)
#             rev.setStartValue(1.0)
#             rev.setEndValue(0.0)
#             rev.setEasingCurve(QEasingCurve.Type.InOutQuad)
#             rev.valueChanged.connect(on_value_changed)

#             def cleanup():
#                 self.reset_typing_area()
#                 self.set_next_question()

#             rev.finished.connect(cleanup)

#             rev.start()
#             self.typing_area._correct_flash_reverse = rev

#         animation.finished.connect(reverse_animation)


#         animation.start()
#         self.typing_area._correct_flash = animation



class Logic(Blueprint):

    def __init__(self, component:QWidget):
        super().__init__()
        self._map_widgets(component)
        self.component = component
        self.question_count = 0
        self.total_questions = 0
        self.correct_question_count = 0
        self.wrong_question_count = 0 
        self.selected_kana_pairs = []
        self.kana_recall_tracker = KanaRecallTracker()
        self.current_kana_pair = None
        self.question_start_time = None

        self.question_queue:ShuffleQueue = ShuffleQueue([])
        
        self.populate_script_combo()
        self.populate_word_type_combo()
        self.populate_vowel_selector()
        self.get_selected_kana()
        self.reset_typing_area()
        self.start_handler = StartKeyHandler(self.typing_area)
        self.component.installEventFilter(self.start_handler)

    def reset_typing_area(self):
        self.typing_area.setStyleSheet(f"color: white; font-size: 128pt;")
        self.typing_area.clear()

    def toggle_session(self):
        if self.timer.logic.time.isActive():
            self.end_session()
        else:
            self.start_session()
    
    def start_session(self):
        self.question_count = 0
        self.correct_question_count = 0
        self.wrong_question_count = 0
        self.update_question_count()
        script_sel, category_sel, vowels = self.get_current_selection()
        self.kana_recall_tracker.init_new_session(script_sel, category_sel, vowels)
        self.timer.logic.set_endurance_timer(True)
        self.timer.logic.start_timer()
        self.timer.logic.enable_all()
        self.typing_area.setFocus()
        self.set_first_question()
        self.typing_area.returnPressed.connect(self.check_kana_to_input)

    def end_session(self):
        self.timer.logic.stop_timer()
        self.timer.logic.disable_all()
        self.typing_area.returnPressed.disconnect(self.check_kana_to_input)
        self.kana_recall_tracker.finalize_master_from_session(self.timer.logic.remaining_time)
        self.kana_recall_tracker.finalize_session(self.timer.logic.remaining_time)

    def populate_vowel_selector(self):
        for vowel in ["A","I","U","E","O","N"]:
            item = QListWidgetItem(vowel)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.vowel_selector.addItem(item)

    def populate_script_combo(self):
        self.script_combo.clear()
        self.script_combo.addItems(["ALL", "HIRAGANA", "KATAKANA"])

    def populate_word_type_combo(self):
        self.word_type_combo.clear()
        self.word_type_combo.addItems(["ALL", "MAIN KANA", "DAKUTEN KANA","COMBINATION KANA"])

    def get_current_selection(self):
        script_sel = self.script_combo.currentText()                            # "ALL", "HIRAGANA", "KATAKANA"
        category_sel = self.word_type_combo.currentText()                       # "ALL", "MAIN KANA", etc.
        vowels = [item.text() for item in self.vowel_selector.selectedItems()]  # e.g., "AIUEO"
        return script_sel, category_sel, vowels
    
    def get_selected_kana(self):
        """
        Returns a flat list of (kana, romaji) from the current selections:
        - script_combo: "ALL", "HIRAGANA", "KATAKANA"
        - word_type_combo: "ALL", "MAIN KANA", "DAKUTEN KANA", "COMBINATION KANA"
        - text_input: vowel selector string e.g. "AIUEO"
        """
        items = []
        
        # 1. Read current selections
        script_sel, category_sel, vowels = self.get_current_selection()

        # 2. Determine which scripts to use
        scripts = ["HIRAGANA", "KATAKANA"] if script_sel == "ALL" else [script_sel]

        for script in scripts:
            all_kana = KANA.get(script, {}).get("ALL KANA", {})

            # 3. Determine which categories to use
            categories = all_kana.keys() if category_sel == "ALL" else [category_sel]

            for cat in categories:
                vowel_dicts = all_kana.get(cat, {})

                for vowel in vowels:
                    group = vowel_dicts.get(vowel)
                    if not group:
                        continue
                    # Add all kana/romaji in this vowel group
                    items.extend(group.items())
        self.selected_kana_pairs = items


    def check_kana_to_input(self):
        kana, eng = self.current_kana_pair
        input_text = self.typing_area.text()

        # Compute elapsed time
        elapsed_time = None
        elapsed_time_to_store = None
        if self.question_start_time is not None:
            elapsed_time = perf_counter() - self.question_start_time
            elapsed_time_rounded = round(elapsed_time, 3)
            self.question_start_time = None  # reset for next question
        
            # Only store time if correct
            elapsed_time_to_store = elapsed_time_rounded if input_text == eng else None

        if input_text == eng:
            self.question_count += 1 
            self.correct_question_count += 1
            self.kana_recall_tracker.add_event_to_session(self.timer.logic.remaining_time,
                                                            elapsed_time_to_store, 
                                                            self.current_kana_pair,
                                                            input_text)
            self.correct_anwser_animation()
        else:
            self.question_count += 1 
            self.wrong_question_count += 1
            self.kana_recall_tracker.add_event_to_session(self.timer.logic.remaining_time, 
                                                            elapsed_time_to_store, 
                                                            self.current_kana_pair, 
                                                            input_text)
            self.wrong_anwser_animation()

    def update_question_count(self):
        # Initialize percentages
        pass_percent = fail_percent = 0.0

        # Avoid division by zero
        if self.question_count > 0:
            pass_percent = (self.correct_question_count / self.question_count) * 100
            fail_percent = (self.wrong_question_count / self.question_count) * 100

        # Format the label text with 1 decimal place
        self.pass_fail_label.setText(
            f"PASS: {self.correct_question_count}/{self.question_count} ({pass_percent:.1f}%) | "
            f"FAIL: {self.wrong_question_count}/{self.question_count} ({fail_percent:.1f}%)"
        )
        total = len(self.selected_kana_pairs)
        self.question_count_label.setText(f"{self.question_count}/{total}")


    def continue_or_end_session(self):
        total = len(self.selected_kana_pairs)
        if self.question_count == total:
            self.question_label.setText("ready")
            self.end_session()
        else:
            self.set_next_question()

    def set_first_question(self):
        self.question_queue = ShuffleQueue(self.selected_kana_pairs)
        self.set_next_question()

    def set_next_question(self):
        self.current_kana_pair = self.question_queue.next()
        self.set_question_label()

    def set_question_label(self):
        kana, eng = self.current_kana_pair
        self.question_label.setText(kana)
        self.question_start_time = perf_counter()  # start timer here
    
    def wrong_anwser_animation(self):
        """
        Shows red text, performs a shake animation,
        then restores white text and normal margins.
        """
        # Turn text red immediately
        self.typing_area.setStyleSheet("color: red; font-size: 128pt;")

        shake_offsets = [0, 16, -16, 16, -16, 6, -6, 0]

        animation = QVariantAnimation()
        animation.setDuration(300)
        animation.setStartValue(0)
        animation.setEndValue(len(shake_offsets) - 1)
        animation.setEasingCurve(QEasingCurve.Type.InOutSine)

        def on_value_changed(value):
            index = int(value)
            offset = shake_offsets[index]
            self.typing_area.setTextMargins(offset, 0, 0, 0)

        animation.valueChanged.connect(on_value_changed)

        # Cleanup occurs AFTER shake
        def cleanup():
            self.reset_typing_area()
            self.update_question_count()
            self.continue_or_end_session()


        animation.finished.connect(cleanup)

        animation.start()
        self.typing_area._wrong_animation = animation


    def correct_anwser_animation(self):
        """
        Fast green flash + tiny pulse for a correct answer.
        """
        base_size = 128
        peak_size = 134  # small pulse, very quick

        animation = QVariantAnimation()
        animation.setDuration(400)  
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        def on_value_changed(v):
            # v = 0.0 → 1.0
            # Interpolate font size
            size = base_size + (peak_size - base_size) * v

            self.typing_area.setStyleSheet(
                f"color: green; font-size: {int(size)}pt;"
            )

        animation.valueChanged.connect(on_value_changed)

        # Reverse at the end (returns to base size + white)
        def reverse_animation():
            rev = QVariantAnimation()
            rev.setDuration(140)
            rev.setStartValue(1.0)
            rev.setEndValue(0.0)
            rev.setEasingCurve(QEasingCurve.Type.InOutQuad)
            rev.valueChanged.connect(on_value_changed)

            def cleanup():
                self.reset_typing_area()
                self.update_question_count()
                self.continue_or_end_session()

            rev.finished.connect(cleanup)

            rev.start()
            self.typing_area._correct_flash_reverse = rev

        animation.finished.connect(reverse_animation)


        animation.start()
        self.typing_area._correct_flash = animation