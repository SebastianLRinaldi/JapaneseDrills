"""
Session word heat map (1/0)
"""
# import json
# import os
# import math
# import pandas as pd
# import numpy as np
# import seaborn as sns

# from matplotlib.gridspec import GridSpec
# import matplotlib.pyplot as plt
# plt.rcParams['font.family'] = 'MS Gothic'

# # === Paths ===
# master_path = r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data\master.json"
# sessions_dir = r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data\sessions"

# # === Load Master Data ===
# with open(master_path, "r", encoding="utf-8") as f:
#     master_data = json.load(f)


# # === Collect all session files ===
# session_files = [f for f in os.listdir(sessions_dir) if f.endswith(".json")]
# # session_files.sort(key=lambda x: int(x.split("(")[-1].split(")")[0]))  # sort by session number if named like session(1).json

# # === Build word–session matrix ===
# session_word_data = {}

# for file in session_files:
#     path = os.path.join(sessions_dir, file)
#     with open(path, "r", encoding="utf-8") as f:
#         data = json.load(f)

#     session_num = data["session_num"]
#     words = data["new_words"] + data["old_words"]

#     # For now, mark presence with 1 (could expand to count if multiple occurrences)
#     for word in words:
#         if word not in session_word_data:
#             session_word_data[word] = {}
#         session_word_data[word][session_num] = session_word_data[word].get(session_num, 0) + 1

# # === Convert to DataFrame ===
# df = pd.DataFrame(session_word_data).fillna(0).astype(int)
# df.index.name = "Session"
# df = df.sort_index()  # sessions in order

# # # === Sort words by total frequency (highest on top) ===
# # total_counts = df.sum(axis=0)
# # sorted_words = total_counts.sort_values(ascending=False).index
# # df = df[sorted_words]  # reorder columns

# # === Split into chunks for plotting ===
# words_per_chunk = 40
# num_chunks = math.ceil(len(df.columns) / words_per_chunk)

# # === Grid layout parameters ===
# cols = 3  # number of heatmaps per row
# rows = math.ceil(num_chunks / cols)

# # === Create figure with bigger size per subplot ===
# subplot_width = 8  # width per subplot
# subplot_height = 8  # height per subplot
# # Set figure DPI
# screen_width = 1920
# screen_height = 1080
# dpi = 100  # typical value; can adjust if needed
# fig_width = screen_width / dpi
# fig_height = screen_height / dpi

# fig = plt.figure(figsize=(fig_width, fig_height), dpi=dpi)
# gs = GridSpec(rows, cols, figure=fig, hspace=0.1, wspace=0.0)  # more space between plots

# for i in range(num_chunks):
#     start = i * words_per_chunk
#     end = start + words_per_chunk
#     chunk = df.iloc[:, start:end]

#     row = i // cols
#     col = i % cols

#     ax = fig.add_subplot(gs[row, col])
#     sns.heatmap(
#         chunk.T,
#         cmap="YlOrRd",
#         linewidths=0.5,
#         cbar=True,
#         ax=ax,
#         annot=False
#     )

#     ax.set_title(f"Words {start+1}-{min(end,len(df.columns))}", fontsize=6, pad=0)
#     ax.set_xlabel("Session", fontsize=8)
#     # ax.set_ylabel("Word", fontsize=12)
#     # ax.tick_params(axis='y', labelsize=8)  # bigger labels
#     ax.tick_params(axis='x', labelsize=6)

# plt.tight_layout()
# plt.show()
















"""
Session word heat map (1/0) all words show up
"""
import sys
import os
import json
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea, QLabel
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea, QLabel
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import json, os
from matplotlib.gridspec import GridSpec

plt.rcParams['font.family'] = 'MS Gothic'

# --- Load your session data ---
folder_path = r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data\sessions"
session_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.json')]
session_files.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0].split('(')[-1].split(')')[0]))

session_word_data = {}
for file in session_files:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    session_num = data["session_num"]
    words = data.get("new_words", []) + data.get("old_words", [])
    for word in words:
        if word not in session_word_data:
            session_word_data[word] = {}
        session_word_data[word][session_num] = session_word_data[word].get(session_num, 0) + 1

df = pd.DataFrame(session_word_data).fillna(0).astype(int)
df = df.sort_index()
df = df[df.sum(axis=0).sort_values(ascending=False).index]  # sort words by frequency

# --- PyQt6 widget ---
class ChunkedHeatmapViewer(QWidget):
    def __init__(self, df, words_per_chunk=40, cols=3):
        super().__init__()
        self.setWindowTitle("Scrollable Chunked Heatmap")
        self.resize(1400, 900)

        # --- Scroll area ---
        scroll = QScrollArea()
        container = QWidget()
        layout = QVBoxLayout(container)

        # Label
        label = QLabel("Chunked Word Recall Heatmap")
        layout.addWidget(label)

        # --- Figure & GridSpec ---
        num_chunks = int(np.ceil(len(df.columns) / words_per_chunk))
        rows = int(np.ceil(num_chunks / cols))
        subplot_width = 10
        subplot_height = 10

        fig_width = cols * subplot_width
        fig_height = rows * subplot_height

        self.fig = plt.figure(figsize=(fig_width, fig_height))
        gs = GridSpec(
            rows, cols,
            figure=self.fig,
            left=0.03, right=0.97,
            top=0.97, bottom=0.03,
            hspace=0.3,
            wspace=0.3
        )

        # --- Plot each chunk ---
        for i in range(num_chunks):
            start = i * words_per_chunk
            end = start + words_per_chunk
            chunk = df.iloc[:, start:end]

            row = i // cols
            col = i % cols

            ax = self.fig.add_subplot(gs[row, col])
            sns.heatmap(chunk.T, cmap="YlOrRd", linewidths=0.3, ax=ax, cbar=True, annot=False)

            ax.set_title(f"Words {start+1}-{min(end,len(df.columns))}", fontsize=8, pad=2)
            ax.set_xlabel("Session", fontsize=8)
            ax.tick_params(axis='x', labelsize=6)
            ax.tick_params(axis='y', labelsize=6)

        # --- Canvas & Toolbar ---
        canvas = FigureCanvas(self.fig)
        layout.addWidget(canvas)

        toolbar = NavigationToolbar(canvas, self)
        layout.addWidget(toolbar)

        scroll.setWidget(container)
        scroll.setWidgetResizable(True)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)


# --- Run App ---
app = QApplication(sys.argv)
window = ChunkedHeatmapViewer(df)
window.show()
sys.exit(app.exec())




"""
Zoom with mouse but bad mouse positions
"""
# import sys
# import os
# import json
# from PyQt6.QtGui import QPainter
# from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea, QLabel, QSizePolicy
# from PyQt6.QtCore import pyqtSignal, Qt, QEvent, QObject
# from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
# import matplotlib.pyplot as plt
# import seaborn as sns
# import pandas as pd
# import numpy as np
# from matplotlib.gridspec import GridSpec

# plt.rcParams['font.family'] = 'MS Gothic'

# # --- Load your session data ---
# folder_path = r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data\sessions"
# session_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.json')]
# session_files.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0].split('(')[-1].split(')')[0]))

# # --- Build initial 0/1 session-word counts ---
# session_word_data = {}
# for file in session_files:
#     with open(file, 'r', encoding='utf-8') as f:
#         data = json.load(f)
#     session_num = data["session_num"]
#     words = data.get("new_words", []) + data.get("old_words", [])
#     for word in words:
#         if word not in session_word_data:
#             session_word_data[word] = {}
#         session_word_data[word][session_num] = 1  # just mark appeared

# df_sessions = pd.DataFrame(session_word_data).fillna(0).astype(int)
# df_sessions = df_sessions.sort_index()
# df_sessions = df_sessions[df_sessions.sum(axis=0).sort_values(ascending=False).index]

# # --- Convert to incremental session numbers ---
# df_incremental = pd.DataFrame(0, index=df_sessions.index, columns=df_sessions.columns)

# for word in df_sessions.columns:
#     count = 0
#     for session in df_sessions.index:
#         if df_sessions.at[session, word] > 0:
#             count += 1
#             df_incremental.at[session, word] = count
#         else:
#             df_incremental.at[session, word] = 0

# # --- Custom Canvas with QTransform Zoom ---
# from PyQt6.QtWidgets import QLabel, QScrollArea, QSizePolicy
# from PyQt6.QtGui import QPixmap, QImage, QMouseEvent
# from PyQt6.QtCore import Qt
# from io import BytesIO

# class ZoomableImage(QLabel):
#     def __init__(self, figure, scroll_area: QScrollArea, dpi=150):
#         super().__init__()
#         self.scroll_area = scroll_area
#         self.zoom_factor = 1.0
#         self.min_zoom, self.max_zoom = 0.25, 5.0
#         self.drag_start_pos = None

#         # Render figure once to image
#         buf = BytesIO()
#         figure.savefig(buf, format="png", dpi=dpi, bbox_inches="tight")
#         buf.seek(0)

#         qimg = QImage.fromData(buf.read(), "PNG")
#         self.pixmap_original = QPixmap.fromImage(qimg)
#         self.setPixmap(self.pixmap_original)

#         # Make label resizable
#         self.setScaledContents(True)
#         self.resize(self.pixmap_original.size())
#         self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

#     # --- Zoom ---
#     def wheelEvent(self, event):
#         if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
#             angle = event.angleDelta().y()
#             factor = 1.2 if angle > 0 else 1 / 1.2
#             new_zoom = self.zoom_factor * factor
#             new_zoom = max(self.min_zoom, min(new_zoom, self.max_zoom))
#             if abs(new_zoom - self.zoom_factor) > 1e-3:
#                 self.zoom_to(event.position(), new_zoom / self.zoom_factor)
#             event.accept()
#         else:
#             super().wheelEvent(event)

#     def zoom_to(self, cursor_pos, factor):
#         hbar = self.scroll_area.horizontalScrollBar()
#         vbar = self.scroll_area.verticalScrollBar()

#         # Cursor position relative to scroll content
#         cursor_x = hbar.value() + cursor_pos.x()
#         cursor_y = vbar.value() + cursor_pos.y()

#         # Apply zoom
#         self.zoom_factor *= factor
#         new_size = self.pixmap_original.size() * self.zoom_factor
#         self.resize(new_size)

#         # Adjust scrollbars to keep cursor in place
#         hbar.setValue(int(cursor_x * factor - cursor_pos.x()))
#         vbar.setValue(int(cursor_y * factor - cursor_pos.y()))

#     # --- Pan ---
#     def mousePressEvent(self, event):
#         if event.button() == Qt.MouseButton.LeftButton:
#             self.drag_start_pos = event.position()
#             self.setCursor(Qt.CursorShape.ClosedHandCursor)
#             event.accept()
#         else:
#             super().mousePressEvent(event)

#     def mouseMoveEvent(self, event):
#         if self.drag_start_pos is not None:
#             delta = event.position() - self.drag_start_pos
#             hbar = self.scroll_area.horizontalScrollBar()
#             vbar = self.scroll_area.verticalScrollBar()
#             hbar.setValue(hbar.value() - int(delta.x()))
#             vbar.setValue(vbar.value() - int(delta.y()))
#             self.drag_start_pos = event.position()
#             event.accept()
#         else:
#             super().mouseMoveEvent(event)

#     def mouseReleaseEvent(self, event):
#         if event.button() == Qt.MouseButton.LeftButton:
#             self.drag_start_pos = None
#             self.setCursor(Qt.CursorShape.ArrowCursor)
#             event.accept()
#         else:
#             super().mouseReleaseEvent(event)

# # --- Viewer ---
# class ChunkedHeatmapViewer(QWidget):
#     def __init__(self, df, words_per_chunk=40, cols=5):
#         super().__init__()
#         self.setWindowTitle("Scrollable Chunked Heatmap (Zoom Safe)")
#         self.resize(1400, 900)

#         # --- Scroll area ---
#         scroll = QScrollArea()
#         container = QWidget()
#         layout = QVBoxLayout(container)

#         # # Label
#         # label = QLabel("Chunked Word Recall Heatmap (Incremental Sessions)")
#         # layout.addWidget(label)

#         # --- Figure & GridSpec ---
#         num_chunks = int(np.ceil(len(df.columns) / words_per_chunk))
#         rows = int(np.ceil(num_chunks / cols))
#         subplot_width = 10
#         subplot_height = 10

#         fig_width = cols * subplot_width
#         fig_height = rows * subplot_height

#         self.fig = plt.figure(figsize=(fig_width, fig_height))
#         gs = GridSpec(
#             rows, cols,
#             figure=self.fig,
#             left=0.02, right=0.98,
#             top=0.98, bottom=0.02,
#             hspace=0.15,
#             wspace=0.15
#         )

#         vmin = df.values.min()
#         vmax = df.values.max()

#         for i in range(num_chunks):
#             start = i * words_per_chunk
#             end = start + words_per_chunk
#             chunk = df.iloc[:, start:end]

#             row = i // cols
#             col = i % cols

#             ax = self.fig.add_subplot(gs[row, col])
#             sns.heatmap(
#                 chunk.T,
#                 cmap="YlOrRd",
#                 linewidths=0.1,
#                 ax=ax,
#                 cbar=True,
#                 annot=False,
#                 vmin=vmin,
#                 vmax=vmax
#             )

#             ax.set_title(f"Words {start+1}-{min(end,len(df.columns))}", fontsize=8, pad=2)
#             ax.set_xlabel("Session", fontsize=8)
#             ax.tick_params(axis='x', labelsize=6)
#             ax.tick_params(axis='y', labelsize=6)

#         # self.fig.tight_layout(pad=0.5)

#         # --- Safe zoom canvas ---
#         self.image_label = ZoomableImage(self.fig, scroll_area=scroll, dpi=150)
#         layout.addWidget(self.image_label)

#         # scroll = QScrollArea()
#         # viewer = ZoomableImage(self.fig, scroll_area=scroll, dpi=150)
#         # scroll.setWidget(viewer)
#         # scroll.setWidgetResizable(True)
#         # layout.addWidget(scroll)

#         # toolbar = NavigationToolbar(self.canvas, self)
#         # layout.addWidget(toolbar)

#         scroll.setWidget(container)
#         scroll.setWidgetResizable(True)

#         main_layout = QVBoxLayout(self)
#         main_layout.addWidget(scroll)
#         self.setLayout(main_layout)


# # --- Run App ---
# app = QApplication(sys.argv)
# window = ChunkedHeatmapViewer(df_incremental)
# window.show()
# sys.exit(app.exec())




















