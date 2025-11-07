# from PyQt6.QtWidgets import (
#     QApplication, QWidget, QTextEdit, QPushButton, QLabel, QGridLayout, 
#     QVBoxLayout, QHBoxLayout, QScrollArea
# )
# from PyQt6.QtCore import Qt
# import sys

# app = QApplication(sys.argv)
# window = QWidget()
# window.setWindowTitle("Scrollable Grid Word List")

# main_layout = QHBoxLayout()

# # -------------------------------
# # Left side: Typing + submit
# # -------------------------------
# left_layout = QVBoxLayout()
# text_edit = QTextEdit()
# text_edit.setPlainText("犬\n猫\n学校\n")  # user typed some words
# submit_btn = QPushButton("Submit")
# left_layout.addWidget(text_edit)
# left_layout.addWidget(submit_btn)

# # -------------------------------
# # Right side: Scrollable word grid
# # -------------------------------
# scroll_area = QScrollArea()
# scroll_area.setWidgetResizable(True)

# grid_container = QWidget()
# grid_layout = QGridLayout()
# grid_layout.setSpacing(5)  # tight spacing for grid
# grid_container.setLayout(grid_layout)

# # Example words (simulate 100+)
# words = [f"単語{i+1}" for i in range(100)]  # 120 words as example
# cols = 5  # number of columns in grid

# for index, word in enumerate(words):
#     row = index // cols
#     col = index % cols
#     label = QLabel(word)
#     label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#     label.setStyleSheet("border: 1px solid gray; padding: 5px;")
#     grid_layout.addWidget(label, row, col)

# scroll_area.setWidget(grid_container)

# # -------------------------------
# # Assemble layout
# # -------------------------------
# main_layout.addLayout(left_layout)
# main_layout.addWidget(scroll_area)

# window.setLayout(main_layout)
# window.resize(800, 600)
# window.show()
# sys.exit(app.exec())














# from PyQt6.QtWidgets import (
#     QApplication, QWidget, QTextEdit, QPushButton, QLabel, QGridLayout,
#     QVBoxLayout, QHBoxLayout, QScrollArea
# )
# from PyQt6.QtCore import Qt
# import sys

# class FreeRecallApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("IME-Friendly Free Recall")
#         self.resize(800, 600)

#         # Main layout
#         main_layout = QHBoxLayout()
#         self.setLayout(main_layout)

#         # Left: typing area
#         left_layout = QVBoxLayout()
#         self.text_edit = QTextEdit()
#         self.submit_btn = QPushButton("Submit")
#         self.submit_btn.clicked.connect(self.submit_word)
#         left_layout.addWidget(self.text_edit)
#         left_layout.addWidget(self.submit_btn)

#         # Right: scrollable grid
#         self.scroll_area = QScrollArea()
#         self.scroll_area.setWidgetResizable(True)
#         self.grid_container = QWidget()
#         self.grid_layout = QGridLayout()
#         self.grid_layout.setSpacing(5)
#         self.grid_container.setLayout(self.grid_layout)
#         self.scroll_area.setWidget(self.grid_container)

#         main_layout.addLayout(left_layout)
#         main_layout.addWidget(self.scroll_area)

#         # Grid settings
#         self.cols = 5
#         self.word_count = 0

#         # Optional: pre-fill some words
#         self.words = ["犬", "猫", "学校", "車"]
#         for word in self.words:
#             self.add_word_to_grid(word)

#     def submit_word(self):
#         # Commit all text in QTextEdit (can be multiple lines)
#         text = self.text_edit.toPlainText().strip()
#         if text:
#             for line in text.split("\n"):
#                 line = line.strip()
#                 if line:
#                     self.add_word_to_grid(line)
#             self.text_edit.clear()

#     def add_word_to_grid(self, word):
#         row = self.word_count // self.cols
#         col = self.word_count % self.cols
#         label = QLabel(word)
#         label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         label.setStyleSheet("border: 1px solid gray; padding: 5px;")
#         self.grid_layout.addWidget(label, row, col)
#         self.word_count += 1

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = FreeRecallApp()
#     window.show()
#     sys.exit(app.exec())

# from pathlib import Path
# path = r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data_test\session_test\session(3)_2025-11-05.json"
# temp = Path(path).stem.replace("_", " ")
# print(temp)
# exit()


# from PyQt6.QtWidgets import QApplication, QLineEdit, QWidget, QVBoxLayout
# from PyQt6.QtGui import QColor

# class ColorLineEdit(QLineEdit):
#     def __init__(self):
#         super().__init__()
#         self.textChanged.connect(self.update_color)

#     def update_color(self, text: str):
#         if text == "日本語":
#             # Special value: blue
#             self.setStyleSheet("color: blue;")
#         else:
#             try:
#                 # Example validation: allow only integers
#                 int(text)
#                 self.setStyleSheet("color: black;")  # valid input
#             except ValueError:
#                 self.setStyleSheet("color: red;")  # invalid input

# app = QApplication([])

# window = QWidget()
# layout = QVBoxLayout()
# line_edit = ColorLineEdit()
# layout.addWidget(line_edit)
# window.setLayout(layout)
# window.show()

# app.exec()








# from PyQt6.QtWidgets import *
# from PyQt6.QtCore import Qt
# import sys

# class FreeRecallApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Current Word + History Free Recall")
#         self.resize(800, 600)

#         # -------------------------------
#         # Layouts
#         # -------------------------------
#         main_layout = QHBoxLayout()
#         self.setLayout(main_layout)

#         # Left side: text area for history + current word
#         left_layout = QVBoxLayout()
#         main_layout.addLayout(left_layout)

#         # History display (read-only)
#         self.history_area = QTextEdit()
#         self.history_area.setReadOnly(True)
#         self.history_area.setPlaceholderText("History of submitted words...")
#         left_layout.addWidget(self.history_area)

#         # Current word input
#         self.current_word_edit = QLineEdit()
#         self.current_word_edit.setFixedHeight(30)  # single-line height
#         self.current_word_edit.installEventFilter(self)  # catch Enter
#         self.current_word_edit.setPlaceholderText("Type next word here...")
#         left_layout.addWidget(self.current_word_edit)

#         # Optional submit button
#         self.submit_btn = QPushButton("Submit")
#         self.submit_btn.clicked.connect(self.submit_current_word)
#         left_layout.addWidget(self.submit_btn)

#         # Right side: scrollable grid for words
#         self.scroll_area = QScrollArea()
#         self.scroll_area.setWidgetResizable(True)
#         self.grid_container = QWidget()
#         self.grid_layout = QGridLayout()
#         self.grid_layout.setSpacing(5)
#         self.grid_container.setLayout(self.grid_layout)
#         self.scroll_area.setWidget(self.grid_container)
#         main_layout.addWidget(self.scroll_area)

#         # Grid settings
#         self.cols = 5
#         self.word_count = 0


#         self.current_word_edit.returnPressed.connect(self.submit_current_word)

#     # -------------------------------
#     # Submit current word
#     # -------------------------------
#     def submit_current_word(self):
#         word = self.current_word_edit.text()
#         if word:
#             # Add to history
#             history_text = self.history_area.toPlainText()
#             new_history = (history_text + "\n" + word) if history_text else word
#             self.history_area.setPlainText(new_history)

#             # Add to grid
#             row = self.word_count // self.cols
#             col = self.word_count % self.cols
#             label = QLabel(word)
#             label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#             label.setStyleSheet("border: 1px solid gray; padding: 5px;")
#             self.grid_layout.addWidget(label, row, col)
#             self.word_count += 1

#             # Clear current word
#             self.current_word_edit.clear()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = FreeRecallApp()
#     window.show()
#     sys.exit(app.exec())





# from PyQt6.QtCore import *
# from PyQt6.QtWidgets import * 
# from PyQt6.QtGui import *
# import sys, random

# from PyQt6.QtCore import *
# from PyQt6.QtWidgets import * 
# from PyQt6.QtGui import *
# import sys, random

# WORDS = ["猫", "犬", "鳥", "魚", "木", "山", "川", "空", "雨", "風",
#     "学校",    # school
#     "図書館",  # library
#     "先生",    # teacher
#     "友達",    # friend
#     "日本語",  # Japanese language
#     "電車",    # train
#     "映画館",  # movie theater
#     "自転車",  # bicycle
#     "電話番号",# phone number
#     "時間割",  # timetable/schedule
#     ]

# class FreeRecallList(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Free Recall List")
#         self.resize(600, 400)

#         main_layout = QVBoxLayout(self)
#         main_layout.setContentsMargins(15, 15, 15, 15)
#         main_layout.setSpacing(10)

#         # List widget
#         self.list_widget = QListWidget()
#         self.list_widget.setFlow(QListWidget.Flow.LeftToRight)
#         self.list_widget.setWrapping(True)
#         self.list_widget.setSpacing(0)  # words closer together
#         self.list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
#         self.list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
#         self.list_widget.setStyleSheet("""
#             QListWidget {
#                 background-color: #fdfdfd;
#                 border: 1px solid #ccc;
#                 border-radius: 10px;
#                 padding: 10px;
#             }
#             QListWidget::item {
#                 border: 1px solid #ddd;
#                 border-radius: 8px;
#                 padding: 12px 18px;
#             }
#             QListWidget::item:selected {
#                 background-color: #a0e7e5;
#             }
#         """)
#         main_layout.addWidget(self.list_widget)

#         # Submit button
#         self.submit_btn = QPushButton("Add Next Word")
#         self.submit_btn.clicked.connect(self.add_word)
#         self.submit_btn.setStyleSheet("""
#             QPushButton {
#                 padding: 12px 25px;
#                 font-size: 18px;
#                 border-radius: 12px;
#                 background-color: #4caf50;
#                 color: white;
#                 font-weight: bold;
#             }
#             QPushButton:hover {
#                 background-color: #45a049;
#             }
#         """)
#         main_layout.addWidget(self.submit_btn, alignment=Qt.AlignmentFlag.AlignCenter)

#         self.toggle_color = True

#     def add_word(self):
#         word = random.choice(WORDS)
#         item = QListWidgetItem(word)
#         item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

#         # Set large font
#         font = QFont()
#         font.setPointSize(48)
#         font.setBold(True)
#         item.setFont(font)

#         # Alternate background colors
#         item.setBackground(QColor("#ffffff") if self.toggle_color else QColor("#e8f5e9"))
#         self.toggle_color = not self.toggle_color

#         # Add item
#         self.list_widget.addItem(item)

#         # Scroll to bottom automatically
#         self.list_widget.scrollToBottom()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = FreeRecallList()
#     window.show()
#     sys.exit(app.exec())



from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QGraphicsDropShadowEffect
from PyQt6.QtCore import QPropertyAnimation, QPoint, QEasingCurve
from PyQt6.QtGui import QColor
import sys


from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QRect
import sys

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton
from PyQt6.QtCore import QTimer
import sys

# class Window(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("QLineEdit Text Shake - Works!")
#         layout = QVBoxLayout(self)

#         self.line_edit = QLineEdit()
#         self.line_edit.setPlaceholderText("Type something...")
#         layout.addWidget(self.line_edit)

#         btn = QPushButton("Shake Text")
#         btn.clicked.connect(self.shake_text)
#         layout.addWidget(btn)

#         self._shake_timer = QTimer(self)
#         self._shake_index = 0
#         self._shake_pattern = [0, 4, -4, 4, -4, 2, -2, 0]  # sequence of horizontal offsets

#     def shake_text(self):
#         if self._shake_timer.isActive():
#             return  # prevent overlapping shakes

#         self._shake_index = 0
#         self._shake_timer.timeout.connect(self._on_shake_step)
#         self._shake_timer.start(25)  # controls speed

#     def _on_shake_step(self):
#         if self._shake_index >= len(self._shake_pattern):
#             self._shake_timer.stop()
#             self.line_edit.setTextMargins(0, 0, 0, 0)
#             self._shake_timer.timeout.disconnect(self._on_shake_step)
#             return

#         offset = self._shake_pattern[self._shake_index]
#         self.line_edit.setTextMargins(offset, 0, 0, 0)
#         self._shake_index += 1


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     w = Window()
#     w.show()
#     sys.exit(app.exec())


# from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton
# from PyQt6.QtCore import QPropertyAnimation, QPoint


# class ShakeExample(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Shake Example")

#         self.layout = QVBoxLayout(self)

#         self.line_edit = QLineEdit()
#         self.line_edit.setPlaceholderText("Type something...")
#         self.layout.addWidget(self.line_edit)

#         self.button = QPushButton("Shake it!")
#         self.button.clicked.connect(self.shake_line_edit)
#         self.layout.addWidget(self.button)

#         self._shake_animation = None

#     def shake_line_edit(self):
#         # Create a horizontal shake animation on the line edit
#         animation = QPropertyAnimation(self.line_edit, b"pos")
#         animation.setDuration(150)
#         original_pos = self.line_edit.pos()

#         # Define the shake pattern
#         animation.setKeyValueAt(0, original_pos)
#         animation.setKeyValueAt(0.1, original_pos + QPoint(4, 0))
#         animation.setKeyValueAt(0.2, original_pos + QPoint(-4, 0))
#         animation.setKeyValueAt(0.3, original_pos + QPoint(4, 0))
#         animation.setKeyValueAt(0.4, original_pos + QPoint(-4, 0))
#         animation.setKeyValueAt(0.5, original_pos + QPoint(2, 0))
#         animation.setKeyValueAt(0.6, original_pos + QPoint(-2, 0))
#         animation.setKeyValueAt(1, original_pos)

#         animation.start()
#         self._shake_animation = animation  # prevent garbage collection


# if __name__ == "__main__":
#     app = QApplication([])
#     window = ShakeExample()
#     window.resize(300, 120)
#     window.show()
#     app.exec()

# from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton
# from PyQt6.QtCore import QPropertyAnimation, pyqtProperty


# class ShakingLineEdit(QLineEdit):
#     def __init__(self):
#         super().__init__()
#         self._offset = 0
#         self._animation = None

#     def getOffset(self):
#         return self._offset

#     def setOffset(self, value):
#         self._offset = value
#         # Move text by adjusting the left margin
#         self.setTextMargins(value, 0, 0, 0)

#     offset = pyqtProperty(int, fget=getOffset, fset=setOffset)

#     def shake(self):
#         if self._animation and self._animation.state() == QPropertyAnimation.State.Running:
#             return  # prevent overlapping shakes

#         animation = QPropertyAnimation(self, b"offset")
#         animation.setDuration(300)
#         animation.setKeyValueAt(0, 0)
#         animation.setKeyValueAt(0.1, 4)
#         animation.setKeyValueAt(0.2, -4)
#         animation.setKeyValueAt(0.3, 4)
#         animation.setKeyValueAt(0.4, -4)
#         animation.setKeyValueAt(0.5, 2)
#         animation.setKeyValueAt(0.6, -2)
#         animation.setKeyValueAt(1, 0)
#         animation.start()

#         self._animation = animation  # keep reference alive


# class ShakeTextExample(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Shake Text Only")

#         layout = QVBoxLayout(self)
#         self.line_edit = ShakingLineEdit()
#         self.line_edit.setPlaceholderText("Type something...")
#         layout.addWidget(self.line_edit)

#         button = QPushButton("Shake text!")
#         button.clicked.connect(self.line_edit.shake)
#         layout.addWidget(button)


# if __name__ == "__main__":
#     app = QApplication([])
#     window = ShakeTextExample()
#     window.resize(300, 120)
#     window.show()
#     app.exec()



from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton
from PyQt6.QtCore import QTimer


class ShakingLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self._shake_pattern = [0, 4, -4, 4, -4, 2, -2, 0]  # horizontal offsets
        self._shake_index = 0
        self._timer = QTimer()
        self._timer.timeout.connect(self._on_shake_step)

    def shake(self):
        if self._timer.isActive():
            return  # prevent overlapping shakes
        self._shake_index = 0
        self._timer.start(25)  # speed of shake

    def _on_shake_step(self):
        if self._shake_index >= len(self._shake_pattern):
            self._timer.stop()
            self.setTextMargins(0, 0, 0, 0)  # reset margins
            return

        offset = self._shake_pattern[self._shake_index]
        self.setTextMargins(offset, 0, 0, 0)
        self._shake_index += 1


# Example usage
class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shake Text Example")
        layout = QVBoxLayout(self)

        self.line_edit = ShakingLineEdit()
        layout.addWidget(self.line_edit)

        button = QPushButton("Shake Text")
        button.clicked.connect(self.line_edit.shake)
        layout.addWidget(button)


if __name__ == "__main__":
    app = QApplication([])
    window = Example()
    window.resize(300, 120)
    window.show()
    app.exec()

