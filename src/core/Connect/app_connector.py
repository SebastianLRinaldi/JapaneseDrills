from main import Dashboard
from src.apps import * 

class AppConnector:
    app0: App0

    def __init__(self, main: Dashboard, apps: dict[str, object]):
        self.main = main
        self.apps = apps
        self.init_connections()


        # self.app0.layout.another_widget.layout.btn1.clicked.connect(lambda:print("HELLO"))
        # self.app0.layout.btn1.clicked.connect(lambda:print("HI"))

    def init_connections(self):
        for name, wrapper in self.apps.items():
            setattr(self, name.lower(), wrapper)

    # def do_something_between_apps(self):
    #     self.app0.layout.btn2.clicked.connect(self.main.switch_to("Another_app"))

    


# class AppConnector:
#     app0_logic: App0Logic

#     app0_ui: App0Layout

#     def __init__(self, apps: dict, logic: dict):
#         self.apps = apps
#         self.logic = logic

#         self.init_connections()
#         # self.basic_ui.btn1.clicked.connect(self.second_logic.somefunction)

#     """
#     This basically just does this part for us:
    
#     class AppConnector:
#         basic_ui: BasicLayout
#         second_logic: SecondLogic

#         def __init__(self, apps, logic):
#             self.basic_ui = apps["Basic"]
#             self.second_logic = logic["Second"]

#             self.basic_ui.btn1.clicked.connect(self.second_logic.somefunction)
#     """
#     def init_connections(self):
#         for name in self.apps:
#             setattr(self, f"{name.lower()}_ui", self.apps[name])
#             setattr(self, f"{name.lower()}_logic", self.logic[name])








# class AppConnector:
#     basic_logic: BasicLogic
#     second_logic:SecondLogic
#     web_logic: WebLogic

#     basic_ui: BasicLayout
#     second_logic:SecondLayout
#     web_logic: WebLayout
    
#     def __init__(self, ):



#         self.basic_ui.btn1.clicked.connect(self.second_logic.somefunction)

#         self.logic["Basic"].ui.update_widget_btn.clicked.connect(
#             self.logic["Second"].update_widget
#         )

#         # self.logic["Basic"].ui.reset_widget_btn.clicked.connect(
#         #     lambda: self.logic["Second"].ui.name_label.setText("Updated Another Way")
#         # )
        