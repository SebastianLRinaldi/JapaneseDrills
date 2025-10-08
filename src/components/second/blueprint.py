from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

class Blueprint:
    # HEADER
    title_label: QLabel
    status_label: QLabel
    user_label: QLabel
    logout_btn: QPushButton
    search_bar: QLineEdit
    search_btn: QPushButton

    # SIDEBAR
    nav_list: QListWidget

    # DASHBOARD TAB
    graph1: QLabel
    graph2: QLabel
    counter1: QLCDNumber
    counter2: QLCDNumber
    activity_table: QTableWidget

    # JOBS TAB
    job_list: QListWidget
    job_details: QTextEdit
    job_form_label: QLabel
    job_start_btn: QPushButton

    # LOGS TAB
    filter_input: QLineEdit
    log_level_combo: QComboBox
    date_filter: QDateTimeEdit
    logs_table: QTableView
    export_logs_btn: QPushButton

    # SETTINGS TAB
    theme_dark: QRadioButton
    theme_light: QRadioButton
    enable_notifications: QCheckBox
    language_selector: QComboBox
    save_settings_btn: QPushButton
    reset_settings_btn: QPushButton


    def _map_widgets(self, source):
        """
        Copy existing widget instances from source to self.
        """
        # source is some object that already has the widgets as attributes
        for name in self.__annotations__:
            setattr(self, name, getattr(source, name))

    def _init_widgets(self):
        """
        Instantiate all widgets defined in type hints.
        Call this manually when you want actual widget instances.
        """
        for name, typ in self.__annotations__.items():
            setattr(self, name, typ())