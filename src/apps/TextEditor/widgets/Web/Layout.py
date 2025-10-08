import os
import sys
import time
import re

import threading
from threading import Thread
from enum import Enum
from queue import Queue
from typing import List
from datetime import timedelta

from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtWebEngineCore import *


from src.core.GUI.UiManager import *

class Layout(UiManager):
    eWebPage: QWebEngineView
    start_page_btn: QPushButton
    xpath_btn: QPushButton
    xpath_btn1: QPushButton
    disable_element_btn: QPushButton
    inject_css_btn: QPushButton
    highlight_elm_btn: QPushButton
    design_mode_btn: QPushButton
    devtools_btn: QPushButton
    url_input: QLineEdit
    change_url_btn: QPushButton
    devtools_view: QWebEngineView

    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.set_widgets()

        layout_data = [
            self.splitter("vertical", [
                "eWebPage",
                # self.tabs(tab_labels=["Web Explore", "Web Editor", "Search Tools"], children=[
                #     self.group("vertical", [
                #         "start_page_btn",
                #         "design_mode_btn",
                #         "devtools_btn"
                #     ]),
                #     self.group("vertical", [
                #         "disable_element_btn",
                #         "inject_css_btn",
                #         "highlight_elm_btn",
                #         "xpath_btn",
                #         "xpath_btn1"
                #     ]),
                #     self.group("horizontal", [
                #         "url_input",
                #         "change_url_btn"
                #     ])
                # ])
            ])
        ]

        self.apply_layout(layout_data)

    def init_widgets(self):
        for name, widget_type in self.__annotations__.items():
            widget = widget_type()
            setattr(self, name, widget)

    def set_widgets(self):
        # Create a persistent profile with a real user agent
        profile = QWebEngineProfile("Default", self)
        # profile.setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
        profile.setHttpUserAgent("Mozilla/5.0 (Linux; Android 11; Pixel 4 XL Build/RQ3A.210805.001.A1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36")

        profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)

        # Use this profile for the main page
        page = QWebEnginePage(profile, self.eWebPage)
        self.eWebPage.setPage(page)


        
        self.eWebPage.setUrl(QUrl("https://chatgpt.com/share/68646d39-4fd4-8003-b2dc-ece6e01620d1"))
        # self.start_page_btn.setText("Start WebPage")
        # self.disable_element_btn.setText("Disable Element")
        # self.inject_css_btn.setText("Inject Blue")
        # self.highlight_elm_btn.setText("Highlight Element")
        # self.design_mode_btn.setText("Activate Design Mode")
        # self.devtools_btn.setText("Activate Dev Tools")
        # self.url_input.setText("URL GOES HERE")
        # self.change_url_btn.setText("Change to Entered URL")
        # self.devtools_view.setWindowTitle("DevTools")

        # self.xpath_btn.setText("Type Response")
        # self.xpath_btn1.setText("Send Repsonse")