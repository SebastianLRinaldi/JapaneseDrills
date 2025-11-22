from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.gui.layout_builder import LayoutBuilder
from .blueprint import Blueprint

class Structure(LayoutBuilder, Blueprint):
    """
    Where you arrange and decorate the widgets
    """

    def __init__(self, component:QWidget):
        super().__init__()
        self._map_widgets(component)
        self.component = component
        self.set_widgets()
        
        self.layout_data = [
            self.stats_table,

            self.close_button


            ]

        self.apply_layout(component, self)


    def set_widgets(self):
        self.close_button.setText("Close")
        self.stats_table.verticalHeader().setVisible(False)
        self.stats_table.setRowCount(7)
        self.stats_table.setColumnCount(4)
        self.stats_table.setHorizontalHeaderLabels(["Name", "Best", "+/-", "This Session"])
        # self.stats_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # self.stats_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # self.stats_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.stats_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff) 
        self.stats_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.component.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        w=414
        h=270

        self.component.setFixedSize(w, h)
        self.stats_table.setEnabled(False)

        self.stats_table.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #333; color: white; font-weight: bold; }")

        # self.stats_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        # self.stats_table.resizeColumnsToContents()
        # self.stats_table.resizeRowsToContents()
        # self.stats_table.updateGeometry()
        # self.component.adjustSize()









