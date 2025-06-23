from src.apps.SentenceChunks.Functions import Logic as SentencechunksLogic
from src.apps.VocabRanomizer.Functions import Logic as VocabranomizerLogic
from src.apps.ConjugationRandomizer.Functions import Logic as ConjugationrandomizerLogic
from src.apps.ConjugationGrid.Functions import Logic as ConjugationgridLogic

from src.apps.SentenceChunks.Layout import Layout as SentencechunksLayout
from src.apps.VocabRanomizer.Layout import Layout as VocabranomizerLayout
from src.apps.ConjugationRandomizer.Layout import Layout as ConjugationrandomizerLayout 
from src.apps.ConjugationGrid.Layout import Layout as ConjugationgridLayout


class AppConnector:
    sentencechunks_logic: SentencechunksLogic
    vocabranomizer_logic: VocabranomizerLogic
    conjugationrandomizer_logic: ConjugationrandomizerLogic
    conjugationgrid_logic: ConjugationgridLogic

    sentencechunks_ui: SentencechunksLayout
    vocabranomizer_ui: VocabranomizerLayout
    conjugationrandomizer_ui: ConjugationrandomizerLayout
    conjugationgrid_ui: ConjugationgridLayout

    def __init__(self, apps: dict, logic: dict):
        self.apps = apps
        self.logic = logic

        self.init_connections()
        # self.basic_ui.btn1.clicked.connect(self.second_logic.somefunction)

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


