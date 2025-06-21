from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *


from src.core.GUI.UiManager import *

# from .widgets.CUSTOMWIDGET import YOURWIDGET


class ConjugationRandomizerLayout(UiManager):
    count_conjugations_spinbox: QSpinBox
    count_auxiliaries_spinbox: QSpinBox
    count_inflections_spinbox: QSpinBox
    
    auxiliaries_list: QListWidget
    inflections_list: QListWidget
    conjugations_list: QListWidget  

    conjugations_set_all_btn: QPushButton
    conjugations_random_btn: QPushButton

    inflections_set_all_btn: QPushButton
    inflections_random_btn: QPushButton

    auxiliaries_set_all_btn: QPushButton
    auxiliaries_random_btn: QPushButton
    
    get_all_btn: QPushButton
    randomize_btn: QPushButton

    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.set_widgets()


        layout_data = [

            self.splitter("horizontal", [
                self.box("vertical", "Conjugations", [
                    "count_conjugations_spinbox",
                    "conjugations_list",
                    "conjugations_set_all_btn",
                    "conjugations_random_btn",
                ]),
                self.box("vertical", "Inflections", [
                    "count_inflections_spinbox",
                    "inflections_list",
                    "inflections_set_all_btn",
                    "inflections_random_btn",
                ]),
                self.box("vertical", "Auxiliaries", [
                    "count_auxiliaries_spinbox",
                    "auxiliaries_list",
                    "auxiliaries_set_all_btn",
                    "auxiliaries_random_btn",
                ]),
            ]),
            self.group("vertical", [
                "get_all_btn",
                "randomize_btn"
            ])
    
        ]

        self.apply_layout(layout_data)


    def init_widgets(self):
        for name, widget_type in self.__annotations__.items():
            widget = widget_type()
            setattr(self, name, widget)


    def set_widgets(self):

        self.get_all_btn.setText("SET ALL")
        self.randomize_btn.setText("RANDOMIZE ALL")

        self.auxiliaries_set_all_btn.setText("SET ALL AUXILIARIES")
        self.auxiliaries_random_btn.setText("RANDOM AUXILIARIES")

        self.inflections_set_all_btn.setText("SET ALL INFLECTIONS")
        self.inflections_random_btn.setText("RANDOM INFLECTIONS")

        self.conjugations_set_all_btn.setText("SET ALL CONJUGATIONS")
        self.conjugations_random_btn.setText("RANDOM CONJUGATIONS")

        self.count_auxiliaries_spinbox.setValue(5)
        self.count_inflections_spinbox.setValue(5)
        self.count_conjugations_spinbox.setValue(5)

        
        # forms = [
        #     "Dictionary form : 辞書形（じしょけい）",
        #     "Negative form : ない形",
        #     "Polite form : ます形",
        #     "Past polite / Negative polite : ました / ません",
        #     "Past form : た形",
        #     "Te-form : て形",
        #     "Progressive / Resultative (〜ing / has done) : ている形",
        #     "Potential form (can do) : 可能形",
        #     "Volitional form (let’s / I’ll) : 意向形",
        #     "Imperative / Command form : 命令形",
        #     "Prohibitive form (don’t do) : 禁止形",
        #     "Conditional (if...) : ば形",
        #     "Tara-form (if / when...) : たら形",
        #     "Passive form (be done) : 受け身形",
        #     "Causative form (make/let do) : 使役形",
        #     "Causative-passive (be made to do) : 使役受け身形",
        #     "Without doing : ないで形",
        #     "Don’t have to do : なくてもいい形",
        #     "Must do : なければならない形",
        #     "Have done / experience : ことがある形",
        #     "Hearsay / Looks like : そうだ形（伝聞・様態）",
        #     "Thinking of doing : ようと思う形",
        #     "Intend to do : つもり形",
        #     "Easy / Hard to do : にくい / やすい形",
        #     "Want to do : たい形",
        #     "Probably / I suppose : でしょう / だろう形",
        # ]
        # self.conjugations.addItems(forms)


        expressions = [
            "〜そうだ : Appears/seems like/Looks like (conjecture)",
            "〜らしい : Hearsay",
            "〜ようだ : Resemblance / Analogy / Metaphor",
            "〜なければならない : Must do / Obligation",
            "〜でしょう / 〜だろう : Probably / I guess"
        ]

        # Each tier represents a valid layer in the verb suffix pipeline
        auxiliary_stack_order = [
                                                            # [ Grammatical Aux Chain ]
            ["れる", "られる"],                              # 0 Potential / Passive
            ["せる", "させる"],                              # 1 Causative
            ["くれる", "くださる", "やる", "あげる"],         # 2 Benefactive
            ["たい", "たがる"],                              # 3 Desire
            ["ます"],                                        # 4 Politeness
            ["ない", "ぬ", "ん"],                            # 5 Negation
            ["た", "ている", "てしまう"],                     # 6 Tense / Aspect
                                                            # [ Modal Auxiliaries Chain ]
            ["そうだ", "ようだ"],                               # 7 Appearance / Evidential
            ["らしい"],                                        # 8 Hearsay
            ["まい", "まじ", "べき", "べし"],                   # 9 Epistemic Judgment
            ["やがる", "たがる"],                              # 🔟 Attitude
        ]

        # Master auxiliary_stack_order
        # Conceptual order — NOT all combinations are valid
        auxiliary_stack_order = [

            # 0. Core verb transformations (closest to verb stem)
            ["れる", "られる"],             # Potential / Passive
            ["せる", "させる"],             # Causative

            # 1. Grammatical modifications
            ["ない"],                      # Negation
            ["たい", "たがる"],            # Desire
            ["う", "よう"],                # Volitional
            ["ば"],                        # Conditional
            ["ろ", "よ"],                  # Imperative

            # 2. Tense and aspect
            ["た"],                        # Past
            ["ている"],                    # Progressive / Resultative
            ["てしまう"],                  # Completion / Regret
            ["ておく"],                    # Do in advance
            ["てみる"],                    # Try doing

            # 3. Benefactives and reception
            ["くれる", "くださる", "やる", "あげる", "もらう"],  # Giving / Receiving

            # 4. Politeness/formality
            ["ます"],                     # Polite
            ["です"],                     # Copula (used with ます-based forms)
            ["でございます"],             # Super polite variant

            # 5. Modal / evidential / judgment (often clause-final but fits here conceptually)
            ["そうだ"],                   # Looks like / Appears
            ["らしい"],                   # Hearsay
            ["ようだ"],                   # Seems like / Metaphorical resemblance
            ["ことがある"],               # Experience
            ["まい"],                     # Probably won't (negative volition)
            ["べき", "べし"],             # Should / Ought to
            ["なければならない"],         # Must / Obligation
            ["やがる"],                   # Displays someone's action with scorn/attitude
        ]

        auxiliary_stack_order = [
            # 0. Core morphological transformations (closest to stem)
            ["せる", "させる"],              # Causative
            ["れる", "られる"],              # Potential / Passive

            # 1. Desire and volitional
            ["たい", "たがる"],             # Desire (attaches before negation)
            ["う", "よう"],                 # Volitional

            # 2. Negation
            ["ない", "ぬ", "ん"],           # Negation

            # 3. Conditional and imperative
            ["ば"],                        # Conditional
            ["ろ", "よ"],                  # Imperative

            # 4. Past tense
            ["た"],                        # Past

            # 5. Te-form auxiliaries (attach via te-form, separate from suffix stacking)
            ["ている"],                    # Progressive / Resultative
            ["てしまう"],                  # Completion / Regret
            ["ておく"],                    # Do in advance
            ["てみる"],                    # Try doing

            # 6. Benefactives / Giving & receiving (treated as auxiliary verbs)
            ["くれる", "くださる", "やる", "あげる", "もらう"],

            # 7. Politeness
            ["ます"],                     # Polite suffix

            # 8. Copulas (separate words)
            ["です"],                     # Copula
            ["でございます"],             # Super polite copula

            # 9. Sentence-level modals / evidentials (not suffixes)
            ["そうだ"],                   # Appears / Evidential
            ["らしい"],                   # Hearsay
            ["ようだ"],                   # Metaphor / Resemblance
            ["ことがある"],               # Experience
            ["まい"],                     # Negative volition
            ["べき", "べし"],             # Should / Ought to
            ["なければならない"],         # Obligation / Must
            ["やがる"],                   # Displays attitude / contempt

        ]

        auxiliary_stack_n5 = [
            # 0. Core
            ["れる", "られる"],           # Potential

            # 1. Desire
            ["たい"],                    # Want to

            # 2. Negation
            ["ない"],                    # Negative

            # 3. Past
            ["た"],                      # Past

            # 4. Politeness
            ["ます"],                   # Polite

            # 5. Te-form auxiliaries
            ["ている"],                  # Progressive / resultative
            ["てみる"],                  # Try doing

            # 6. Giving/receiving (basic only)
            ["あげる", "もらう", "くれる"],

            # 7. Sentence mood / evidential
            ["そうだ"],                 # Seems like (visual)
            
            # (Optional for completeness)
            # ["です"] — Copula, not suffix stack, but used often
        ]

        auxiliary_stack_n4 = [
            # 0. Core
            ["れる", "られる"],           # Potential / Passive

            # 1. Causative
            ["せる", "させる"],           # Causative (often ends up in passive-causative combo)

            # 2. Desire / Volitional
            ["たい", "たがる"],          # Want to / they want to
            ["う", "よう"],              # Volitional

            # 3. Negation
            ["ない"],                   # Negative

            # 4. Past
            ["た"],                     # Past

            # 5. Politeness
            ["ます"],                  # Polite

            # 6. Te-form auxiliaries
            ["ている"],                 # Progressive / resultative
            ["てしまう"],               # Completion / regret
            ["ておく"],                 # Do in advance
            ["てみる"],                 # Try doing

            # 7. Benefactive / giving-receiving
            ["くれる", "あげる", "もらう"],

            # 8. Conditional / imperative
            ["ば"],                    # Conditional (formal)
            ["ろ", "よ"],              # Imperative

            # 9. Evidentials
            ["そうだ"],                # Seems like (visual + reported speech in N4)
            ["ようだ"],                # Appears / seems (based on inference)

            # 10. Copulas
            ["です"],                 # Polite copula
            ["でございます"],          # Very polite copula
        ]





        
        # for inflection in inflections:
        #     item = QListWidgetItem(inflection)
        #     item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        #     item.setCheckState(Qt.CheckState.Unchecked)
        #     self.inflections.addItem(item)

        # for auxiliary in auxiliaries:
        #     item = QListWidgetItem(auxiliary)
        #     item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        #     item.setCheckState(Qt.CheckState.Unchecked)
        #     self.auxiliaries.addItem(item)

        # for conjugation in conjugations:
        #     item = QListWidgetItem(conjugation)
        #     item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        #     item.setCheckState(Qt.CheckState.Unchecked)
        #     self.conjugations.addItem(item)