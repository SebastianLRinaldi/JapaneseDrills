from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.gui.layout_builder import LayoutBuilder
from .blueprint import Blueprint

class Structure(LayoutBuilder, Blueprint):
    """
    Where you arrange and decorate the widgets
    """

    def __init__(self, component):
        super().__init__()
        
        self._map_widgets(component)
        self.set_widgets()

        self.layout_data = [
            self.box("horizontal", title="Header", children=[
                self.group("horizontal", ["title_label", "status_label"]),
                self.group("horizontal", ["search_bar", "search_btn"]),
                self.group("horizontal", ["user_label", "logout_btn"])
            ]),
            self.splitter("horizontal", children=[
                self.box("vertical", title="Navigation", children=["nav_list"]),
                self.tabs(tab_labels=["Dashboard", "Jobs", "Logs", "Settings"], children=[
                    self.grid([
                        "graph1", "graph2", 
                        "counter1", "counter2", 
                        "activity_table"
                    ], rows=3, columns=2),

                    self.splitter("horizontal", children=[
                        self.box("vertical", title="Job List", children=["job_list"]),
                        self.box("vertical", title="Job Details", children=[
                            "job_form_label", "job_details", "job_start_btn"])
                    ]),

                    self.group("vertical", [
                        self.group("horizontal", ["filter_input", "log_level_combo", "date_filter"]),
                        "logs_table", "export_logs_btn"
                    ]),

                    self.group("vertical", [
                        self.box("horizontal", title="Theme", children=["theme_dark", "theme_light"]),
                        self.box("vertical", title="Preferences", children=[
                            "enable_notifications", "language_selector"
                        ]),
                        self.group("horizontal", ["save_settings_btn", "reset_settings_btn"])
                    ])
                ])
            ])
        ]

        self.apply_layout(component, self)

    # def init_widgets(self):
    #     for name, widget_type in self.__annotations__.items():
    #         widget = widget_type()

    #         match widget:
    #             case QTableWidget():
    #                 widget.setRowCount(5)
    #                 widget.setColumnCount(3)
    #             case QTableView():
    #                 widget.setModel(QStandardItemModel())
    #             case QListWidget():
    #                 widget.addItems([f"Item {i}" for i in range(10)])

    #         setattr(self, name, widget)

    def set_widgets(self):
        self.title_label.setText("Data Dashboard")
        self.status_label.setText("Status: OK")
        self.user_label.setText("User: Admin")
        self.logout_btn.setText("Logout")
        self.search_btn.setText("Search")

        self.graph1.setText("Graph 1")
        self.graph2.setText("Graph 2")

        self.job_form_label.setText("Job Details")
        self.job_start_btn.setText("Start Job")

        self.export_logs_btn.setText("Export Logs")

        self.theme_dark.setText("Dark")
        self.theme_light.setText("Light")
        self.enable_notifications.setText("Enable Notifications")
        self.save_settings_btn.setText("Save")
        self.reset_settings_btn.setText("Reset")


