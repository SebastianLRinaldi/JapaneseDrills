from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys

class GridCell(QLabel):
    def __init__(self, char='', preview=False):
        super().__init__(char)
        self.setFont(QFont("Arial", 16))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(24, 32)
        if preview:
            self.setStyleSheet("border: 1px solid gray; color: blue; font-style: italic; padding: 0px; margin: 0px;")
        else:
            self.setStyleSheet("border: 1px solid gray; color: black; padding: 0px; margin: 0px;")

class CursorOverlay(QWidget):
    def __init__(self, parent, cell_size):
        super().__init__(parent)
        self.cell_size = cell_size
        self.cursor_visible = True
        self.cursor_pos = (0, 0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.blink)
        self.timer.start(500)
        self.resize(parent.size())
        self.show()

    def blink(self):
        self.cursor_visible = not self.cursor_visible
        self.update()

    def setCursorPos(self, row, col):
        self.cursor_pos = (row, col)
        self.update()

    def paintEvent(self, event):
        if not self.cursor_visible:
            return
        painter = QPainter(self)
        pen = QPen(QColor(0, 120, 215), 2)  # blue cursor color
        painter.setPen(pen)
        x = self.cursor_pos[1] * self.cell_size.width()
        y = self.cursor_pos[0] * self.cell_size.height()
        rect = QRect(x + 2, y + 2, self.cell_size.width() - 4, self.cell_size.height() - 4)
        painter.drawRect(rect)

class IMEGridEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_InputMethodEnabled, True)

        self.rows = 10
        self.cols = 20
        self.cell_size = QSize(24, 32)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(2, 2, 2, 2)
        self.setLayout(self.grid_layout)

        self.cells_data = [['' for _ in range(self.cols)] for _ in range(self.rows)]
        self.cells_widgets = [[GridCell() for _ in range(self.cols)] for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid_layout.addWidget(self.cells_widgets[r][c], r, c)

        self.cur_row = 0
        self.cur_col = 0

        self.cursor = CursorOverlay(self, self.cell_size)

        # Keep track of preview cells (for preedit string)
        self.preview_cells = []

        QTimer.singleShot(0, self.setFocus)

    def update_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.cells_widgets[r][c].setText(self.cells_data[r][c])
                self.cells_widgets[r][c].setStyleSheet("border: 1px solid gray; color: black; padding: 0px; margin: 0px;")

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
            self.grid_layout.addWidget(cell, r, c + i)
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = IMEGridEditor()
    win.setWindowTitle("IME Grid Editor with Composition Preview")
    win.resize(600, 400)
    win.show()
    sys.exit(app.exec())
