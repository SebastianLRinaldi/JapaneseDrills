from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.gui.layout_builder import LayoutBuilder
from .blueprint import Blueprint

class Structure(LayoutBuilder, Blueprint):

    def __init__(self, component):
        super().__init__()
        self._map_widgets(component)
        self.set_widgets()

        self.layout_data = [
            self.splitter("vertical", [
                "eWebPage",
                self.tabs(tab_labels=["Web Explore", "Web Editor", "Search Tools"], children=[
                    self.group("vertical", [
                        "start_page_btn",
                        "design_mode_btn",
                        "devtools_btn"
                    ]),
                    self.group("vertical", [
                        "disable_element_btn",
                        "inject_css_btn",
                        "highlight_elm_btn"
                    ]),
                    self.group("horizontal", [
                        "url_input",
                        "change_url_btn"
                    ])
                ])
            ])
        ]

        self.apply_layout(component, self)


    def set_widgets(self):
        self.eWebPage.setUrl(QUrl("chrome://gpu"))
        self.start_page_btn.setText("Start WebPage")
        self.disable_element_btn.setText("Disable Element")
        self.inject_css_btn.setText("Inject Blue")
        self.highlight_elm_btn.setText("Highlight Element")
        self.design_mode_btn.setText("Activate Design Mode")
        self.devtools_btn.setText("Activate Dev Tools")
        self.url_input.setText("URL GOES HERE")
        self.change_url_btn.setText("Change to Entered URL")
        self.devtools_view.setWindowTitle("DevTools")