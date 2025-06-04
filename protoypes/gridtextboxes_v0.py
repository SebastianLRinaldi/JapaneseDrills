from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys

class GridCell(QLabel):
    def __init__(self, char, preview=False):
        super().__init__(char)
        self.setFont(QFont("Arial", 16))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        color = "blue" if preview else "black"
        self.setStyleSheet(f"border: 1px solid gray; color: {color}; padding: 0px; margin: 0px;")
        self.adjustSize()

class IMEGridInput(QWidget):
    def __init__(self):
        super().__init__()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_InputMethodEnabled, True)
        QTimer.singleShot(0, self.setFocus)  # Ensure IME focus

        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(2, 2, 2, 2)
        self.setLayout(self.grid)

        self.row = 0
        self.col = 0
        self.max_cols = 20

        self.preview_cells = []

    def inputMethodEvent(self, event):
        for c in self.preview_cells:
            self.grid.removeWidget(c)
            c.deleteLater()
        self.preview_cells.clear()

        text = event.commitString()
        preview = event.preeditString()

        if preview:
            for i, char in enumerate(preview):
                cell = GridCell(char, preview=True)
                self.grid.addWidget(cell, self.row, self.col + i)
                self.preview_cells.append(cell)

        if text:
            for char in text:
                cell = GridCell(char)
                self.grid.addWidget(cell, self.row, self.col)
                self.col += 1
                if self.col >= self.max_cols:
                    self.col = 0
                    self.row += 1

    def inputMethodQuery(self, query):
        if query == Qt.InputMethodQuery.ImEnabled:
            return True
        if query == Qt.InputMethodQuery.ImCursorRectangle:
            return QRect(self.col * 20, self.row * 20, 1, 20)
        return super().inputMethodQuery(query)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            for c in self.preview_cells:
                self.grid.removeWidget(c)
                c.deleteLater()
            self.preview_cells.clear()
        elif event.key() == Qt.Key.Key_Backspace:
            if self.col > 0:
                self.col -= 1
            elif self.row > 0:
                self.row -= 1
                self.col = self.max_cols - 1
            item = self.grid.itemAtPosition(self.row, self.col)
            if item:
                widget = item.widget()
                self.grid.removeWidget(widget)
                widget.deleteLater()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = IMEGridInput()
    win.setWindowTitle("Live IME Grid Input")
    win.resize(800, 600)
    win.show()
    sys.exit(app.exec())
