# import sys
# import os
# import json
# from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea, QLabel
# from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
# import matplotlib.pyplot as plt
# import seaborn as sns
# import pandas as pd
# import numpy as np
# from matplotlib.gridspec import GridSpec

# plt.rcParams['font.family'] = 'MS Gothic'

# # ---------------------------------------------
# # Load session data and build recency heatmap
# # ---------------------------------------------
# folder_path = r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data\sessions"
# session_files = [os.path.join(folder_path, f) 
#                  for f in os.listdir(folder_path) if f.endswith('.json')]

# # sort by session number like (1).json, (2).json...
# session_files.sort(
#     key=lambda x: int(os.path.splitext(os.path.basename(x))[0].split('(')[-1].split(')')[0])
# )

# # Recency heat parameters
# boost = 1.0
# decay = 0.90

# heat_state = {}          # running heat values per word
# heat_by_session = {}     # session_num -> {word: heat_value}

# # Build the recency-based heat map
# for file in session_files:
#     with open(file, 'r', encoding='utf-8') as f:
#         data = json.load(f)

#     session_num = data["session_num"]
#     words = data.get("new_words", []) + data.get("old_words", [])

#     # decay existing heat
#     for w in heat_state:
#         heat_state[w] *= decay

#     # boost heat for used words
#     for w in words:
#         if w not in heat_state:
#             heat_state[w] = 0.0
#         heat_state[w] += boost

#     # save snapshot for this session
#     heat_by_session[session_num] = dict(heat_state)

# # Convert to DataFrame: rows = sessions, columns = words
# df = pd.DataFrame(heat_by_session).T.fillna(0)

# # Sort rows and columns
# df = df.sort_index()
# df = df[df.sum(axis=0).sort_values(ascending=False).index]


# # ---------------------------------------------
# # PyQt6 Heatmap Viewer
# # ---------------------------------------------
# class ChunkedHeatmapViewer(QWidget):
#     def __init__(self, df, words_per_chunk=40, cols=3):
#         super().__init__()
#         self.setWindowTitle("Scrollable Recency-Based Recall Heatmap")
#         self.resize(1400, 900)

#         scroll = QScrollArea()
#         container = QWidget()
#         layout = QVBoxLayout(container)

#         label = QLabel("Recency-Based Word Recall Heatmap")
#         layout.addWidget(label)

#         # How many heatmaps we need
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
#             left=0.03, right=0.97,
#             top=0.97, bottom=0.03,
#             hspace=0.3,
#             wspace=0.3
#         )

#         # Build each chunked heatmap
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
#                 linewidths=0.3,
#                 ax=ax,
#                 cbar=True,
#                 annot=False
#             )

#             ax.set_title(f"Words {start+1}-{min(end, len(df.columns))}", fontsize=8, pad=2)
#             ax.set_xlabel("Session", fontsize=8)
#             ax.tick_params(axis='x', labelsize=6)
#             ax.tick_params(axis='y', labelsize=6)

#         canvas = FigureCanvas(self.fig)
#         layout.addWidget(canvas)

#         toolbar = NavigationToolbar(canvas, self)
#         layout.addWidget(toolbar)

#         scroll.setWidget(container)
#         scroll.setWidgetResizable(True)

#         main_layout = QVBoxLayout(self)
#         main_layout.addWidget(scroll)
#         self.setLayout(main_layout)


# # ---------------------------------------------
# # Run app
# # ---------------------------------------------
# app = QApplication(sys.argv)
# window = ChunkedHeatmapViewer(df)
# window.show()
# sys.exit(app.exec())





"""
Recency-based recall heatmap with interactive UI:
- Dropdown + custom selection (single, range, list)
- Prev/Next buttons
- Keyboard shortcuts (←, →, Ctrl+N etc.)
- Clickable chunk titles to jump to chunk
- Real-time re-render (no window recreation)
- Compact overview panel (clickable tiles)
"""

import sys
import os
import json
from functools import partial

import json
import os
from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *


import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.gridspec import GridSpec

import seaborn as sns
import pandas as pd
import numpy as np

# -------------------------
# CONFIG
# -------------------------
SESSIONS_FOLDER = r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data\sessions"
WORDS_PER_CHUNK = 40
CHUNKS_COLS = 3
BOOST = 1.0
DECAY = 0.90
OVERVIEW_TILE_SIZE = (120, 40)  # width, height px

plt.rcParams['font.family'] = 'MS Gothic'

# -------------------------
# DATA LOADER: recency heat computation
# -------------------------
def load_sessions_heat(folder_path, boost=BOOST, decay=DECAY):
    # Build ordered list of session files
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.json')]
    # sort by session number using same parsing as user code
    def session_key(x):
        base = os.path.splitext(os.path.basename(x))[0]
        # attempt to find (num)
        try:
            return int(base.split('(')[-1].split(')')[0])
        except Exception:
            # fallback: sort by filename
            return base
    files.sort(key=session_key)

    heat_state = {}
    heat_by_session = {}
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        session_num = data.get("session_num", None)
        # fall back to sequence index if no explicit session_num
        if session_num is None:
            # attempt to derive from filename ordering
            session_num = len(heat_by_session) + 1
        words = data.get("new_words", []) + data.get("old_words", [])
        # decay
        for w in list(heat_state.keys()):
            heat_state[w] *= decay
        # boost
        for w in words:
            heat_state.setdefault(w, 0.0)
            heat_state[w] += boost
        heat_by_session[session_num] = dict(heat_state)

    if not heat_by_session:
        # empty DataFrame fallback
        return pd.DataFrame()

    df = pd.DataFrame(heat_by_session).T.fillna(0)
    df = df.sort_index()
    # sort words by total heat descending
    df = df[df.sum(axis=0).sort_values(ascending=False).index]
    return df

# -------------------------
# Utility: chunk math
# -------------------------
def total_chunks_for_df(df, words_per_chunk=WORDS_PER_CHUNK):
    if df is None or df.empty:
        return 0
    return int(np.ceil(len(df.columns) / words_per_chunk))

def chunk_slice(chunk_index, words_per_chunk=WORDS_PER_CHUNK, total_words=None):
    start = chunk_index * words_per_chunk
    end = start + words_per_chunk
    if total_words is not None:
        end = min(end, total_words)
    return start, end

# -------------------------
# UI: Main interactive window
# -------------------------
class HeatmapMainWindow(QWidget):
    def __init__(self, df, words_per_chunk=WORDS_PER_CHUNK, cols=CHUNKS_COLS):
        super().__init__()
        self.df = df.copy() if (df is not None) else pd.DataFrame()
        self.words_per_chunk = words_per_chunk
        self.cols = cols

        self.total_chunks = total_chunks_for_df(self.df, words_per_chunk=self.words_per_chunk)
        self.chunk_indices = list(range(self.total_chunks))  # full set
        self.current_chunk_positions = [0] if self.total_chunks > 0 else []
        # current visible chunk indices (0-based); default show chunk 0
        self.visible_chunk_indices = [0] if self.total_chunks > 0 else []

        # Setup UI
        self.setWindowTitle("Recency-Based Recall Heatmap — Interactive Viewer")
        self.resize(1400, 900)
        self._build_ui()
        self._connect_shortcuts()
        self._render()  # initial render

    # -------------------------
    # UI Construction
    # -------------------------
    def _build_ui(self):
        main_layout = QVBoxLayout(self)

        # Top control bar
        controls = QHBoxLayout()
        self.combo = QComboBox()
        self.combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self._populate_combo()
        controls.addWidget(QLabel("Select Chunks:"))
        controls.addWidget(self.combo)

        self.custom_line = QLineEdit()
        self.custom_line.setPlaceholderText("e.g. 1 or 1-3 or 1,4,6")
        self.custom_apply_btn = QPushButton("Apply")
        controls.addWidget(self.custom_line)
        controls.addWidget(self.custom_apply_btn)

        self.prev_btn = QPushButton("← Prev")
        self.next_btn = QPushButton("Next →")
        controls.addWidget(self.prev_btn)
        controls.addWidget(self.next_btn)

        self.overview_toggle = QCheckBox("Show Overview")
        self.overview_toggle.setChecked(True)
        controls.addWidget(self.overview_toggle)

        # Add stretch to push controls left
        controls.addStretch()
        main_layout.addLayout(controls)

        # Middle splitter: left = canvas, right = overview tiles
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left: central canvas area with toolbar
        left_frame = QFrame()
        left_layout = QVBoxLayout(left_frame)

        # Matplotlib figure & canvas
        self.fig = plt.Figure(figsize=(10, 8))
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        left_layout.addWidget(self.canvas)
        left_layout.addWidget(self.toolbar)

        splitter.addWidget(left_frame)

        # Right: overview list (scrollable)
        self.overview_list = QListWidget()
        self.overview_list.setFixedWidth(OVERVIEW_TILE_SIZE[0] + 40)
        splitter.addWidget(self.overview_list)

        splitter.setStretchFactor(0, 8)
        splitter.setStretchFactor(1, 2)
        main_layout.addWidget(splitter)

        # Status label
        self.status_label = QLabel("")
        main_layout.addWidget(self.status_label)

        # Wire UI events
        self.custom_apply_btn.clicked.connect(self._on_apply_custom)
        self.combo.currentIndexChanged.connect(self._on_combo_changed)
        self.prev_btn.clicked.connect(self._on_prev_clicked)
        self.next_btn.clicked.connect(self._on_next_clicked)
        self.overview_toggle.stateChanged.connect(self._on_overview_toggle)
        self.overview_list.itemClicked.connect(self._on_overview_item_clicked)

        # Matplotlib pick & click handlers
        self.canvas.mpl_connect("pick_event", self._on_pick_event)

    def _populate_combo(self):
        self.combo.clear()
        self.combo.addItem("All Chunks")
        for i in range(self.total_chunks):
            self.combo.addItem(f"Chunk {i+1}")
        self.combo.addItem("Range (dialog)")
        self.combo.addItem("Custom list (dialog)")
        # default selected: first chunk if exists
        if self.total_chunks > 0:
            self.combo.setCurrentIndex(1)  # Chunk 1

    # -------------------------
    # Shortcuts & Keybindings
    # -------------------------
    def _connect_shortcuts(self):
        # Left / Right
        QShortcut(QKeySequence(Qt.Key.Key_Left), self, activated=self._on_prev_clicked)
        QShortcut(QKeySequence(Qt.Key.Key_Right), self, activated=self._on_next_clicked)
        # Ctrl + A => show all
        QShortcut(QKeySequence("Ctrl+A"), self, activated=self._show_all_chunks)
        # Ctrl + O => open dialog to enter custom range/list
        QShortcut(QKeySequence("Ctrl+O"), self, activated=self._open_range_dialog)
        # Ctrl + H => toggle overview
        QShortcut(QKeySequence("Ctrl+H"), self, activated=lambda: self.overview_toggle.toggle())

        # Ctrl + 1..9 jump to chunk 1..9 if available
        for i in range(1, 10):
            seq = QKeySequence(f"Ctrl+{i}")
            QShortcut(seq, self, activated=partial(self._ctrl_number_jump, i))

    def _ctrl_number_jump(self, n):
        if 1 <= n <= self.total_chunks:
            self.visible_chunk_indices = [n-1]
            self.combo.setCurrentIndex(n)  # align combo (Chunk n)
            self._render()

    # -------------------------
    # Event handlers
    # -------------------------
    def _on_combo_changed(self, idx):
        # All Chunks
        if idx == 0:
            self.visible_chunk_indices = list(range(self.total_chunks))
            self._render()
            return
        # individual chunk selection
        if 1 <= idx <= self.total_chunks:
            chunk_idx = idx - 1
            self.visible_chunk_indices = [chunk_idx]
            self._render()
            return
        # Range or Custom list selections should trigger dialog
        text = self.combo.currentText()
        if "Range" in text:
            self._open_range_dialog()
        elif "Custom list" in text:
            self._open_list_dialog()

    def _on_apply_custom(self):
        s = self.custom_line.text().strip()
        if not s:
            QMessageBox.warning(self, "Input required", "Please enter a chunk expression like '1' or '1-3' or '1,3,5'.")
            return
        try:
            indices = self._parse_chunk_expression(s)
            if not indices:
                QMessageBox.warning(self, "No chunks", "Parsed to no valid chunk indices.")
                return
            self.visible_chunk_indices = indices
            # keep combo in sync (set to "All Chunks" if multiple)
            if len(indices) == 1:
                self.combo.setCurrentIndex(indices[0] + 1)
            else:
                self.combo.setCurrentIndex(0)  # All Chunks
            self._render()
        except Exception as e:
            QMessageBox.critical(self, "Parse error", f"Couldn't parse input: {e}")

    def _on_prev_clicked(self):
        if not self.visible_chunk_indices:
            return
        # pick first visible chunk and move left one chunk
        first = self.visible_chunk_indices[0]
        target = max(0, first - 1)
        self.visible_chunk_indices = [target]
        # sync combo
        self.combo.setCurrentIndex(target + 1)
        self._render()

    def _on_next_clicked(self):
        if not self.visible_chunk_indices:
            return
        last = self.visible_chunk_indices[-1]
        target = min(self.total_chunks - 1, last + 1)
        self.visible_chunk_indices = [target]
        self.combo.setCurrentIndex(target + 1)
        self._render()

    def _on_overview_toggle(self, state):
        self.overview_list.setVisible(self.overview_toggle.isChecked())

    def _on_overview_item_clicked(self, item: QListWidgetItem):
        idx = item.data(Qt.ItemDataRole.UserRole)
        if idx is None:
            return
        self.visible_chunk_indices = [idx]
        self.combo.setCurrentIndex(idx + 1)
        self._render()

    # Matplotlib pick (click on titles)
    def _on_pick_event(self, event):
        # when title text picked, find its axes and chunk index from stored mapping
        artist = event.artist
        if hasattr(artist, "get_text"):  # likely text object
            txt = artist
            # we embedded chunk index in txt._chunk_idx (see draw)
            chunk_idx = getattr(txt, "_chunk_idx", None)
            if chunk_idx is not None:
                self.visible_chunk_indices = [chunk_idx]
                self.combo.setCurrentIndex(chunk_idx + 1)
                self._render()

    # -------------------------
    # Parsing helpers
    # -------------------------
    def _parse_chunk_expression(self, s):
        s = s.strip()
        if not s:
            return []
        # single number
        if s.isdigit():
            n = int(s)
            return [n-1] if 1 <= n <= self.total_chunks else []
        # range: "a-b"
        if '-' in s and ',' not in s:
            parts = s.split('-')
            if len(parts) != 2:
                raise ValueError("Range must be like '1-3'")
            a, b = int(parts[0]), int(parts[1])
            if a > b:
                a, b = b, a
            return [i for i in range(a-1, b) if 0 <= i < self.total_chunks]
        # list: comma separated
        parts = [p.strip() for p in s.split(',') if p.strip()]
        indices = []
        for p in parts:
            if p.isdigit():
                n = int(p)
                if 1 <= n <= self.total_chunks:
                    indices.append(n-1)
        return sorted(set(indices))

    # Dialogs
    def _open_range_dialog(self):
        text, ok = QInputDialog.getText(self, "Range", "Enter chunk range (e.g. 1-3):")
        if ok and text:
            try:
                indices = self._parse_chunk_expression(text)
                if not indices:
                    QMessageBox.warning(self, "No chunks", "Parsed to no valid chunk indices.")
                    return
                self.visible_chunk_indices = indices
                self._render()
            except Exception as e:
                QMessageBox.critical(self, "Parse error", str(e))

    def _open_list_dialog(self):
        text, ok = QInputDialog.getText(self, "Custom list", "Enter chunk list (e.g. 1,4,6):")
        if ok and text:
            try:
                indices = self._parse_chunk_expression(text)
                if not indices:
                    QMessageBox.warning(self, "No chunks", "Parsed to no valid chunk indices.")
                    return
                self.visible_chunk_indices = indices
                self._render()
            except Exception as e:
                QMessageBox.critical(self, "Parse error", str(e))

    def _show_all_chunks(self):
        self.visible_chunk_indices = list(range(self.total_chunks))
        self.combo.setCurrentIndex(0)
        self._render()

    # -------------------------
    # Rendering
    # -------------------------
    def _render(self):
        # clear figure
        self.fig.clf()
        # if no data, show placeholder text
        if self.df is None or self.df.empty or self.total_chunks == 0:
            ax = self.fig.add_subplot(111)
            ax.text(0.5, 0.5, "No session data found or empty folder.", ha='center', va='center')
            ax.axis('off')
            self.canvas.draw()
            return

        # compute visible chunks list in 0-based indices
        vis = sorted(set(self.visible_chunk_indices))
        if not vis:
            vis = [0]  # fallback

        # how many subplots will we draw
        num_to_draw = len(vis)
        rows = int(np.ceil(num_to_draw / self.cols))
        gs = GridSpec(rows, self.cols, figure=self.fig, left=0.03, right=0.75 if self.overview_toggle.isChecked() else 0.97,
                      top=0.97, bottom=0.03, hspace=0.4, wspace=0.4)

        # Map to remember axes->chunk index for clickable titles
        self._ax_chunk_map = {}

        # Draw chunk heatmaps
        for plot_pos, chunk_idx in enumerate(vis):
            start, end = chunk_slice(chunk_idx, words_per_chunk=self.words_per_chunk, total_words=len(self.df.columns))
            chunk_df = self.df.iloc[:, start:end]
            row = plot_pos // self.cols
            col = plot_pos % self.cols
            ax = self.fig.add_subplot(gs[row, col])
            sns.heatmap(chunk_df.T, cmap="YlOrRd", linewidths=0.3, ax=ax, cbar=True, annot=False)

            title = f"Chunk {chunk_idx+1} (Words {start+1}-{end})"
            t = ax.set_title(title, fontsize=9, pad=2, picker=True)  # make title pickable
            # store chunk idx on title artist for pick event
            try:
                t._chunk_idx = chunk_idx
            except Exception:
                pass
            self._ax_chunk_map[ax] = chunk_idx

            ax.set_xlabel("Session", fontsize=8)
            ax.tick_params(axis='x', labelsize=6)
            ax.tick_params(axis='y', labelsize=6)

        # draw overview (right side) if enabled
        if self.overview_toggle.isChecked():
            self._draw_overview(right_area=True)

        # update status
        self.status_label.setText(f"Showing chunks: {', '.join(str(i+1) for i in vis)}  —  Total chunks: {self.total_chunks}")
        self.canvas.draw_idle()

    def _draw_overview(self, right_area=True):
        # Overview is implemented as a QListWidget with colored pixmaps
        self.overview_list.clear()
        max_value = self.df.values.max() if (self.df is not None and not self.df.empty) else 1.0
        if max_value == 0:
            max_value = 1.0

        for chunk_idx in range(self.total_chunks):
            start, end = chunk_slice(chunk_idx, words_per_chunk=self.words_per_chunk, total_words=len(self.df.columns))
            chunk_df = self.df.iloc[:, start:end]
            # Compute a summary scalar per chunk: max heat (or mean or other)
            val = float(chunk_df.values.max()) if chunk_df.size > 0 else 0.0
            norm_val = val / max_value

            # Build pixmap for tile
            w, h = OVERVIEW_TILE_SIZE
            pix = QPixmap(w, h)
            pix.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pix)
            # Map normalized value [0,1] to a colormap via matplotlib
            cmap = plt.get_cmap("YlOrRd")
            rgba = cmap(norm_val)
            color = QColor(int(rgba[0]*255), int(rgba[1]*255), int(rgba[2]*255))
            painter.fillRect(0, 0, w, h, QBrush(color))
            painter.setPen(Qt.GlobalColor.black)
            painter.drawText(8, int(h/2)+6, f"Chunk {chunk_idx+1}  ({start+1}-{end})")
            painter.end()

            item = QListWidgetItem()
            item.setSizeHint(QSize(w+20, h+10))
            item.setData(Qt.ItemDataRole.UserRole, chunk_idx)
            # item.setIcon(pix)
            item.setText(f"  Chunk {chunk_idx+1}")
            self.overview_list.addItem(item)

    # -------------------------
    # Public: update data and re-render live
    # -------------------------
    def update_df(self, new_df):
        """
        Replace underlying DataFrame and re-render. Keeps UI alive.
        """
        self.df = new_df.copy() if (new_df is not None) else pd.DataFrame()
        self.total_chunks = total_chunks_for_df(self.df, words_per_chunk=self.words_per_chunk)
        # clamp visible indices
        self.visible_chunk_indices = [i for i in self.visible_chunk_indices if i < self.total_chunks]
        if not self.visible_chunk_indices and self.total_chunks > 0:
            self.visible_chunk_indices = [0]
        self._populate_combo()
        self._render()

# -------------------------
# Entrypoint
# -------------------------
def main():
    df = load_sessions_heat(SESSIONS_FOLDER, boost=BOOST, decay=DECAY)
    app = QApplication(sys.argv)
    win = HeatmapMainWindow(df, words_per_chunk=WORDS_PER_CHUNK, cols=CHUNKS_COLS)
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
