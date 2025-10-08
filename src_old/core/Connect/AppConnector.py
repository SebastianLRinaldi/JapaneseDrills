from src_old.apps.SentenceChunks.Functions import Logic as SentencechunksLogic
from src_old.apps.VocabRanomizer.Functions import Logic as VocabranomizerLogic
from src_old.apps.ConjugationRandomizer.Functions import Logic as ConjugationrandomizerLogic
from src_old.apps.ConjugationGrid.Functions import Logic as ConjugationgridLogic
from src_old.apps.TextEditor.Functions import Logic as TexteditorLogic
from src_old.apps.ConjugationDrill.Functions import Logic as ConjugationdrillLogic
from src_old.apps.SceneMaker.Functions import Logic as ScenemakerLogic

from src_old.apps.SentenceChunks.Layout import Layout as SentencechunksLayout
from src_old.apps.VocabRanomizer.Layout import Layout as VocabranomizerLayout
from src_old.apps.ConjugationRandomizer.Layout import Layout as ConjugationrandomizerLayout
from src_old.apps.ConjugationGrid.Layout import Layout as ConjugationgridLayout
from src_old.apps.TextEditor.Layout import Layout as TexteditorLayout
from src_old.apps.ConjugationDrill.Layout import Layout as ConjugationdrillLayout
from src_old.apps.SceneMaker.Layout import Layout as ScenemakerLayout


from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

class AppConnector:
    sentencechunks_logic: SentencechunksLogic
    vocabranomizer_logic: VocabranomizerLogic
    conjugationrandomizer_logic: ConjugationrandomizerLogic
    conjugationgrid_logic: ConjugationgridLogic
    texteditor_logic: TexteditorLogic
    conjugationdrill_logic: ConjugationdrillLogic
    scenemaker_logic: ScenemakerLogic

    sentencechunks_ui: SentencechunksLayout
    vocabranomizer_ui: VocabranomizerLayout
    conjugationrandomizer_ui: ConjugationrandomizerLayout
    conjugationgrid_ui: ConjugationgridLayout
    texteditor_ui: TexteditorLayout
    conjugationdrill_ui: ConjugationdrillLayout
    scenemaker_ui: ScenemakerLayout

    def __init__(self, apps: dict, logic: dict):
        self.apps = apps
        self.logic = logic

        self.init_connections()
        # self.basic_ui.btn1.clicked.connect(self.second_logic.somefunction)
        self.conjugationdrill_ui.sync_btn.clicked.connect(self.fetch)




    # def fetch(self):
    #     # Fill combo types
    #     self.conjugationdrill_logic.vocab_map["Godan"] = self.vocabranomizer_logic.verbs_logic.get_verbs_by_type("godan")
    #     self.conjugationdrill_logic.vocab_map["Ichidan"] = self.vocabranomizer_logic.verbs_logic.get_verbs_by_type("ichidan")
    #     self.conjugationdrill_logic.vocab_map["Irregular"] = self.vocabranomizer_logic.verbs_logic.get_verbs_by_type("irregular")
    #     self.conjugationdrill_logic.vocab_map["Godan + Ichidan"] = self.conjugationdrill_logic.vocab_map["Godan"] + self.conjugationdrill_logic.vocab_map["Ichidan"]
    #     self.conjugationdrill_logic.vocab_map["All Verb Types"] = self.conjugationdrill_logic.vocab_map["Godan"] + self.conjugationdrill_logic.vocab_map["Ichidan"] + self.conjugationdrill_logic.vocab_map["Irregular"]

    #     # Leave adjective slots empty for now
    #     self.conjugationdrill_logic.vocab_map["い-Adjective"] = self.vocabranomizer_logic.adjectives_logic.get_adjectives_by_type("i-adjective")
    #     self.conjugationdrill_logic.vocab_map["な-Adjective"] = self.vocabranomizer_logic.adjectives_logic.get_adjectives_by_type("na-adjective")
    #     self.conjugationdrill_logic.vocab_map["い-Adjective + な-Adjective"] = (
    #         self.conjugationdrill_logic.vocab_map["い-Adjective"] + self.conjugationdrill_logic.vocab_map["な-Adjective"]
    #     )

    # def fetch(self):
        
    #     verb_logic = self.vocabranomizer_logic.verbs_logic
    #     adjective_logic = self.vocabranomizer_logic.adjectives_logic
    #     drills_map = self.conjugationdrill_logic.vocab_map

    #     # Verbs
    #     drills_map["Godan"] = verb_logic.get_verbs_by_type("godan") or []
    #     drills_map["Ichidan"] = verb_logic.get_verbs_by_type("ichidan") or []
    #     drills_map["Irregular"] = verb_logic.get_verbs_by_type("irregular") or []
    #     drills_map["Godan + Ichidan"] = drills_map["Godan"] + drills_map["Ichidan"]
    #     drills_map["All Verb Types"] = drills_map["Godan + Ichidan"] + drills_map["Irregular"]

    #     # Adjectives
    #     drills_map["い-Adjective"] = adjective_logic.get_adjectives_by_type("i-adjective") or []
    #     drills_map["な-Adjective"] = adjective_logic.get_adjectives_by_type("na-adjective") or []
    #     drills_map["い-Adjective + な-Adjective"] = drills_map["い-Adjective"] + drills_map["な-Adjective"]
    def center_notification(self):
        parent_size = self.conjugationdrill_ui.size()
        label_size = self.notification_label.size()

        x = (parent_size.width() - label_size.width()) // 2
        y = (parent_size.height() - label_size.height()) // 2

        self.notification_label.move(x, y)


    def init_notification(self):
        # Call this once in your UI setup
        self.notification_label = QLabel(self.conjugationdrill_ui)
        self.notification_label.setStyleSheet("""
            background-color: #333;
            color: white;
            padding: 20px 40px;
            border-radius: 12px;
            font-size: 18pt;
            font-weight: bold;
        """)
        self.notification_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.notification_label.resize(self.conjugationdrill_ui.width(), 60)
        self.notification_label.move(0, 0)
        self.notification_label.setVisible(False)  # hidden by default
        self.notification_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)  # Pass clicks through

    def show_loading(self):
        self.notification_label.setText("Loading from Anki...")
        self.notification_label.setVisible(True)
        self.notification_label.raise_()
        self.center_notification()


    def show_finished(self):
        
        self.notification_label.setText("Fetch completed!")
        self.notification_label.raise_()
        self.center_notification()

        # Hide after 2 seconds
        QTimer.singleShot(2000, lambda: self.notification_label.setVisible(False))



    def fetch(self):
        self.init_notification()
        self.show_loading()
        
        verb_logic = self.vocabranomizer_logic.verbs_logic
        adjective_logic = self.vocabranomizer_logic.adjectives_logic
        drills_map = self.conjugationdrill_logic.vocab_map

        # Create closures for verb/adjective logic
        def get_all_vocab_map():
            
            return {
                "Godan": verb_logic.get_verbs_by_type("godan") or [],
                "Ichidan": verb_logic.get_verbs_by_type("ichidan") or [],
                "Irregular": verb_logic.get_verbs_by_type("irregular") or [],
                "い-Adjective": adjective_logic.get_adjectives_by_type("i-adjective") or [],
                "な-Adjective": adjective_logic.get_adjectives_by_type("na-adjective") or [],
            }

        def set_vocab_map(result):
            self.show_finished()
            drills_map["Godan"] = result["Godan"]
            drills_map["Ichidan"] = result["Ichidan"]
            drills_map["Irregular"] = result["Irregular"]

            # Combine AFTER assigning
            drills_map["Godan + Ichidan"] = drills_map["Godan"] + drills_map["Ichidan"]
            drills_map["All Verb Types"] = drills_map["Godan + Ichidan"] + drills_map["Irregular"]

            drills_map["い-Adjective"] = result["い-Adjective"]
            drills_map["な-Adjective"] = result["な-Adjective"]
            drills_map["い-Adjective + な-Adjective"] = drills_map["い-Adjective"] + drills_map["な-Adjective"]

        # Launch async fetch
        self.vocabranomizer_logic.verbs_logic.fetch_from_anki(get_all_vocab_map, set_vocab_map)






        

    """
    This basically just does this part for us:
    
    class AppConnector:
        basic_ui: BasicLayout
        second_logic: SecondLogic

        def __init__(self, apps, logic):
            self.basic_ui = apps["Basic"]
            self.second_logic = logic["Second"]

            self.basic_ui.btn1.clicked.connect(self.second_logic.somefunction)
    """
    def init_connections(self):
        for name in self.apps:
            setattr(self, f"{name.lower()}_ui", self.apps[name])
            setattr(self, f"{name.lower()}_logic", self.logic[name])


