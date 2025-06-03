from application.apps.BasicApp.basicFunctions import*

class BasicConnections:
    def __init__(self, ui: BasicLayout, logic: BasicLogic):
        self.ui = ui
        self.logic = logic


        self.ui.add_btn.clicked.connect(self.logic.add_row)
        self.ui.remove_btn.clicked.connect(self.logic.remove_row)
        self.ui.chunk_holder.customContextMenuRequested.connect(self.logic.show_context_menu)
        self.ui.chunk_holder.delete_handler.deletePressed.connect(self.logic.remove_row)
