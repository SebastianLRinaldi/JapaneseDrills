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

from application.FrontEnd.C_Grouper.SpliterGroupConfiguration import *
from application.FrontEnd.C_Grouper.TabGroupConfigureation import *
from application.FrontEnd.C_Grouper.widgetGroupFrameworks import *

from application.FrontEnd.D_WindowFolder.windowConfigureation import *

from .widgets.cursorOverlay import CursorOverlay
from .widgets.gridCell import GridCell

class SecondLayout(LayoutManager):
    def __init__(self):
        super().__init__()


        self.rows = 6  # editable rows only
        self.cols = 60
        self.cell_size = QSize(24, 32)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(2, 2, 2, 2)
        self.setLayout(self.grid_layout)
        # Create summary widgets row (not part of cells_widgets 2D list)
        self.summary_widgets = []
        for c in range(self.cols):
            cell = GridCell('', preview=False)
            cell.setStyleSheet("border: 1px solid gray; color: red; font-weight: bold;")
            self.grid_layout.addWidget(cell, 0, c)
            self.summary_widgets.append(cell)

        # Create editable cells below summary row, rows start at 1 in layout
        self.cells_data = [['' for _ in range(self.cols)] for _ in range(self.rows)]
        self.cells_widgets = []
        for r in range(self.rows):
            row_widgets = []
            for c in range(self.cols):
                cell = GridCell()
                self.grid_layout.addWidget(cell, r+1, c)  # +1 for summary offset
                row_widgets.append(cell)
            self.cells_widgets.append(row_widgets)

        self.cur_row = 0  # zero-based in editable data rows
        self.cur_col = 0

        self.cursor = CursorOverlay(self, self.cell_size, color="blue")
        self.preview_cells = []



        self.summary_cursor = CursorOverlay(self, self.cell_size, "green", is_summary=True)


        # Position summary cursor at summary row (row=0), same col as editable cursor
        self.update_summary_cursor()

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_InputMethodEnabled, True)

    def update_summary_cursor(self):
        # summary row is always row 0, col synced to editable cursor's col
        self.summary_cursor.setCursorPos(0, self.cur_col)


    def update_summary_row(self):
        # For each column, find first non-empty, non-'X' char from editable rows
        for c in range(self.cols):
            ch = ''
            for r in range(self.rows):
                val = self.cells_data[r][c]
                if val and val != 'X':
                    ch = val  # overwrite ch, keep last non-X
            self.summary_widgets[c].setText(ch)

    def update_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.cells_widgets[r][c].setText(self.cells_data[r][c])
                self.cells_widgets[r][c].setStyleSheet("border: 1px solid gray; color: black; padding: 0px; margin: 0px;")
        self.update_summary_row()

    def clear_preview(self):
        for pc in self.preview_cells:
            self.grid_layout.removeWidget(pc)
            pc.deleteLater()
        self.preview_cells.clear()

    def show_preview(self, text):
        self.clear_preview()
        r, c = self.cur_row, self.cur_col
        for i, ch in enumerate(text):
            if c + i >= self.cols:
                r += 1
                c = 0
            cell = GridCell(ch, preview=True)
            self.grid_layout.addWidget(cell, r+1, c + i)
            self.preview_cells.append(cell)

    def move_cursor(self, dr, dc):
        nr = min(max(0, self.cur_row + dr), self.rows - 1)
        nc = self.cur_col + dc
        if nc < 0:
            nr = max(0, nr - 1)
            nc = self.cols - 1
        elif nc >= self.cols:
            nr = min(self.rows - 1, nr + 1)
            nc = 0
        self.cur_row, self.cur_col = nr, nc
        self.cursor.setCursorPos(nr, nc)
        self.update_summary_cursor()

    def insert_char(self, ch):
        self.cells_data[self.cur_row][self.cur_col] = ch
        self.update_grid()
        self.move_cursor(0, 1)

    def delete_before_cursor(self):
        if self.cur_col == 0 and self.cur_row == 0:
            return
        if self.cur_col == 0:
            self.cur_row -= 1
            self.cur_col = self.cols - 1
        else:
            self.cur_col -= 1
        self.cells_data[self.cur_row][self.cur_col] = ''
        self.update_grid()
        self.cursor.setCursorPos(self.cur_row, self.cur_col)
        self.update_summary_cursor()

    def inputMethodEvent(self, event):
        commit_text = event.commitString()
        preedit_text = event.preeditString()

        if commit_text:
            for ch in commit_text:
                self.insert_char(ch)
            self.clear_preview()

        if preedit_text:
            self.show_preview(preedit_text)
        else:
            self.clear_preview()

        event.accept()

    def inputMethodQuery(self, query):
        if query == Qt.InputMethodQuery.ImEnabled:
            return True
        if query == Qt.InputMethodQuery.ImCursorRectangle:
            x = self.cur_col * self.cell_size.width()
            y = self.cur_row * self.cell_size.height()
            return QRect(x, y, self.cell_size.width(), self.cell_size.height())
        return super().inputMethodQuery(query)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Left:
            self.move_cursor(0, -1)
            self.clear_preview()
        elif key == Qt.Key.Key_Right:
            self.move_cursor(0, 1)
            self.clear_preview()
        elif key == Qt.Key.Key_Up:
            self.move_cursor(-1, 0)
            self.clear_preview()
        elif key == Qt.Key.Key_Down:
            self.move_cursor(1, 0)
            self.clear_preview()
        elif key == Qt.Key.Key_Backspace:
            self.delete_before_cursor()
            self.clear_preview()
        elif key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
            self.clear_preview()
        else:
            text = event.text()
            if text:
                self.insert_char(text)
                self.clear_preview()

    def mousePressEvent(self, event):
        pos = event.globalPosition().toPoint() if hasattr(event, 'globalPosition') else event.globalPos()

        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.cells_widgets[r][c]
                rect = QRect(cell.mapToGlobal(QPoint(0, 0)), cell.size())
                if rect.contains(pos):
                    self.cur_row = r
                    self.cur_col = c
                    self.cursor.setCursorPos(r, c)
                    self.update_summary_cursor()
                    self.setFocus()
                    return

        super().mousePressEvent(event)

