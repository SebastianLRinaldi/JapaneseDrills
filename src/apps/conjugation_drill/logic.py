from enum import Enum
from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *
from numpy import empty

from src.helper_classes.shuffle_que import ShuffleQueue
from .blueprint import Blueprint

import random
from japanese_verb_conjugator_v2 import Formality, Polarity, Tense, VerbClass, BaseForm, Formality, JapaneseVerbFormGenerator as jvfg
from japanese_verb_conjugator_v2 import generate_japanese_verb_form

"""
Close methods
Ctrl+k + Ctrl+0

Open Methods 
Ctrl+k + Ctrl+J
"""


verb_conjugations = [
    # ─── Basic Forms ───
    # "Dictionary Form",
    # "ます Form / Polite",

    # ─── Te-form ───
    # "て Form",

    # ─── Tense / Polarity ───
    # "た : Past",
    # "ない : Negative",
    # "なかった : Past Negative",
    # "ません : Polite Negative",
    # "ました : Polite Past",
    # "ませんでした : Polite Past Negative",

    # ─── Desire / Intention ───
    # "たい : Want to / Desiderative",
    # "たくない : Don't want to /  Negative Desiderative",
    # "たかった : Wanted to",
    # "たくなかった : Didn't want to"

    # "てほしい : Want (someone) to do",
    # "てほしくない : Don’t want (someone) to do",
    # "てほしかった : Wanted (someone) to do",
    # "てほしくなかった : Didn’t want (someone) to do",
    
    # "たがる : Someone Else's Desire",
    

    # ─── Progressive / Resulting State ───
    "ている : Progressive / Resulting State",         # is doing / has done (result state)
    # "ていない : Negative Progressive",                # isn’t doing / hasn’t done
    # "ていた : Past Progressive",                      # was doing / had done
    # "ていなかった : Past Negative Progressive",       # wasn’t doing / hadn’t done

    # "ています : Polite Progressive",
    # "ていません : Polite Negative Progressive",
    # "ていました : Polite Past Progressive",
    # "ていませんでした : Polite Past Negative Progressive",

    # ─── Connective Forms ───
    # "ながら Form : Simultaneous 'while doing'",
    # "たり Form : Example listing of Actions",
    # "Conditional (〜ば / 〜たら / 〜なら)",


    # ─── Volitional ─── # "Volitional (〜う / 〜よう)",
    # "よう : Volitional (casual)",
    # "ましょう : Polite Volitional",

    # ─── Imperative ───
    # "ろ / え : Imperative (casual)",
    # "なさい : Polite Imperative",
    # "な : Negative Command",

    # ─── Conditional ───
    # "ば : Conditional",
    # "たら : Past Conditional",
    # "なら : Hypothetical Conditional",

    # ─── Potential ───     # "Potential (〜れる / 〜られる)",
    # "られる / える : Potential",

    # ─── Passive ───     # "Passive (〜れる / 〜られる)", 
    # "られる : Passive", #Can do (ability)

    # ─── Causative ───
    # "せる / させる : Causative",

    # ─── Causative-Passive ───
    # "させられる : Causative-Passive", # Be made to do



    # ─── Auxiliary Constructions ───
    # "やすい : Easy to do",
    # "やすくない : Not easy to do",
    # "やすかった : Was easy to do",
    # "やすくなかった : Wasn’t easy to do",

    # "にくい : Hard to do",
    # "にくくない : Not hard to do",
    # "にくかった : Was hard to do",
    # "にくくなかった : Wasn’t hard to do",


    # ─── Optional Extras ───
    # "Completion (〜てしまう)",
    # "すぎる : Overdo / too much",
    # "てみる : Try doing",
    # "てしまう : Finish doing / Do completely",
    # "ちゃう : Finish doing (casual)",
    # "なければならない : Must do",
    # "ておく : Do in advance / prepare",
    # "とく : Do in advance (casual)",
    # "たりする : Do things like / etc.",
    # "たりする : Do things like / etc.",
    # etc.
]

adj_conjugations = [
    # "Plain",
    "Negative",
    "Negative Past",
    "Past",
    "Te-form",
    "Adverbial",
]

conjugations_map = {
    "Godan": verb_conjugations,
    "Ichidan": verb_conjugations,
    "Irregular": ["する", "来る"],
    "Godan + Ichidan": verb_conjugations,
    "All Verb Types": verb_conjugations,
    "い-Adjective": adj_conjugations,
    "な-Adjective": adj_conjugations,
    "い-Adjective + な-Adjective": adj_conjugations,
}





"""
Load all conjugations 
"""
class Logic(Blueprint):

    def __init__(self, component:QWidget):
        super().__init__()
        self._map_widgets(component)
        self.component = component

        self.question_count = 0

        self.current_word = ""
        self.current_word_tag = ""
        self.current_conjugation = ""

        self.verb_word_queue = []
        self.base_form_queue = []
        self.polarity_queue = []

        self.base_form_idx = 0
        self.polarity_idx = 0
        
        self.populate_combo_from_enum()
        self.set_up_queues()
        self.reset_typing_area()

    def reset_typing_area(self):
        self.typing_area.setStyleSheet(f"color: white; font-size: 128pt;")
        self.typing_area.clear()
    
    def populate_combo_from_enum(self):
        combos = {
            self.verb_class_combo : VerbClass, # Based on the input word
            self.base_form_combo:BaseForm, # what base conjugation you want
            self.polarity_combo: Polarity, # pos, neg
            self.formality_combo: Formality, # plain vs polite but will be set as option
            
        }

        for combo, enum_cls in combos.items():
            combo.clear()
            for member in enum_cls:
                combo.addItem(member.name, member)
    def grab_vocab_words(self):
        fetcher = self.verb_list.logic.update_words_taged()
        fetcher.finished.connect(self.set_up_word_queue)
        return fetcher


    def set_up_word_queue(self):
        words = self.verb_list.logic.word_dict_tagged
        print(words)
        self.verb_word_queue = ShuffleQueue(words)

    def set_up_queues(self):
        count = self.base_form_combo.count()
        self.base_form_queue = ShuffleQueue([2, 3])#ShuffleQueue(random.sample(range(count), count))

        count = self.polarity_combo.count()
        self.polarity_queue = ShuffleQueue([0]) #ShuffleQueue(random.sample(range(count), count))

        self.base_form_idx = self.base_form_queue.next()
        self.polarity_idx = self.polarity_queue.next()

    def check_conjugation_to_input(self):
        text = self.typing_area.text()
        if text == self.current_conjugation:
            self.correct_anwser_animation()
        else:
            self.wrong_anwser_animation()

    def check_then_next_conjugation(self):
        if not self.verb_word_queue:
            self.vocab_label.setText("SYNCING")
            fetecher = self.grab_vocab_words()
            fetecher.finished.connect( self.next_conjugation)
        else:
            self.next_conjugation()



    def next_conjugation(self):
        self.current_word, self.current_word_tag = self.verb_word_queue.next()
        if self.current_word_tag == "godan":
            self.verb_class_combo.setCurrentIndex(0)
        elif self.current_word_tag == "ichidan":
            self.verb_class_combo.setCurrentIndex(1)
        elif self.current_word_tag == "irregular":
            self.verb_class_combo.setCurrentIndex(2)
        else:
            print(f"{self.current_word_tag}: is NOT A VALID TAG")


        self.vocab_label.setText(self.current_word)

        self.base_form_idx = self.base_form_queue.next()
        
        self.base_form_combo.setCurrentIndex(self.base_form_idx)

        self.make_conjugation()
        self.update_words_left()


    def make_conjugation(self):
        verb_class = self.verb_class_combo.currentData()
        base_form = self.base_form_combo.currentData()

        self.polarity_combo.setCurrentIndex(self.polarity_idx)
        self.polarity_idx = self.polarity_queue.next()
        

        if base_form in {BaseForm.PLAIN, BaseForm.POLITE}:
            self.polarity_combo.setCurrentIndex(1)
            kwargs = {
                "polarity": self.polarity_combo.currentData(),
                "tense": Tense.NONPAST
            }

        elif base_form in {BaseForm.TE, BaseForm.TA}:
            kwargs = {
                "formality": Formality.PLAIN,
                "polarity": self.polarity_combo.currentData()
            }

        self.current_conjugation = generate_japanese_verb_form(
            verb=self.current_word,
            verb_class=verb_class,
            base_form=base_form,
            **kwargs
        )
        print(f"{self.current_word} : {self.current_word_tag} | {verb_class} | {self.current_conjugation} | kwargs:{kwargs}")

    def update_words_left(self):
        total = len(self.verb_list.logic.word_dict_tagged)
        self.word_count_label.setText(f"{self.question_count} /{total}")
        self.question_count += 1

        
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
            self.typing_area.setTextMargins(0, 0, 0, 0)
            self.typing_area.setStyleSheet("color: white; font-size: 128pt;")

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
                self.check_then_next_conjugation()

            rev.finished.connect(cleanup)

            rev.start()
            self.typing_area._correct_flash_reverse = rev

        animation.finished.connect(reverse_animation)


        animation.start()
        self.typing_area._correct_flash = animation

















        


    # def handle_good(self):
    #     self.typing_area.setStyleSheet("color: green")

    # def handle_wrong(self):
    #     self.typing_area.setStyleSheet("color: red")


    # def update_labels(self, selected_type):
    #     vocab_list = self.vocab_map.get(selected_type, [])
    #     conjugation_list = conjugations_map.get(selected_type, [])

    #     if not vocab_list or not conjugation_list:
    #         self.vocab_label.setText("No vocab")
    #         self.conjugation_label.setText("No conjugations")
    #         return

    #     if selected_type not in self.vocab_queues:
    #         self.vocab_queues[selected_type] = ShuffleQueue(vocab_list)
    #     if selected_type not in self.conj_queues:
    #         self.conj_queues[selected_type] = ShuffleQueue(conjugation_list)

    #     vocab = self.vocab_queues[selected_type].next()
    #     conj_type = self.conj_queues[selected_type].next()

    #     print(f"VQUE: {self.vocab_queues[selected_type]}")
    #     print(f"VQUE: {self.conj_queues[selected_type]}")

    #     self.vocab_label.setText(vocab)
    #     self.conjugation_label.setText(f"→ {conj_type}")
    #     self.typing_area.clear()
    #     self.typing_area.setStyleSheet("")

    # def randomize(self):
    #     selected_type = self.word_type_combo.currentText()

    #     vocab_list = self.vocab_map.get(selected_type, [])
    #     conjugation_list = conjugations_map.get(selected_type, [])

    #     if not vocab_list or not conjugation_list:
    #         self.vocab_label.setText("No vocab")
    #         self.conjugation_label.setText("No conjugations")
    #         return

    #     if selected_type not in self.vocab_queues:
    #         self.vocab_queues[selected_type] = ShuffleQueue(vocab_list)
    #     if selected_type not in self.conj_queues:
    #         self.conj_queues[selected_type] = ShuffleQueue(conjugation_list)

    #     vocab = self.vocab_queues[selected_type].next()
    #     conj_type = self.conj_queues[selected_type].next()

    #     print(f"VQUE: {self.vocab_queues[selected_type]}")
    #     print(f"VQUE: {self.conj_queues[selected_type]}")

    #     self.vocab_label.setText(vocab)
    #     self.conjugation_label.setText(f"→ {conj_type}")
    #     self.typing_area.clear()
    #     self.typing_area.setStyleSheet("")

    
    """
    from old src code
    """
    # def center_notification(self):
    #     parent_size = self.conjugationdrill_ui.size()
    #     label_size = self.notification_label.size()

    #     x = (parent_size.width() - label_size.width()) // 2
    #     y = (parent_size.height() - label_size.height()) // 2

    #     self.notification_label.move(x, y)


    # def init_notification(self):
    #     # Call this once in your UI setup
    #     self.notification_label = QLabel(self.conjugationdrill_ui)
    #     self.notification_label.setStyleSheet("""
    #         background-color: #333;
    #         color: white;
    #         padding: 20px 40px;
    #         border-radius: 12px;
    #         font-size: 18pt;
    #         font-weight: bold;
    #     """)
    #     self.notification_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    #     self.notification_label.resize(self.conjugationdrill_ui.width(), 60)
    #     self.notification_label.move(0, 0)
    #     self.notification_label.setVisible(False)  # hidden by default
    #     self.notification_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)  # Pass clicks through

    # def show_loading(self):
    #     self.notification_label.setText("Loading from Anki...")
    #     self.notification_label.setVisible(True)
    #     self.notification_label.raise_()
    #     self.center_notification()


    # def show_finished(self):
        
    #     self.notification_label.setText("Fetch completed!")
    #     self.notification_label.raise_()
    #     self.center_notification()

    #     # Hide after 2 seconds
    #     QTimer.singleShot(2000, lambda: self.notification_label.setVisible(False))



    # def fetch(self):
    #     self.init_notification()
    #     self.show_loading()
        
    #     verb_logic = self.vocabranomizer_logic.verbs_logic
    #     adjective_logic = self.vocabranomizer_logic.adjectives_logic
    #     drills_map = self.conjugationdrill_logic.vocab_map

    #     # Create closures for verb/adjective logic
    #     def get_all_vocab_map():
            
    #         return {
    #             "Godan": verb_logic.get_verbs_by_type("godan") or [],
    #             "Ichidan": verb_logic.get_verbs_by_type("ichidan") or [],
    #             "Irregular": verb_logic.get_verbs_by_type("irregular") or [],
    #             "い-Adjective": adjective_logic.get_adjectives_by_type("i-adjective") or [],
    #             "な-Adjective": adjective_logic.get_adjectives_by_type("na-adjective") or [],
    #         }

    #     def set_vocab_map(result):
    #         self.show_finished()
    #         drills_map["Godan"] = result["Godan"]
    #         drills_map["Ichidan"] = result["Ichidan"]
    #         drills_map["Irregular"] = result["Irregular"]

    #         # Combine AFTER assigning
    #         drills_map["Godan + Ichidan"] = drills_map["Godan"] + drills_map["Ichidan"]
    #         drills_map["All Verb Types"] = drills_map["Godan + Ichidan"] + drills_map["Irregular"]

    #         drills_map["い-Adjective"] = result["い-Adjective"]
    #         drills_map["な-Adjective"] = result["な-Adjective"]
    #         drills_map["い-Adjective + な-Adjective"] = drills_map["い-Adjective"] + drills_map["な-Adjective"]

    #     # Launch async fetch
    #     self.fetch_from_anki(get_all_vocab_map, set_vocab_map)