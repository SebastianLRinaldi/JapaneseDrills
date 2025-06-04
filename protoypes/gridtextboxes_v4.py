"""

- so like each part of the sentence that you give the first window will make new menu that basically lets you click each part of the sentence with the 
    correct colored bg color to tell the differnce and it will allow you to go to that word types trainer


Some menu that has all teh verb forms in there from the previous step
- shows if you marked it as completed or yet to be done 
- when you double click the 

I would like to be able to shift rows side to side and keep just wrap to other edge of row if it text spills off
I would like to be able to select rows, copy and paste, shift selected rows, idk if I want the ability to shift rows up
I would like to be able to copy finished conjugation
I would like to be able to had notes at end of rows to say what I did or added
I would like to save conjugations and have some to preload as examples
"""





from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys

class GridCell(QLabel):
    def __init__(self, char='', preview=False):
        super().__init__(char)
        self.setFont(QFont("Arial", 20))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.setFixedSize(24, 32)
        self.state = None  # None, 'remove', 'mod'
        
        self.setMouseTracking(True)
        # self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        if preview:
            self.setStyleSheet("border: 1px solid gray; color: blue; font-style: italic; padding: 0px; margin: 0px;")
        else:
            self.setStyleSheet("border: 1px solid gray; color: black; padding: 0px; margin: 0px;")


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            print(f"Right-click on cell with text '{self.text()}'")  # debug
            self.toggle_state()
            event.accept()
        else:
            super().mousePressEvent(event)

    def toggle_state(self):
        if self.state is None:
            self.state = 'remove'
            bg_color = '#ffcccc'  # light red background
            text_color = 'black'
        elif self.state == 'remove':
            self.state = 'mod'
            bg_color = '#ccffff'  # light cyan background
            text_color = 'black'
        else:
            self.state = None
            bg_color = ''
            text_color = 'black'
            
        self.setStyleSheet(f"""
            border: 1px solid gray;
            background-color: {bg_color};
            color: {text_color};
        """)

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


class IMEGridEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.rows = 10  # editable rows only
        self.cols = 20
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = IMEGridEditor()
    win.setWindowTitle("IME Grid Editor with Composition Preview")
    win.resize(600, 400)
    win.show()
    win.setFocus()
    
    sys.exit(app.exec())
