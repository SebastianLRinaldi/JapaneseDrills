from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.helper_classes.shuffle_que import ShuffleQueue
from .blueprint import Blueprint

from japanese_verb_conjugator_v2 import Formality, Polarity, Tense, VerbClass, JapaneseVerbFormGenerator as jvfg


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
Instead of needing to sumbit words with enter if the word is 
correct it will show as green play a nice ding sounds 
then wait like 1 second then load a new conjugation
"""
class Logic(Blueprint):

    def __init__(self, component):
        super().__init__()
        self._map_widgets(component)
        self.component = component
        self.current_conjugation = ""



    def make_conjugation(self):
        self.current_conjugation = jvfg.generate_plain_form("飲む", VerbClass.GODAN, Tense.PAST, Polarity.POSITIVE) 
        self.conjugation_label.setText(self.current_conjugation )

    def update_color(self):
        text = self.typing_area.text()
        # if text ==  :
        #     self.typing_area.setStyleSheet("color:red; font-size: 64pt;")
        if text == self.current_conjugation:
            self.typing_area.setStyleSheet(f"color: green; ; font-size: 64pt;")
        else:
            self.typing_area.setStyleSheet("color:white; font-size: 64pt;")
            self.shake_line_edit()

    
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