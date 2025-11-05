from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from .widgets.ScenePlayer import ScenePlayer

from .Layout import Layout


class Scene:
    def __init__(self, sentence):
        self.sentence = sentence
        self.strokes = []  # list of (points: List[QPointF], pen: QPen)
        self.images = []   # unused here but placeholder
        self.bg_pixmap = None


class Logic:
    def __init__(self, ui: Layout):
        self.ui = ui
        self.scenes = []

    def set_stroke_color(self, color_name):
        print(f"COLOR: {color_name}")
        self.ui.canvas.stroke_color = QColor(color_name)
        self.ui.canvas.update()

    def set_stroke_width(self, val):
        self.ui.canvas.stroke_width = val
        self.ui.canvas.update()

    def refresh_scene_list(self):
        self.ui.scene_list.clear()
        for i, scene in enumerate(self.scenes):
            txt = scene.sentence or "(no sentence)"
            display = txt if len(txt) < 30 else txt[:27] + "..."
            self.ui.scene_list.addItem(f"{i+1}: {display}")
        if self.scenes:
            current_row = self.ui.scene_list.currentRow()
            self.ui.scene_list.setCurrentRow(current_row if current_row >= 0 else 0)
        else:
            self.ui.text_edit.clear()
            self.ui.canvas.set_scene(None)

    def add_scene(self):
        text = self.ui.text_edit.toPlainText().strip()
        if not text:
            QMessageBox.warning(self.ui, "Empty Sentence", "Please enter a sentence.")
            return
        self.scenes.append(Scene(text))
        self.refresh_scene_list()

    def update_scene(self):
        row = self.ui.scene_list.currentRow()
        if row < 0:
            QMessageBox.warning(self.ui, "No Selection", "Select a scene first.")
            return
        text = self.ui.text_edit.toPlainText().strip()
        if not text:
            QMessageBox.warning(self.ui, "Empty Sentence", "Please enter a sentence.")
            return
        self.scenes[row].sentence = text
        self.refresh_scene_list()

    def clear_drawing(self):
        row = self.ui.scene_list.currentRow()
        if row < 0:
            return
        scene = self.scenes[row]
        scene.strokes.clear()
        scene.images.clear()
        scene.bg_pixmap = None
        self.ui.canvas.set_scene(scene)

    def delete_scene(self):
        row = self.ui.scene_list.currentRow()
        if row < 0:
            return
        del self.scenes[row]
        self.refresh_scene_list()

    def load_scene(self, row):
        if row < 0 or row >= len(self.scenes):
            self.ui.text_edit.clear()
            self.ui.canvas.set_scene(None)
            return
        scene = self.scenes[row]
        self.ui.text_edit.setText(scene.sentence)
        self.ui.canvas.set_scene(scene)

    def open_player(self):
        if not self.scenes:
            QMessageBox.warning(self.ui, "No Scenes", "Please add some scenes first.")
            return
        self.player = ScenePlayer(self.scenes)
        self.player.show()