import sys
import random
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

# -------------------------
# Generate test data for 300 kanji
# -------------------------
KANJI_LIST = [f"漢{i}" for i in range(1, 301)]
KANJI_STATS = {}

for kanji in KANJI_LIST:
    # random scores simulating accuracy/avg_time
    acc = round(random.uniform(0.6, 1.0), 2)   # accuracy 60–100%
    t   = round(random.uniform(0.3, 1.5), 2)   # avg time 0.3–1.5s
    score = acc / (t + 1e-4)                    # score = accuracy / avg_time
    KANJI_STATS[kanji] = (acc, t, score)

# -------------------------
# Kanji cell widget
# -------------------------
class KanjiCell(QLabel):
    NEUTRAL_BG = QColor("#1a1a1a")
    WEAK_BG    = QColor("#c55b3c")
    MODERATE_BG= QColor("#d4b03f")
    STRONG_BG  = QColor("#4db6ac")
    NATIVE_BG  = QColor("#1abc9c")
    TEXT_COLOR = QColor("#f5f5f5")

    def __init__(self, kanji, data=None):
        super().__init__(kanji)
        self.kanji = kanji
        self.data = data
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(48, 48)
        self.apply_style()
        if data:
            acc, t, score = data
            self.setToolTip(f"{kanji}\nAccuracy: {acc:.1%}\nAvg time: {t:.2f}s\nScore: {score:.2f}")

    def apply_style(self):
        score = self.data[2] if self.data else 0
        if score <= 0:
            bg = self.NEUTRAL_BG
        elif score <= 0.5:
            bg = self.WEAK_BG
        elif score <= 1.0:
            bg = self.MODERATE_BG
        elif score <= 2.0:
            bg = self.STRONG_BG
        else:
            bg = self.NATIVE_BG

        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg.name()};
                color: {self.TEXT_COLOR.name()};
                font-size: 16px;
                font-weight: bold;
                border: 1px solid #111;
            }}
        """)

# -------------------------
# Kanji chart widget
# -------------------------
class KanjiChart(QWidget):
    def __init__(self, kanji_stats, kanji_list):
        super().__init__()
        layout = QGridLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(2,2,2,2)

        cols = 20  # number of columns in grid
        for idx, kanji in enumerate(kanji_list):
            row = idx // cols
            col = idx % cols
            data = kanji_stats.get(kanji)
            cell = KanjiCell(kanji, data)
            layout.addWidget(cell, row, col)

        self.setLayout(layout)

# -------------------------
# Scrollable container
# -------------------------
class ScrollableChart(QScrollArea):
    def __init__(self, chart_widget):
        super().__init__()
        self.setWidget(chart_widget)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setStyleSheet("background-color: #262626;")

# -------------------------
# Main window
# -------------------------
class KanjiWindow(QMainWindow):
    def __init__(self, kanji_stats, kanji_list):
        super().__init__()
        self.setWindowTitle("Kanji Drill Chart - 300 Kanji")
        self.resize(1200, 800)

        chart = KanjiChart(kanji_stats, kanji_list)
        scroll = ScrollableChart(chart)
        self.setCentralWidget(scroll)

# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KanjiWindow(KANJI_STATS, KANJI_LIST)
    window.show()
    sys.exit(app.exec())
