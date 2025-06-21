from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys

class CursorOverlay(QWidget):
    def __init__(self, parent, cell_size, color, is_summary=False):
        super().__init__(parent)
        self.cell_size = cell_size
        self.color = color
        self.cursor_visible = True
        self.cursor_pos = (0, 0)
        self.is_summary = is_summary  # 🔥 Add this
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.timer = QTimer()
        self.timer.timeout.connect(self.blink)
        self.timer.start(250)
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
        pen = QPen(QColor(self.color), 2)
        painter.setPen(pen)

        parent = self.parent()
        r, c = self.cursor_pos
        if 0 <= c < parent.cols:
            if self.is_summary:
                cell_widget = parent.summary_widgets[c]  # 🔥 Use summary row
            elif 0 <= r < parent.rows:
                cell_widget = parent.cells_widgets[r][c]
            else:
                return  # invalid row
            rect_global_top_left = cell_widget.mapToGlobal(QPoint(0, 0))
            rect_local_top_left = self.mapFromGlobal(rect_global_top_left)
            cursor_rect = QRect(rect_local_top_left, cell_widget.size())
            painter.drawRect(cursor_rect.adjusted(1, 1, -1, -1))

