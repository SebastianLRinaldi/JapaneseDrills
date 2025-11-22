"""
Single session Example
"""
# import json
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns


# plt.rcParams['font.family'] = 'MS Gothic'



# # --- Load session JSON file ---
# path = r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data\sessions\session(10)_2025-11-06.json"
# with open(path, "r", encoding="utf-8") as f:
#     session_data = json.load(f)


# # --- Convert events to DataFrame ---
# df = pd.DataFrame(session_data['events'])

# # --- Configurable time bin size (seconds) ---
# time_bin_size = 60  # change to 30, 120, etc.

# # --- Assign bin number starting from 0 ---
# df['bin_num'] = (df['timestamp'] // time_bin_size).astype(int)

# # --- Stack within each bin ---
# df['stack_y'] = df.groupby('bin_num').cumcount() + 1

# # --- Compute bar heights per bin ---
# bin_counts = df.groupby('bin_num').size()

# # --- Plot ---
# fig, ax = plt.subplots(figsize=(14, 6))

# # Bar chart (per bin, contiguous)
# ax.bar(bin_counts.index, bin_counts.values, width=1, alpha=0.2, color='gray', align='edge', label=f'Words per {time_bin_size}s')

# # Scatter points for words (stacked)
# colors = df['type'].map({'old': 'blue', 'new': 'red'})
# ax.scatter(df['bin_num'] + 0.5, df['stack_y'], c=colors, s=80)  # +0.5 to center points in bar

# # Annotate words
# for _, row in df.iterrows():
#     ax.text(row['bin_num'] + 0.5, row['stack_y'] + 0.1, row['word'], ha='center', fontsize=9)

# # --- Formatting ---
# ax.set_xlabel('Time bin (index)')
# ax.set_ylabel('Word stack per bin')
# ax.set_title(f"Session {session_data['session_num']} Word Timeline (Stacked, Contiguous Bins)")
# ax.set_xticks(bin_counts.index + 0.5)
# ax.set_xticklabels([f"{i*time_bin_size}-{(i+1)*time_bin_size}s" for i in bin_counts.index], rotation=45)

# ax.legend(handles=[
#     plt.Line2D([0], [0], marker='o', color='w', label='Old', markerfacecolor='blue', markersize=10),
#     plt.Line2D([0], [0], marker='o', color='w', label='New', markerfacecolor='red', markersize=10),
#     plt.Line2D([0], [0], color='gray', lw=10, alpha=0.2, label=f'Words per {time_bin_size}s')
# ])

# plt.tight_layout()
# plt.show()









import sys
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends import backend_qtagg
from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

plt.rcParams['font.family'] = 'MS Gothic'

# --- Folder path ---
folder_path = r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data\sessions"

# --- Load all JSON files ---
session_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.json')]

class SessionViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Session Word Timeline Viewer")
        self.current_index = 0

        # Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Session label
        self.session_label = QLabel("")
        self.layout.addWidget(self.session_label)

        # Matplotlib Figure
        FigureCanvas = backend_qtagg.FigureCanvasQTAgg
        self.fig, self.ax = plt.subplots(figsize=(14,6))
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)

        # Navigation buttons
        nav_layout = QHBoxLayout()
        self.prev_btn = QPushButton("← Previous")
        self.next_btn = QPushButton("Next →")
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.next_btn)
        self.layout.addLayout(nav_layout)

        self.prev_btn.clicked.connect(self.prev_session)
        self.next_btn.clicked.connect(self.next_session)

        self.load_session()

    def load_session(self):
        path = session_files[self.current_index]
        with open(path, "r", encoding="utf-8") as f:
            session_data = json.load(f)
        self.session_label.setText(f"Session {session_data['session_num']} - {session_data['date']}")

        self.ax.clear()

        # --- Determine session format ---
        events = session_data.get('events', [])
        if events:
            # --- Event-based timeline ---
            df = pd.DataFrame(events)
            time_bin_size = 60
            df['bin_num'] = (df['timestamp'] // time_bin_size).astype(int)
            df['stack_y'] = df.groupby('bin_num').cumcount() + 1
            bin_counts = df.groupby('bin_num').size()

            # Bars
            self.ax.bar(bin_counts.index, bin_counts.values, width=1, alpha=0.2, color='gray', align='edge')
            # Scatter
            colors = df['type'].map({'old': 'blue', 'new': 'red'})
            self.ax.scatter(df['bin_num'] + 0.5, df['stack_y'], c=colors, s=80)
            # Annotate words
            for _, row in df.iterrows():
                self.ax.text(row['bin_num'] + 0.5, row['stack_y'] + 0.1, row['word'], ha='center', fontsize=9)
            # X-axis
            self.ax.set_xticks(bin_counts.index + 0.5)
            self.ax.set_xticklabels([f"{i*time_bin_size}-{(i+1)*time_bin_size}s" for i in bin_counts.index], rotation=45)
            self.ax.set_xlabel("Time bin")
            self.ax.set_ylabel("Word stack per bin")
            self.ax.set_title(f"Session {session_data['session_num']} Word Timeline")
            self.ax.legend(handles=[
                plt.Line2D([0], [0], marker='o', color='w', label='Old', markerfacecolor='blue', markersize=10),
                plt.Line2D([0], [0], marker='o', color='w', label='New', markerfacecolor='red', markersize=10),
                plt.Line2D([0], [0], color='gray', lw=10, alpha=0.2, label=f'Words per {time_bin_size}s')
            ])
        else:
            # --- Fallback for older format ---
            new_count = session_data.get('new_count', 0)
            old_count = session_data.get('old_count', 0)
            counts = [old_count, new_count]
            labels = ['Old', 'New']
            colors = ['blue', 'red']

            self.ax.bar(labels, counts, color=colors, alpha=0.7)
            for i, count in enumerate(counts):
                self.ax.text(i, count + 0.5, str(count), ha='center', va='bottom', fontsize=12)
            self.ax.set_ylabel("Word count")
            self.ax.set_title(f"Session {session_data['session_num']} Word Counts")
        
        self.fig.tight_layout()
        self.canvas.draw()

    def prev_session(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_session()

    def next_session(self):
        if self.current_index < len(session_files) - 1:
            self.current_index += 1
            self.load_session()


# --- Run ---
app = QApplication(sys.argv)
viewer = SessionViewer()
viewer.show()
sys.exit(app.exec())

