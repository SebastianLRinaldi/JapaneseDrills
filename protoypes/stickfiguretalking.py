# import sys
# from PyQt6.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QHBoxLayout,
#     QPushButton, QTextEdit, QLabel, QListWidget, QMessageBox
# )
# from PyQt6.QtCore import QTimer, Qt, QRectF, QPointF
# from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QBrush

# class Scene:
#     def __init__(self, sentence):
#         self.sentence = sentence

# class SceneEditor(QWidget):
#     def __init__(self, parent):
#         super().__init__()
#         self.parent = parent
#         self.setWindowTitle("Scene Editor")
#         self.setMinimumSize(400, 300)

#         self.layout = QVBoxLayout()

#         self.scene_list = QListWidget()
#         self.layout.addWidget(self.scene_list)

#         self.text_edit = QTextEdit()
#         self.layout.addWidget(self.text_edit)

#         btn_layout = QHBoxLayout()
#         self.add_btn = QPushButton("Add Scene")
#         self.add_btn.clicked.connect(self.add_scene)
#         btn_layout.addWidget(self.add_btn)

#         self.update_btn = QPushButton("Update Scene")
#         self.update_btn.clicked.connect(self.update_scene)
#         btn_layout.addWidget(self.update_btn)

#         self.del_btn = QPushButton("Delete Scene")
#         self.del_btn.clicked.connect(self.delete_scene)
#         btn_layout.addWidget(self.del_btn)

#         self.layout.addLayout(btn_layout)
#         self.setLayout(self.layout)

#         self.scene_list.currentRowChanged.connect(self.load_scene)

#         self.refresh_scene_list()

#     def refresh_scene_list(self):
#         self.scene_list.clear()
#         for i, scene in enumerate(self.parent.scenes):
#             display_text = scene.sentence if len(scene.sentence) < 30 else scene.sentence[:27] + "..."
#             self.scene_list.addItem(f"{i+1}: {display_text}")
#         if self.parent.scenes:
#             self.scene_list.setCurrentRow(0)

#     def add_scene(self):
#         text = self.text_edit.toPlainText().strip()
#         if not text:
#             QMessageBox.warning(self, "Empty Sentence", "Please enter a sentence.")
#             return
#         self.parent.scenes.append(Scene(text))
#         self.refresh_scene_list()

#     def update_scene(self):
#         row = self.scene_list.currentRow()
#         if row == -1:
#             QMessageBox.warning(self, "No Scene Selected", "Please select a scene to update.")
#             return
#         text = self.text_edit.toPlainText().strip()
#         if not text:
#             QMessageBox.warning(self, "Empty Sentence", "Please enter a sentence.")
#             return
#         self.parent.scenes[row].sentence = text
#         self.refresh_scene_list()

#     def delete_scene(self):
#         row = self.scene_list.currentRow()
#         if row == -1:
#             QMessageBox.warning(self, "No Scene Selected", "Please select a scene to delete.")
#             return
#         del self.parent.scenes[row]
#         self.refresh_scene_list()

#     def load_scene(self, row):
#         if row == -1:
#             self.text_edit.clear()
#             return
#         self.text_edit.setText(self.parent.scenes[row].sentence)

# class ScenePlayer(QWidget):
#     def __init__(self, scenes):
#         super().__init__()
#         self.setWindowTitle("Scene Player")
#         self.setMinimumSize(700, 450)
#         self.scenes = scenes
#         self.index = 0
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.next_scene)
#         self.playing = False
#         self.display_time = 4000  # ms per scene

#         self.init_ui()

#     def init_ui(self):
#         self.next_btn = QPushButton("Next Scene")
#         self.next_btn.clicked.connect(self.next_scene)

#         self.play_btn = QPushButton("Play")
#         self.play_btn.clicked.connect(self.toggle_play)

#         self.layout = QVBoxLayout()
#         btn_layout = QHBoxLayout()
#         btn_layout.addWidget(self.next_btn)
#         btn_layout.addWidget(self.play_btn)
#         self.layout.addLayout(btn_layout)

#         self.setLayout(self.layout)

#     def toggle_play(self):
#         if self.playing:
#             self.timer.stop()
#             self.play_btn.setText("Play")
#         else:
#             self.timer.start(self.display_time)
#             self.play_btn.setText("Pause")
#         self.playing = not self.playing

#     def next_scene(self):
#         if not self.scenes:
#             return
#         self.index = (self.index + 1) % len(self.scenes)
#         self.update()

#     def paintEvent(self, event):
#         if not self.scenes:
#             return
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.RenderHint.Antialiasing)
#         painter.fillRect(self.rect(), QColor(255, 255, 255))

#         scene = self.scenes[self.index]
#         w, h = self.width(), self.height()

#         # Draw simple stick figure in center
#         center_x = w // 2
#         center_y = h // 2 + 50

#         self.draw_stick_figure(painter, center_x, center_y)

#         # Draw speech bubble with sentence
#         bubble_w, bubble_h = w * 0.8, 80
#         bubble_x = center_x - bubble_w/2
#         bubble_y = center_y - 150

#         self.draw_speech_bubble(painter, QRectF(bubble_x, bubble_y, bubble_w, bubble_h), scene.sentence)

#     def draw_stick_figure(self, painter, x, y):
#         pen = QPen(QColor(0,0,0), 3)
#         painter.setPen(pen)
#         painter.setBrush(Qt.BrushStyle.NoBrush)

#         # Head
#         painter.drawEllipse(x - 20, y - 120, 40, 40)
#         # Body
#         painter.drawLine(x, y - 80, x, y)
#         # Arms
#         painter.drawLine(x, y - 60, x - 40, y - 20)
#         painter.drawLine(x, y - 60, x + 40, y - 20)
#         # Legs
#         painter.drawLine(x, y, x - 40, y + 80)
#         painter.drawLine(x, y, x + 40, y + 80)

#     def draw_speech_bubble(self, painter, rect, text):
#         painter.setBrush(QBrush(QColor(255, 255, 224)))  # light yellow bubble
#         painter.setPen(QPen(QColor(0,0,0), 2))
#         painter.drawRoundedRect(rect, 15, 15)

#         # Tail bottom center
#         tail_w, tail_h = 20, 15
#         tail_points = [
#             QPointF(rect.center().x() - tail_w/2, rect.bottom()),
#             QPointF(rect.center().x() + tail_w/2, rect.bottom()),
#             QPointF(rect.center().x(), rect.bottom() + tail_h)
#         ]
#         painter.drawPolygon(*tail_points)

#         # Text
#         painter.setPen(QColor(0,0,0))
#         font = QFont("Arial", 16)
#         painter.setFont(font)
#         painter.drawText(rect.adjusted(10,10,-10,-10), Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap, text)

# class MainApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Scene Maker & Player")
#         self.setMinimumSize(800, 600)

#         self.scenes = []

#         self.layout = QVBoxLayout()

#         self.scene_editor_btn = QPushButton("Open Scene Editor")
#         self.scene_editor_btn.clicked.connect(self.open_scene_editor)
#         self.layout.addWidget(self.scene_editor_btn)

#         self.scene_player_btn = QPushButton("Open Scene Player")
#         self.scene_player_btn.clicked.connect(self.open_scene_player)
#         self.layout.addWidget(self.scene_player_btn)

#         self.setLayout(self.layout)

#     def open_scene_editor(self):
#         self.editor = SceneEditor(self)
#         self.editor.show()

#     def open_scene_player(self):
#         if not self.scenes:
#             from PyQt6.QtWidgets import QMessageBox
#             QMessageBox.warning(self, "No scenes", "Please add some scenes first.")
#             return
#         self.player = ScenePlayer(self.scenes)
#         self.player.show()

# def main():
#     app = QApplication(sys.argv)
#     window = MainApp()
#     window.show()
#     sys.exit(app.exec())

# if __name__ == "__main__":
#     main()



"""
WORKS just no imgs that cna be draged into the scene
"""
# import sys
# from PyQt6.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QHBoxLayout,
#     QPushButton, QTextEdit, QListWidget, QMessageBox
# )
# from PyQt6.QtGui import (
#     QPainter, QColor, QPen, QFont, QMouseEvent, QPaintEvent
# )
# from PyQt6.QtCore import Qt, QRectF, QPointF, QTimer

# class Scene:
#     def __init__(self, sentence=""):
#         self.sentence = sentence
#         self.strokes = []  # list of lists of QPointF

# class DrawingCanvas(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setMinimumSize(400, 300)
#         self.setStyleSheet("background-color: white;")
#         self.scene = None
#         self.current_stroke = []

#     def set_scene(self, scene):
#         self.scene = scene
#         self.current_stroke = []
#         self.update()

#     def mousePressEvent(self, event: QMouseEvent):
#         if not self.scene or event.button() != Qt.MouseButton.LeftButton:
#             return
#         self.current_stroke = [event.position()]
#         self.update()

#     def mouseMoveEvent(self, event: QMouseEvent):
#         if not self.scene or not (event.buttons() & Qt.MouseButton.LeftButton):
#             return
#         self.current_stroke.append(event.position())
#         self.update()

#     def mouseReleaseEvent(self, event: QMouseEvent):
#         if not self.scene or event.button() != Qt.MouseButton.LeftButton:
#             return
#         if self.current_stroke:
#             self.scene.strokes.append(self.current_stroke)
#             self.current_stroke = []
#             self.update()

#     def paintEvent(self, event: QPaintEvent):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.RenderHint.Antialiasing)
#         painter.fillRect(self.rect(), QColor(255, 255, 255))

#         if not self.scene:
#             return

#         pen = QPen(QColor(0, 0, 0), 2)
#         painter.setPen(pen)
#         # draw saved strokes
#         for stroke in self.scene.strokes:
#             for i in range(len(stroke) - 1):
#                 painter.drawLine(stroke[i], stroke[i+1])
#         # draw current stroke
#         for i in range(len(self.current_stroke) - 1):
#             painter.drawLine(self.current_stroke[i], self.current_stroke[i+1])

# class SceneEditor(QWidget):
#     def __init__(self, parent):
#         super().__init__()
#         self.parent = parent
#         self.setWindowTitle("Scene Editor")
#         self.setMinimumSize(600, 500)

#         self.layout = QVBoxLayout(self)

#         self.scene_list = QListWidget()
#         self.layout.addWidget(self.scene_list)

#         self.text_edit = QTextEdit()
#         self.text_edit.setPlaceholderText("Enter sentence for scene here...")
#         self.layout.addWidget(self.text_edit)

#         self.canvas = DrawingCanvas()
#         self.layout.addWidget(self.canvas)

#         btn_layout = QHBoxLayout()
#         self.add_btn = QPushButton("Add Scene");      self.add_btn.clicked.connect(self.add_scene)
#         self.update_btn = QPushButton("Update Scene");self.update_btn.clicked.connect(self.update_scene)
#         self.clear_btn = QPushButton("Clear Drawing");self.clear_btn.clicked.connect(self.clear_drawing)
#         self.del_btn = QPushButton("Delete Scene");   self.del_btn.clicked.connect(self.delete_scene)
#         for btn in (self.add_btn, self.update_btn, self.clear_btn, self.del_btn):
#             btn_layout.addWidget(btn)
#         self.layout.addLayout(btn_layout)

#         self.scene_list.currentRowChanged.connect(self.load_scene)
#         self.refresh_scene_list()

#     def refresh_scene_list(self):
#         self.scene_list.clear()
#         for i, scene in enumerate(self.parent.scenes):
#             text = scene.sentence or "(no sentence)"
#             display = text if len(text) < 30 else text[:27] + "..."
#             self.scene_list.addItem(f"{i+1}: {display}")
#         if self.parent.scenes:
#             self.scene_list.setCurrentRow(0)
#         else:
#             self.text_edit.clear()
#             self.canvas.set_scene(None)

#     def add_scene(self):
#         text = self.text_edit.toPlainText().strip()
#         if not text:
#             QMessageBox.warning(self, "Empty Sentence", "Please enter a sentence.")
#             return
#         new_scene = Scene(text)
#         self.parent.scenes.append(new_scene)
#         self.refresh_scene_list()

#     def update_scene(self):
#         row = self.scene_list.currentRow()
#         if row < 0:
#             QMessageBox.warning(self, "No Selection", "Select a scene first.")
#             return
#         text = self.text_edit.toPlainText().strip()
#         if not text:
#             QMessageBox.warning(self, "Empty Sentence", "Please enter a sentence.")
#             return
#         scene = self.parent.scenes[row]
#         scene.sentence = text
#         # drawing is already saved directly in scene.strokes
#         self.refresh_scene_list()

#     def clear_drawing(self):
#         row = self.scene_list.currentRow()
#         if row < 0:
#             return
#         self.parent.scenes[row].strokes = []
#         self.canvas.set_scene(self.parent.scenes[row])

#     def delete_scene(self):
#         row = self.scene_list.currentRow()
#         if row < 0:
#             return
#         del self.parent.scenes[row]
#         self.refresh_scene_list()

#     def load_scene(self, row):
#         if row < 0 or row >= len(self.parent.scenes):
#             self.text_edit.clear()
#             self.canvas.set_scene(None)
#             return
#         scene = self.parent.scenes[row]
#         self.text_edit.setText(scene.sentence)
#         self.canvas.set_scene(scene)

# class ScenePlayer(QWidget):
#     def __init__(self, scenes):
#         super().__init__()
#         self.setWindowTitle("Scene Player")
#         self.setMinimumSize(700, 500)
#         self.scenes = scenes
#         self.index = -1
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.next_scene)
#         self.playing = False
#         self.display_time = 4000

#         layout = QVBoxLayout(self)
#         btns = QHBoxLayout()
#         self.next_btn = QPushButton("Next Scene"); self.next_btn.clicked.connect(self.next_scene)
#         self.play_btn = QPushButton("Play"); self.play_btn.clicked.connect(self.toggle_play)
#         btns.addWidget(self.next_btn); btns.addWidget(self.play_btn)
#         layout.addLayout(btns)

#     def toggle_play(self):
#         if self.playing:
#             self.timer.stop(); self.play_btn.setText("Play")
#         else:
#             self.timer.start(self.display_time); self.play_btn.setText("Pause")
#         self.playing = not self.playing

#     def next_scene(self):
#         if not self.scenes:
#             return
#         self.index = (self.index + 1) % len(self.scenes)
#         self.update()

#     def paintEvent(self, event):
#         if self.index < 0 or self.index >= len(self.scenes):
#             return
#         scene = self.scenes[self.index]
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.RenderHint.Antialiasing)
#         painter.fillRect(self.rect(), QColor(255, 255, 255))

#         # draw strokes
#         painter.setPen(QPen(QColor(0, 0, 0), 3))
#         for stroke in scene.strokes:
#             for i in range(len(stroke)-1):
#                 painter.drawLine(stroke[i], stroke[i+1])

#         # draw subtitle bubble
#         w, h = self.width(), self.height()
#         bw, bh = w * 0.8, 80
#         bx, by = (w - bw)/2, h - bh - 40
#         rect = QRectF(bx, by, bw, bh)
#         painter.setBrush(QColor(255, 255, 224))
#         painter.setPen(QPen(QColor(0, 0, 0), 2))
#         painter.drawRoundedRect(rect, 15, 15)
#         tail = [
#             QPointF(rect.center().x()-10, rect.bottom()),
#             QPointF(rect.center().x()+10, rect.bottom()),
#             QPointF(rect.center().x(), rect.bottom()+15)
#         ]
#         painter.drawPolygon(*tail)
#         painter.setPen(QColor(0, 0, 0))
#         painter.setFont(QFont("Arial", 16))
#         painter.drawText(rect.adjusted(10,10,-10,-10),
#                          Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap,
#                          scene.sentence)

# class MainApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Scene Maker & Player with Drawing")
#         self.setMinimumSize(800, 600)
#         self.scenes = []
#         layout = QVBoxLayout(self)
#         btns = QHBoxLayout()
#         self.editor_btn = QPushButton("Open Scene Editor"); self.editor_btn.clicked.connect(self.open_editor)
#         self.player_btn = QPushButton("Open Scene Player"); self.player_btn.clicked.connect(self.open_player)
#         btns.addWidget(self.editor_btn); btns.addWidget(self.player_btn)
#         layout.addLayout(btns)

#     def open_editor(self):
#         self.editor = SceneEditor(self)
#         self.editor.show()

#     def open_player(self):
#         if not self.scenes:
#             QMessageBox.warning(self, "No Scenes", "Please add some scenes first.")
#             return
#         self.player = ScenePlayer(self.scenes)
#         self.player.show()

# def main():
#     app = QApplication(sys.argv)
#     window = MainApp()
#     window.show()
#     sys.exit(app.exec())

# if __name__ == "__main__":
#     main()


import sys, os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QListWidget, QMessageBox
)
from PyQt6.QtGui import (
    QPainter, QColor, QPen, QFont, QMouseEvent, QPaintEvent,
    QPixmap
)
from PyQt6.QtCore import Qt, QRectF, QPointF, QTimer

class Scene:
    def __init__(self, sentence=""):
        self.sentence = sentence
        self.strokes = []       # list of lists of QPointF
        self.images = []        # list of dicts: {'pixmap': QPixmap, 'pos': QPointF}

# class DrawingCanvas(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setMinimumSize(400, 300)
#         self.setStyleSheet("background-color: white;")
#         self.scene = None
#         self.current_stroke = []
#         self.setAcceptDrops(True)

#     def set_scene(self, scene):
#         self.scene = scene
#         self.current_stroke = []
#         self.update()

#     def mousePressEvent(self, event: QMouseEvent):
#         if not self.scene or event.button() != Qt.MouseButton.LeftButton:
#             return
#         self.current_stroke = [event.position()]
#         self.update()

#     def mouseMoveEvent(self, event: QMouseEvent):
#         if not self.scene or not (event.buttons() & Qt.MouseButton.LeftButton):
#             return
#         self.current_stroke.append(event.position())
#         self.update()

#     def mouseReleaseEvent(self, event: QMouseEvent):
#         if not self.scene or event.button() != Qt.MouseButton.LeftButton:
#             return
#         if self.current_stroke:
#             self.scene.strokes.append(self.current_stroke)
#             self.current_stroke = []
#             self.update()

#     def dragEnterEvent(self, event):
#         if event.mimeData().hasUrls():
#             event.acceptProposedAction()

#     def dropEvent(self, event):
#         if not self.scene:
#             return
#         for url in event.mimeData().urls():
#             path = url.toLocalFile()
#             if os.path.isfile(path):
#                 pix = QPixmap(path)
#                 if not pix.isNull():
#                     pos = event.position()
#                     self.scene.images.append({'pixmap': pix, 'pos': pos})
#         self.update()

#     def paintEvent(self, event: QPaintEvent):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.RenderHint.Antialiasing)
#         painter.fillRect(self.rect(), QColor(255, 255, 255))
#         if not self.scene:
#             return
#         # Draw images
#         for img in self.scene.images:
#             painter.drawPixmap(int(img['pos'].x()), int(img['pos'].y()), img['pixmap'])
#         # Draw strokes
#         painter.setPen(QPen(QColor(0, 0, 0), 2))
#         for stroke in self.scene.strokes:
#             for i in range(len(stroke) - 1):
#                 painter.drawLine(stroke[i], stroke[i+1])
#         # Draw current stroke
#         for i in range(len(self.current_stroke) - 1):
#             painter.drawLine(self.current_stroke[i], self.current_stroke[i+1])


"""
WORKS WITH SCENES and DRWAING AND DRAG AND DROP FROM GOOGLE IMGS
"""
# import sys
# import os
# import requests
# from urllib.parse import urlparse, parse_qs, unquote
# from PyQt6.QtCore import QByteArray, QPointF, Qt, QRectF, QTimer
# from PyQt6.QtGui import QImage, QPixmap, QPainter, QPen, QColor, QFont
# from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QTextEdit, QMessageBox, QApplication

# def get_direct_image_url(google_url):
#     parsed = urlparse(google_url)
#     qs = parse_qs(parsed.query)
#     if 'imgurl' in qs:
#         return unquote(qs['imgurl'][0])
#     return google_url

# # ---- New Scene class with bg_pixmap field ----
# class Scene:
#     def __init__(self, sentence):
#         self.sentence = sentence
#         self.strokes = []
#         self.images = []  # overlay images
#         self.bg_pixmap = None  # background image

# class DrawingCanvas(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setMinimumSize(400, 300)
#         self.setStyleSheet("background-color: white;")
#         self.scene = None
#         self.current_stroke = []
#         self.setAcceptDrops(True)
#         self.bg_image = None
#         self.bg_pixmap = None

#     def set_scene(self, scene):
#         self.scene = scene
#         self.current_stroke = []
#         # Update background pixmap from scene.bg_pixmap if exists
#         if scene and scene.bg_pixmap:
#             self.bg_pixmap = scene.bg_pixmap.scaled(
#                 self.size(),
#                 Qt.AspectRatioMode.KeepAspectRatioByExpanding,
#                 Qt.TransformationMode.SmoothTransformation
#             )
#         else:
#             self.bg_pixmap = None
#         self.update()

#     def mousePressEvent(self, event):
#         if not self.scene or event.button() != Qt.MouseButton.LeftButton:
#             return
#         self.current_stroke = [event.position()]
#         self.update()

#     def mouseMoveEvent(self, event):
#         if not self.scene or not (event.buttons() & Qt.MouseButton.LeftButton):
#             return
#         self.current_stroke.append(event.position())
#         self.update()

#     def mouseReleaseEvent(self, event):
#         if not self.scene or event.button() != Qt.MouseButton.LeftButton:
#             return
#         if self.current_stroke:
#             self.scene.strokes.append(self.current_stroke)
#             self.current_stroke = []
#             self.update()

#     def dragEnterEvent(self, event):
#         if event.mimeData().hasUrls() or event.mimeData().hasImage():
#             event.acceptProposedAction()
#         else:
#             event.ignore()

#     def dropEvent(self, event):
#         if not self.scene:
#             return
#         mime = event.mimeData()

#         if mime.hasImage():
#             img = mime.imageData()
#             if isinstance(img, QImage):
#                 self.set_background_image(img)
#             else:
#                 self.set_background_image(img.toImage())
#             return

#         if mime.hasUrls():
#             for url in mime.urls():
#                 url_str = url.toString()
#                 real_url = get_direct_image_url(url_str)
#                 image = None

#                 if url.isLocalFile():
#                     path = url.toLocalFile()
#                     if os.path.isfile(path):
#                         image = QImage(path)
#                 else:
#                     try:
#                         resp = requests.get(real_url)
#                         if resp.status_code == 200:
#                             image = QImage.fromData(QByteArray(resp.content))
#                     except Exception as e:
#                         print(f"Error downloading image: {e}")
#                         continue

#                 if image and not image.isNull():
#                     self.set_background_image(image)

#     # ---- Updated to save background to scene.bg_pixmap ----
#     def set_background_image(self, image: QImage):
#         self.bg_image = image
#         self.update_background_pixmap()

#         if self.scene:
#             self.scene.bg_pixmap = QPixmap.fromImage(image)

#         self.update()

#     def update_background_pixmap(self):
#         if self.bg_image:
#             self.bg_pixmap = QPixmap.fromImage(
#                 self.bg_image.scaled(
#                     self.size(),
#                     Qt.AspectRatioMode.KeepAspectRatioByExpanding,
#                     Qt.TransformationMode.SmoothTransformation
#                 )
#             )

#     def resizeEvent(self, event):
#         self.update_background_pixmap()

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.RenderHint.Antialiasing)

#         if self.bg_pixmap:
#             painter.drawPixmap(self.rect(), self.bg_pixmap)
#         else:
#             painter.fillRect(self.rect(), Qt.GlobalColor.white)

#         if not self.scene:
#             return

#         painter.setPen(QPen(Qt.GlobalColor.black, 2))
#         for stroke in self.scene.strokes:
#             for i in range(len(stroke) - 1):
#                 painter.drawLine(stroke[i], stroke[i + 1])

#         for i in range(len(self.current_stroke) - 1):
#             painter.drawLine(self.current_stroke[i], self.current_stroke[i + 1])

# class SceneEditor(QWidget):
#     def __init__(self, parent):
#         super().__init__()
#         self.parent = parent
#         self.setWindowTitle("Scene Editor")
#         self.setMinimumSize(600, 500)

#         layout = QVBoxLayout(self)
#         self.scene_list = QListWidget()
#         layout.addWidget(self.scene_list)

#         self.text_edit = QTextEdit()
#         self.text_edit.setPlaceholderText("Enter sentence for scene here…")
#         layout.addWidget(self.text_edit)

#         self.canvas = DrawingCanvas()
#         layout.addWidget(self.canvas)

#         btns = QHBoxLayout()
#         for label, handler in [
#             ("Add Scene", self.add_scene),
#             ("Update Scene", self.update_scene),
#             ("Clear Drawing", self.clear_drawing),
#             ("Delete Scene", self.delete_scene),
#         ]:
#             btn = QPushButton(label)
#             btn.clicked.connect(handler)
#             btns.addWidget(btn)
#         layout.addLayout(btns)

#         self.scene_list.currentRowChanged.connect(self.load_scene)
#         self.refresh_scene_list()

#     def refresh_scene_list(self):
#         self.scene_list.clear()
#         for i, scene in enumerate(self.parent.scenes):
#             txt = scene.sentence or "(no sentence)"
#             display = txt if len(txt) < 30 else txt[:27] + "..."
#             self.scene_list.addItem(f"{i+1}: {display}")
#         if self.parent.scenes:
#             self.scene_list.setCurrentRow(0)
#         else:
#             self.text_edit.clear()
#             self.canvas.set_scene(None)

#     def add_scene(self):
#         text = self.text_edit.toPlainText().strip()
#         if not text:
#             QMessageBox.warning(self, "Empty Sentence", "Please enter a sentence.")
#             return
#         scene = Scene(text)
#         self.parent.scenes.append(scene)
#         self.refresh_scene_list()

#     def update_scene(self):
#         row = self.scene_list.currentRow()
#         if row < 0:
#             QMessageBox.warning(self, "No Selection", "Select a scene first.")
#             return
#         text = self.text_edit.toPlainText().strip()
#         if not text:
#             QMessageBox.warning(self, "Empty Sentence", "Please enter a sentence.")
#             return
#         self.parent.scenes[row].sentence = text
#         self.refresh_scene_list()

#     def clear_drawing(self):
#         row = self.scene_list.currentRow()
#         if row < 0:
#             return
#         scene = self.parent.scenes[row]
#         scene.strokes.clear()
#         scene.images.clear()
#         scene.bg_pixmap = None
#         self.canvas.set_scene(scene)

#     def delete_scene(self):
#         row = self.scene_list.currentRow()
#         if row < 0:
#             return
#         del self.parent.scenes[row]
#         self.refresh_scene_list()

#     def load_scene(self, row):
#         if row < 0 or row >= len(self.parent.scenes):
#             self.text_edit.clear()
#             self.canvas.set_scene(None)
#             return
#         scene = self.parent.scenes[row]
#         self.text_edit.setText(scene.sentence)
#         self.canvas.set_scene(scene)

# class ScenePlayer(QWidget):
#     def __init__(self, scenes):
#         super().__init__()
#         self.setWindowTitle("Scene Player")
#         self.setMinimumSize(700, 500)
#         self.scenes = scenes
#         self.index = -1
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.next_scene)
#         self.playing = False
#         self.display_time = 4000

#         layout = QVBoxLayout(self)
#         btns = QHBoxLayout()
#         self.next_btn = QPushButton("Next Scene")
#         self.next_btn.clicked.connect(self.next_scene)
#         self.play_btn = QPushButton("Play")
#         self.play_btn.clicked.connect(self.toggle_play)
#         btns.addWidget(self.next_btn)
#         btns.addWidget(self.play_btn)
#         layout.addLayout(btns)

#     def toggle_play(self):
#         if self.playing:
#             self.timer.stop()
#             self.play_btn.setText("Play")
#         else:
#             self.timer.start(self.display_time)
#             self.play_btn.setText("Pause")
#         self.playing = not self.playing

#     def next_scene(self):
#         if not self.scenes:
#             return
#         self.index = (self.index + 1) % len(self.scenes)
#         self.update()

#     def paintEvent(self, event):
#         if self.index < 0 or self.index >= len(self.scenes):
#             return
#         scene = self.scenes[self.index]
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.RenderHint.Antialiasing)
#         painter.fillRect(self.rect(), QColor(255,255,255))
#         print("Painting canvas with", len(scene.images), "images")

#         # --- Use bg_pixmap for background ---
#         if scene.bg_pixmap:
#             painter.drawPixmap(self.rect(), scene.bg_pixmap)

#         # Draw other overlay images on top
#         painter.setPen(QPen(QColor(0,0,0), 3))
#         for img in scene.images:
#             painter.drawPixmap(int(img['pos'].x()), int(img['pos'].y()), img['pixmap'])

#         # Draw strokes
#         for stroke in scene.strokes:
#             for i in range(len(stroke)-1):
#                 painter.drawLine(stroke[i], stroke[i+1])

#         # Draw subtitle bubble
#         w, h = self.width(), self.height()
#         bw, bh = w * 0.8, 80
#         bx, by = (w - bw)/2, h - bh - 40
#         rect = QRectF(bx, by, bw, bh)
#         painter.setBrush(QColor(255,255,224))
#         painter.setPen(QPen(QColor(0,0,0),2))
#         painter.drawRoundedRect(rect, 15, 15)
#         tail = [
#             QPointF(rect.center().x()-10, rect.bottom()),
#             QPointF(rect.center().x()+10, rect.bottom()),
#             QPointF(rect.center().x(), rect.bottom()+15)
#         ]
#         painter.drawPolygon(*tail)
#         painter.setPen(QColor(0,0,0))
#         painter.setFont(QFont("Arial",16))
#         painter.drawText(rect.adjusted(10,10,-10,-10),
#                          Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap,
#                          scene.sentence)

# class MainApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Scene Maker & Player with Drawing & Images")
#         self.setMinimumSize(800, 600)
#         self.scenes = []
#         layout = QVBoxLayout(self)
#         btns = QHBoxLayout()
#         self.editor_btn = QPushButton("Open Scene Editor")
#         self.editor_btn.clicked.connect(self.open_editor)
#         self.player_btn = QPushButton("Open Scene Player")
#         self.player_btn.clicked.connect(self.open_player)
#         btns.addWidget(self.editor_btn)
#         btns.addWidget(self.player_btn)
#         layout.addLayout(btns)

#     def open_editor(self):
#         self.editor = SceneEditor(self)
#         self.editor.show()

#     def open_player(self):
#         if not self.scenes:
#             QMessageBox.warning(self, "No Scenes", "Please add some scenes first.")
#             return
#         self.player = ScenePlayer(self.scenes)
#         self.player.show()

# def main():
#     app = QApplication(sys.argv)
#     window = MainApp()
#     window.show()
#     sys.exit(app.exec())

# if __name__ == "__main__":
#     main()

import sys
import os
import requests
from urllib.parse import urlparse, parse_qs, unquote
from PyQt6.QtCore import QByteArray, QPointF, Qt, QRectF, QTimer
from PyQt6.QtGui import QImage, QPixmap, QPainter, QPen, QColor, QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget,
    QTextEdit, QMessageBox, QApplication, QSlider, QLabel
)

def get_direct_image_url(google_url):
    parsed = urlparse(google_url)
    qs = parse_qs(parsed.query)
    if 'imgurl' in qs:
        return unquote(qs['imgurl'][0])
    return google_url

class Scene:
    def __init__(self, sentence):
        self.sentence = sentence
        self.strokes = []  # list of (points, pen)
        self.images = []  # overlay images
        self.bg_pixmap = None  # background image

class DrawingCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 300)
        self.setStyleSheet("background-color: white;")
        self.scene = None
        self.current_stroke = []
        self.setAcceptDrops(True)
        self.bg_image = None
        self.bg_pixmap = None
        self.stroke_color = QColor('black')
        self.stroke_width = 2

    def set_scene(self, scene):
        self.scene = scene
        self.current_stroke = []
        if scene and scene.bg_pixmap:
            self.bg_pixmap = scene.bg_pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
        else:
            self.bg_pixmap = None
        self.update()

    def mousePressEvent(self, event):
        if not self.scene or event.button() != Qt.MouseButton.LeftButton:
            return
        self.current_stroke = [event.position()]
        self.update()

    def mouseMoveEvent(self, event):
        if not self.scene or not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        self.current_stroke.append(event.position())
        self.update()

    def mouseReleaseEvent(self, event):
        if not self.scene or event.button() != Qt.MouseButton.LeftButton:
            return
        if self.current_stroke:
            pen = QPen(self.stroke_color, self.stroke_width)
            self.scene.strokes.append((self.current_stroke, pen))
            self.current_stroke = []
            self.update()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() or event.mimeData().hasImage():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if not self.scene:
            return
        mime = event.mimeData()

        if mime.hasImage():
            img = mime.imageData()
            if isinstance(img, QImage):
                self.set_background_image(img)
            else:
                self.set_background_image(img.toImage())
            return

        if mime.hasUrls():
            for url in mime.urls():
                url_str = url.toString()
                real_url = get_direct_image_url(url_str)
                image = None

                if url.isLocalFile():
                    path = url.toLocalFile()
                    if os.path.isfile(path):
                        image = QImage(path)
                else:
                    try:
                        resp = requests.get(real_url)
                        if resp.status_code == 200:
                            image = QImage.fromData(QByteArray(resp.content))
                    except Exception as e:
                        print(f"Error downloading image: {e}")
                        continue

                if image and not image.isNull():
                    self.set_background_image(image)

    def set_background_image(self, image: QImage):
        self.bg_image = image
        self.update_background_pixmap()

        if self.scene:
            self.scene.bg_pixmap = QPixmap.fromImage(image)

        self.update()

    def update_background_pixmap(self):
        if self.bg_image:
            self.bg_pixmap = QPixmap.fromImage(
                self.bg_image.scaled(
                    self.size(),
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation
                )
            )

    def resizeEvent(self, event):
        self.update_background_pixmap()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.bg_pixmap:
            painter.drawPixmap(self.rect(), self.bg_pixmap)
        else:
            painter.fillRect(self.rect(), Qt.GlobalColor.white)

        if not self.scene:
            return

        for stroke, pen in self.scene.strokes:
            painter.setPen(pen)
            for i in range(len(stroke) - 1):
                painter.drawLine(stroke[i], stroke[i + 1])

        painter.setPen(QPen(self.stroke_color, self.stroke_width))
        for i in range(len(self.current_stroke) - 1):
            painter.drawLine(self.current_stroke[i], self.current_stroke[i + 1])

class SceneEditor(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Scene Editor")
        self.setMinimumSize(700, 500)

        main_layout = QHBoxLayout(self)

        editor_layout = QVBoxLayout()
        self.scene_list = QListWidget()
        editor_layout.addWidget(self.scene_list)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Enter sentence for scene here…")
        editor_layout.addWidget(self.text_edit)

        self.canvas = DrawingCanvas()
        editor_layout.addWidget(self.canvas)

        btns = QHBoxLayout()
        for label, handler in [
            ("Add Scene", self.add_scene),
            ("Update Scene", self.update_scene),
            ("Clear Drawing", self.clear_drawing),
            ("Delete Scene", self.delete_scene),
        ]:
            btn = QPushButton(label)
            btn.clicked.connect(handler)
            btns.addWidget(btn)
        editor_layout.addLayout(btns)

        main_layout.addLayout(editor_layout, stretch=4)

        side_panel = QVBoxLayout()
        side_panel.addWidget(QLabel("Stroke Color:"))

        colors = ['black', 'red', 'green', 'blue', 'orange']
        for c in colors:
            btn = QPushButton()
            btn.setFixedSize(30, 30)
            btn.setStyleSheet(f"background-color: {c};")
            btn.clicked.connect(lambda checked, col=c: self.set_stroke_color(col))
            side_panel.addWidget(btn)

        side_panel.addSpacing(20)
        side_panel.addWidget(QLabel("Stroke Size:"))
        self.size_slider = QSlider(Qt.Orientation.Vertical)
        self.size_slider.setMinimum(1)
        self.size_slider.setMaximum(10)
        self.size_slider.setValue(self.canvas.stroke_width)
        self.size_slider.valueChanged.connect(self.set_stroke_width)
        side_panel.addWidget(self.size_slider)

        main_layout.addLayout(side_panel, stretch=1)

        self.scene_list.currentRowChanged.connect(self.load_scene)
        self.refresh_scene_list()

    def set_stroke_color(self, color_name):
        self.canvas.stroke_color = QColor(color_name)
        self.canvas.update()

    def set_stroke_width(self, val):
        self.canvas.stroke_width = val
        self.canvas.update()

    def refresh_scene_list(self):
        self.scene_list.clear()
        for i, scene in enumerate(self.parent.scenes):
            txt = scene.sentence or "(no sentence)"
            display = txt if len(txt) < 30 else txt[:27] + "..."
            self.scene_list.addItem(f"{i+1}: {display}")
        if self.parent.scenes:
            self.scene_list.setCurrentRow(0)
        else:
            self.text_edit.clear()
            self.canvas.set_scene(None)

    def add_scene(self):
        text = self.text_edit.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Empty Sentence", "Please enter a sentence.")
            return
        scene = Scene(text)
        self.parent.scenes.append(scene)
        self.refresh_scene_list()

    def update_scene(self):
        row = self.scene_list.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Select a scene first.")
            return
        text = self.text_edit.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Empty Sentence", "Please enter a sentence.")
            return
        self.parent.scenes[row].sentence = text
        self.refresh_scene_list()

    def clear_drawing(self):
        row = self.scene_list.currentRow()
        if row < 0:
            return
        scene = self.parent.scenes[row]
        scene.strokes.clear()
        scene.images.clear()
        scene.bg_pixmap = None
        self.canvas.set_scene(scene)

    def delete_scene(self):
        row = self.scene_list.currentRow()
        if row < 0:
            return
        del self.parent.scenes[row]
        self.refresh_scene_list()

    def load_scene(self, row):
        if row < 0 or row >= len(self.parent.scenes):
            self.text_edit.clear()
            self.canvas.set_scene(None)
            return
        scene = self.parent.scenes[row]
        self.text_edit.setText(scene.sentence)
        self.canvas.set_scene(scene)

class ScenePlayer(QWidget):
    def __init__(self, scenes):
        super().__init__()
        self.setWindowTitle("Scene Player")
        self.setMinimumSize(700, 500)
        self.scenes = scenes
        self.index = -1
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_scene)
        self.playing = False
        self.display_time = 4000

        layout = QVBoxLayout(self)
        btns = QHBoxLayout()
        self.next_btn = QPushButton("Next Scene")
        self.next_btn.clicked.connect(self.next_scene)
        self.play_btn = QPushButton("Play")
        self.play_btn.clicked.connect(self.toggle_play)
        btns.addWidget(self.next_btn)
        btns.addWidget(self.play_btn)
        layout.addLayout(btns)

    def toggle_play(self):
        if self.playing:
            self.timer.stop()
            self.play_btn.setText("Play")
        else:
            self.timer.start(self.display_time)
            self.play_btn.setText("Pause")
        self.playing = not self.playing

    def next_scene(self):
        if not self.scenes:
            return
        self.index = (self.index + 1) % len(self.scenes)
        self.update()

    def paintEvent(self, event):
        if self.index < 0 or self.index >= len(self.scenes):
            return
        scene = self.scenes[self.index]
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(255,255,255))

        if scene.bg_pixmap:
            painter.drawPixmap(self.rect(), scene.bg_pixmap)

        painter.setPen(QPen(QColor(0,0,0), 3))
        for img in scene.images:
            painter.drawPixmap(int(img['pos'].x()), int(img['pos'].y()), img['pixmap'])

        for stroke, pen in scene.strokes:
            painter.setPen(pen)
            for i in range(len(stroke)-1):
                painter.drawLine(stroke[i], stroke[i+1])

        w, h = self.width(), self.height()
        bw, bh = w * 0.8, 80
        bx, by = (w - bw)/2, h - bh - 40
        rect = QRectF(bx, by, bw, bh)
        painter.setBrush(QColor(255,255,224))
        painter.setPen(QPen(QColor(0,0,0),2))
        painter.drawRoundedRect(rect, 15, 15)
        tail = [
            QPointF(rect.center().x()-10, rect.bottom()),
            QPointF(rect.center().x()+10, rect.bottom()),
            QPointF(rect.center().x(), rect.bottom()+15)
        ]
        painter.drawPolygon(*tail)
        painter.setPen(QColor(0,0,0))
        painter.setFont(QFont("Arial",16))
        painter.drawText(rect.adjusted(10,10,-10,-10),
                         Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap,
                         scene.sentence)

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scene Maker & Player with Drawing & Images")
        self.setMinimumSize(800, 600)
        self.scenes = []
        layout = QVBoxLayout(self)
        btns = QHBoxLayout()
        self.editor_btn = QPushButton("Open Scene Editor")
        self.editor_btn.clicked.connect(self.open_editor)
        self.player_btn = QPushButton("Open Scene Player")
        self.player_btn.clicked.connect(self.open_player)
        btns.addWidget(self.editor_btn)
        btns.addWidget(self.player_btn)
        layout.addLayout(btns)

    def open_editor(self):
        self.editor = SceneEditor(self)
        self.editor.show()

    def open_player(self):
        if not self.scenes:
            QMessageBox.warning(self, "No Scenes", "Please add some scenes first.")
            return
        self.player = ScenePlayer(self.scenes)
        self.player.show()

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
