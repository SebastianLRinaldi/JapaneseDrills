import json
import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *


"""
Level	Accuracy	Avg Time (s per kana)	Approx. Score
Native-level	~1.0	0.3–0.5 s	2–3
Strong learner	0.95–1.0	0.5–1.0 s	1–2
Intermediate	0.9	1.0–1.5 s	0.6–0.9
Beginner/weak	<0.8	>1.5 s	<0.5

NEUTRAL_BG = QColor("#1a1a1a")  # untested/score 0
WEAK_BG    = QColor("#c55b3c")  # low score (red-orange)
MODERATE_BG= QColor("#d4b03f")  # medium score (amber)
STRONG_BG  = QColor("#4db6ac")  # strong learner (teal)
NATIVE_BG  = QColor("#1abc9c")  # near-native (green)
TEXT_LIGHT = QColor("#f5f5f5")  # for contrast


"""





"""
RN we have it as a global best and worst 15
Needs a best and worst for each category more of a drop down per HIRIKAN vs KATAKANA TAB
Need to have some way to have in the corner of a box show the ranking of like 1-15 and if its 1 in best its the strongest 
- if its 1 in worst its the weakest

"""




MASTER_PATH = r"F:\_Small\344 School Python\JapaneseDrills\kana_recall_data\kana_mastery_progress.json"
TOP_N_GLOBAL = 15

"""
        if self.mode=="best":
            bg="#1abc9c"; fg="#fff"; border="2px solid #0e6655"
        elif self.mode=="worst":
            bg="#c0392b"; fg="#fff"; border="2px solid #641e16"
        else:
            bg="#1a1a1a"; fg="#666"; border="1px solid #111"
"""

# -------------------------
# Load and compute scores

# -------------------------
def load_master(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def compute_score(stats):
    correct = stats.get("correct",0)
    wrong = stats.get("wrong",0)
    total = correct+wrong
    accuracy = correct/total if total else 0
    avg_time = stats.get("avg_time") or float("inf")
    score = accuracy / (avg_time + 1e-4)
    return accuracy, avg_time, score

# -------------------------
# KANA CHART DATA
# Each row: main consonant, then combos
# Dakuten row follows under main
# -------------------------
# Vowels order
VOWELS = ["a","i","u","e","o"]

HIRAGANA_ROWS = [
    # Main
    ["あ","い","う","え","お"],
    ["か","き","く","け","こ","きゃ","きゅ","きょ"],
    ["さ","し","す","せ","そ","しゃ","しゅ","しょ"],
    ["た","ち","つ","て","と","ちゃ","ちゅ","ちょ"],
    ["な","に","ぬ","ね","の","にゃ","にゅ","にょ"],
    ["は","ひ","ふ","へ","ほ","ひゃ","ひゅ","ひょ","ふぁ","ふぃ"], # optional f combos
    ["ま","み","む","め","も","みゃ","みゅ","みょ"],
    ["や","","ゆ","","よ"],
    ["ら","り","る","れ","ろ","りゃ","りゅ","りょ"],
    ["わ","","","","を"],
    ["ん",""],

    # Dakuten
    ["が","ぎ","ぐ","げ","ご","ぎゃ","ぎゅ","ぎょ"],
    ["ざ","じ","ず","ぜ","ぞ","じゃ","じゅ","じょ"],
    ["だ","ぢ","づ","で","ど","ぢゃ","ぢゅ","ぢょ"],
    ["ば","び","ぶ","べ","ぼ","びゃ","びゅ","びょ"],
    ["ぱ","ぴ","ぷ","ぺ","ぽ","ぴゃ","ぴゅ","ぴょ"]
]

KATAKANA_ROWS = [
    ["ア","イ","ウ","エ","オ"],
    ["カ","キ","ク","ケ","コ","キャ","キュ","キョ"],
    ["サ","シ","ス","セ","ソ","シャ","シュ","ショ"],
    ["タ","チ","ツ","テ","ト","チャ","チュ","チョ"],
    ["ナ","ニ","ヌ","ネ","ノ","ニャ","ニュ","ニョ"],
    ["ハ","ヒ","フ","ヘ","ホ","ヒャ","ヒュ","ヒョ"],
    ["マ","ミ","ム","メ","モ","ミャ","ミュ","ミョ"],
    ["ヤ","","ユ","","ヨ"],
    ["ラ","リ","ル","レ","ロ","リャ","リュ","リョ"],
    ["ワ","","","","ヲ"],
    ["ン",""],

    # Dakuten
    ["ガ","ギ","グ","ゲ","ゴ","ギャ","ギュ","ギョ"],
    ["ザ","ジ","ズ","ゼ","ゾ","ジャ","ジュ","ジョ"],
    ["ダ","ヂ","ヅ","デ","ド","ヂャ","ヂュ","ヂョ"],
    ["バ","ビ","ブ","ベ","ボ","ビャ","ビュ","ビョ"],
    ["パ","ピ","プ","ペ","ポ","ピャ","ピュ","ピョ"]
]

FULL_CHARTS = [("Hiragana", HIRAGANA_ROWS), ("Katakana", KATAKANA_ROWS)]








class KanaCell(QLabel):
    NEUTRAL_COLOR = QColor("#666666")  # text for score 0
    LOW_COLOR = QColor("#c0392b")      # text for low positive score
    HIGH_COLOR = QColor("#1abc9c")     # text for high score
    TEXT_LIGHT = QColor("#f5f5f5")          # soft white
    TEXT_DARK  = QColor("#1a1a1a")           # dark for contrast on light bg

    def __init__(self, kana, data=None, mode="neutral"):
        super().__init__(kana if kana else "")
        self.kana = kana
        self.data = data
        self.mode = mode  # "neutral", "best", "worst"
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(48, 48)
        self.apply_style()
        if data:
            acc, t, score = data
            self.setToolTip(f"{kana}\nAccuracy: {acc:.1%}\nAvg time: {t:.2f}s\nScore: {score:.4f}")

    def apply_style(self):
        if not self.kana:
            self.setStyleSheet("background: transparent; border: none;")
            return

        # Background and border from mode
        if self.mode == "best":
            bg = "#1abc9c"
            border = "2px solid #0e6655"
            fg = self.TEXT_DARK
        elif self.mode == "worst":
            bg = "#c0392b"
            border = "2px solid #641e16"
            fg = self.TEXT_DARK
        else:
            bg = "#1a1a1a"
            border = "1px solid #111"

            # Text color based on score gradient
            if self.data:
                _, _, score = self.data
                if score <= 0:
                    fg = self.NEUTRAL_COLOR
                else:
                    t = min(score, 1.0)  # normalize for gradient
                    fg = self.interpolate_color(self.LOW_COLOR, self.HIGH_COLOR, t)
            else:
                fg = self.NEUTRAL_COLOR

        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg};
                color: {fg.name()};
                font-size: 14px;
                font-weight: bold;
                border: {border};
            }}
        """)

    @staticmethod
    def interpolate_color(c1: QColor, c2: QColor, t: float) -> QColor:
        r = int(c1.red() + (c2.red() - c1.red()) * t)
        g = int(c1.green() + (c2.green() - c1.green()) * t)
        b = int(c1.blue() + (c2.blue() - c1.blue()) * t)
        return QColor(r, g, b)

# -------------------------
# KANA CHART WIDGET
# -------------------------
class KanaChart(QWidget):
    def __init__(self, kana_stats, highlight_set, chart_rows, mode):
        super().__init__()

        # Use a fixed-size inner widget for the grid
        grid_container = QWidget()
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)  # compact spacing
        grid_layout.setContentsMargins(0, 0, 0, 0)

        max_cols = max(len(row) for row in chart_rows)
        for r, row in enumerate(chart_rows):
            for c, kana in enumerate(row):
                if not kana:
                    continue
                data = kana_stats.get(kana)
                cell_mode = mode if kana in highlight_set else "neutral"
                cell = KanaCell(kana, data, cell_mode)
                grid_layout.addWidget(cell, r, c)

        grid_container.setLayout(grid_layout)

        # Fix the size of the container to prevent expansion
        total_width = max_cols * 48 + (max_cols - 1) * 2  # cell size + spacing
        total_height = len(chart_rows) * 48 + (len(chart_rows) - 1) * 2
        grid_container.setFixedSize(total_width, total_height)

        # Add the container to this widget (so you can place it in tabs)
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(grid_container)
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

# -------------------------
# MAIN WINDOW
# -------------------------
class KanaChartWindow(QMainWindow):
    def __init__(self,kana_stats,best_set,worst_set):
        super().__init__()
        self.setWindowTitle("Kana Performance Chart")
        self.resize(800,700)


        # Slightly lighter background than cell neutral
        self.setStyleSheet("background-color: #262626;")  # slightly lighter dark gray

        tabs = QTabWidget()
        for name, chart_rows in FULL_CHARTS:
            tabs.addTab(KanaChart(kana_stats,best_set,chart_rows,"best"), f"{name} Best 15")
            tabs.addTab(KanaChart(kana_stats,worst_set,chart_rows,"worst"), f"{name} Worst 15")
        self.setCentralWidget(tabs)
        tabs.setStyleSheet("""
            /* Tab widget pane (where charts appear) */
            QTabWidget::pane {
                background: #262626; /* match window bg */
                border: none;
            }

            /* Tab bar */
            QTabBar::tab {
                background: #333333;  /* unselected tabs */
                color: #f5f5f5;       /* text */
                padding: 6px 12px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }

            QTabBar::tab:selected {
                background: #444444;  /* selected tab */
                font-weight: bold;
            }

            QTabBar::tab:hover {
                background: #555555;  /* hover effect */
            }
        """)


"""
If we want percentile of best and worst (later for performace tuning)
scores = [s for _, s in scored]
scores.sort()
# example:
good_cutoff = scores[int(len(scores)*0.8)]  # top 20% are “good”
bad_cutoff  = scores[int(len(scores)*0.2)]  # bottom 20% are “bad”
---
Correct — using fixed percentiles like that does always mark roughly 20% as “bad”. That’s the tradeoff with percentile-based thresholds: they are relative, not absolute.

If you want absolute meaning — i.e., only truly low-performing kana are marked bad regardless of overall improvement — you need a dynamic absolute threshold, like:

BAD_THRESHOLD = 0.5  # or whatever makes sense in your score formula
GOOD_THRESHOLD = 1.5


"""




# -------------------------
# RUN
# -------------------------
if __name__=="__main__":
    master = load_master(MASTER_PATH)
    kana_stats={}
    scored=[]
    for kana, stats in master["kana"].items():
        acc,t,score = compute_score(stats)
        kana_stats[kana]=(acc,t,score)
        scored.append((kana,score))
    print(f"SCORED: {scored}")
    scored.sort(key=lambda x:x[1],reverse=True)
    best_set={k for k,_ in scored[:TOP_N_GLOBAL]}
    worst_set={k for k,_ in scored[-TOP_N_GLOBAL:]}
    app=QApplication(sys.argv)
    window=KanaChartWindow(kana_stats,best_set,worst_set)
    window.show()
    sys.exit(app.exec())


