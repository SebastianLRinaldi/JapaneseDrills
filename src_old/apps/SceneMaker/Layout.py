from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src_old.core.GUI.UiManager import *

# from .widgets.CUSTOMWIDGET import YOURWIDGET

from .widgets.DrawingCanvas import DrawingCanvas

from src_old.core.GUI.UiManager import UiManager
import sys
import os
import requests
from urllib.parse import urlparse, parse_qs, unquote


class Layout(UiManager):

    scene_list: QListWidget
    text_edit: QTextEdit
    canvas: DrawingCanvas
    add_btn: QPushButton
    update_btn: QPushButton
    clear_btn: QPushButton
    delete_btn: QPushButton
    stroke_color_label: QLabel
    stroke_buttons: list
    stroke_size_label: QLabel
    size_slider: QSlider
    open_player_btn: QPushButton
    
    black: QPushButton
    red: QPushButton
    green: QPushButton
    blue: QPushButton
    orange: QPushButton
    

    
    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.setup_stylesheets()
        self.set_widgets()

        layout_data = [

            self.group("horizontal",[

                self.group("vertical", ["scene_list", "text_edit", "canvas",

                    self.group("horizontal",["add_btn","clear_btn", "delete_btn", "open_player_btn"])
                                        ]),
                self.group("vertical",["stroke_color_label", *self.color_names,
                                                            # "black", 
                                                            # "red",
                                                            # "green",
                                                            # "blue",
                                                            # "orange",
                                                            "stroke_size_label", 
                                                            "size_slider"]),
                
            ]),
        ]
        
        self.apply_layout(layout_data)

    def init_widgets(self):
        annotations = getattr(self.__class__, "__annotations__", {})
        for name, widget_type in annotations.items():
            widget = widget_type()
            setattr(self, name, widget)
            
    def setup_stylesheets(self):
        self.setStyleSheet(""" 
            QListWidget { font-size: 14px; }
            QTextEdit { font-size: 14px; }
            QPushButton { min-width: 90px; min-height: 30px; }
            QLabel { font-weight: bold; }
        """)

    def set_widgets(self):
        self.text_edit.setPlaceholderText("Enter sentence for scene here…")
        self.canvas.stroke_color = QColor('black')
        self.canvas.stroke_width = 2

        self.add_btn.setText("Add Scene")
        self.update_btn.setText("Update Scene")
        self.clear_btn.setText("Clear Drawing")
        self.delete_btn.setText("Delete Scene")
        self.open_player_btn.setText("Open Scene Player")

        self.stroke_color_label.setText("Stroke Color:")
        self.stroke_size_label.setText("Stroke Size:")

        
        self.color_names = ["black", "red", "green", "blue", "orange"]

        
        for color in self.color_names:
            btn = getattr(self, color, None)
            if isinstance(btn, QPushButton):
                btn.setFixedSize(30, 30)
                btn.setStyleSheet(f"background-color: {color};")

        self.size_slider.setOrientation(Qt.Orientation.Vertical)
        self.size_slider.setMinimum(1)
        self.size_slider.setMaximum(10)
        self.size_slider.setValue(self.canvas.stroke_width)
        

        # self.refresh_scene_list()



# def get_direct_image_url(google_url):
#     parsed = urlparse(google_url)
#     qs = parse_qs(parsed.query)
#     if 'imgurl' in qs:
#         return unquote(qs['imgurl'][0])
#     return google_url

# class Scene:
#     def __init__(self, sentence):
#         self.sentence = sentence
#         self.strokes = []  # list of (points: List[QPointF], pen: QPen)
#         self.images = []   # unused here but placeholder
#         self.bg_pixmap = None

# class ScenePlayer(QWidget):
#     def __init__(self, scenes):
#         super().__init__()
#         self.setWindowTitle("Scene Player")
#         self.setMinimumSize(400, 300)
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

#         if scene.bg_pixmap:
#             painter.drawPixmap(self.rect(), scene.bg_pixmap)

#         painter.setPen(QPen(QColor(0,0,0), 3))
#         for img in scene.images:
#             painter.drawPixmap(int(img['pos'].x()), int(img['pos'].y()), img['pixmap'])

#         w, h = self.width(), self.height()
#         for stroke, pen in scene.strokes:
#             painter.setPen(pen)
#             for i in range(len(stroke) - 1):
#                 p1 = QPointF(stroke[i].x() * w, stroke[i].y() * h)
#                 p2 = QPointF(stroke[i + 1].x() * w, stroke[i + 1].y() * h)
#                 painter.drawLine(p1, p2)

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


# class DrawingCanvas(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setMinimumSize(400, 300)
#         self.setStyleSheet("background-color: white;")
#         self.scene = None
#         self.current_stroke = []  # normalized points QPointF(x/w, y/h)
#         self.setAcceptDrops(True)
#         self.bg_image = None
#         self.bg_pixmap = None
#         self.stroke_color = QColor('black')
#         self.stroke_width = 2
#         self._base_size = self.size()  # store initial size for scaling stroke width if needed

#     def set_scene(self, scene):
#         self.scene = scene
#         self.current_stroke = []
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
#         pos = event.position()
#         norm_pos = QPointF(pos.x() / self.width(), pos.y() / self.height())
#         self.current_stroke = [norm_pos]
#         self.update()

#     def mouseMoveEvent(self, event):
#         if not self.scene or not (event.buttons() & Qt.MouseButton.LeftButton):
#             return
#         pos = event.position()
#         norm_pos = QPointF(pos.x() / self.width(), pos.y() / self.height())
#         self.current_stroke.append(norm_pos)
#         self.update()

#     def mouseReleaseEvent(self, event):
#         if not self.scene or event.button() != Qt.MouseButton.LeftButton:
#             return
#         if self.current_stroke:
#             pen = QPen(self.stroke_color, self.stroke_width)
#             self.scene.strokes.append((self.current_stroke, pen))
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
#         self.update()

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.RenderHint.Antialiasing)

#         if self.bg_pixmap:
#             painter.drawPixmap(self.rect(), self.bg_pixmap)
#         else:
#             painter.fillRect(self.rect(), Qt.GlobalColor.white)

#         if not self.scene:
#             return

#         w, h = self.width(), self.height()

#         for stroke, pen in self.scene.strokes:
#             painter.setPen(pen)
#             for i in range(len(stroke) - 1):
#                 p1 = QPointF(stroke[i].x() * w, stroke[i].y() * h)
#                 p2 = QPointF(stroke[i + 1].x() * w, stroke[i + 1].y() * h)
#                 painter.drawLine(p1, p2)

#         # Draw current stroke being drawn with current color/width
#         painter.setPen(QPen(self.stroke_color, self.stroke_width))
#         for i in range(len(self.current_stroke) - 1):
#             p1 = QPointF(self.current_stroke[i].x() * w, self.current_stroke[i].y() * h)
#             p2 = QPointF(self.current_stroke[i + 1].x() * w, self.current_stroke[i + 1].y() * h)
#             painter.drawLine(p1, p2)


# class Layout(UiManager):
#     scene_list: QListWidget
#     text_edit: QTextEdit
#     canvas: DrawingCanvas
#     add_btn: QPushButton
#     update_btn: QPushButton
#     clear_btn: QPushButton
#     delete_btn: QPushButton
#     stroke_color_label: QLabel
#     stroke_buttons: list
#     stroke_size_label: QLabel
#     size_slider: QSlider
#     open_player_btn: QPushButton

#     def __init__(self):
#         super().__init__()
#         self.scenes = []
#         self.init_widgets()
#         self.setup_stylesheets()
#         self.set_widgets()
#         self.setup_layout()

#     def init_widgets(self):
#         annotations = getattr(self.__class__, "__annotations__", {})
#         for name, widget_type in annotations.items():
#             if name == "stroke_buttons":
#                 setattr(self, name, [])
#                 continue
#             setattr(self, name, widget_type())

#     def setup_stylesheets(self):
#         self.setStyleSheet(""" 
#             QListWidget { font-size: 14px; }
#             QTextEdit { font-size: 14px; }
#             QPushButton { min-width: 90px; min-height: 30px; }
#             QLabel { font-weight: bold; }
#         """)

#     def set_widgets(self):
#         self.text_edit.setPlaceholderText("Enter sentence for scene here…")
#         self.canvas.stroke_color = QColor('black')
#         self.canvas.stroke_width = 2

#         self.add_btn.setText("Add Scene")
#         self.update_btn.setText("Update Scene")
#         self.clear_btn.setText("Clear Drawing")
#         self.delete_btn.setText("Delete Scene")
#         self.open_player_btn.setText("Open Scene Player")

#         self.stroke_color_label.setText("Stroke Color:")
#         self.stroke_size_label.setText("Stroke Size:")

#         self.add_btn.clicked.connect(self.add_scene)
#         self.update_btn.clicked.connect(self.update_scene)
#         self.clear_btn.clicked.connect(self.clear_drawing)
#         self.delete_btn.clicked.connect(self.delete_scene)
#         self.open_player_btn.clicked.connect(self.open_player)

#         self.scene_list.currentRowChanged.connect(self.load_scene)

#         colors = ['black', 'red', 'green', 'blue', 'orange']
#         for color in colors:
#             btn = QPushButton()
#             btn.setFixedSize(30, 30)
#             btn.setStyleSheet(f"background-color: {color};")
#             btn.clicked.connect(lambda checked, c=color: self.set_stroke_color(c))
#             self.stroke_buttons.append(btn)

#         self.size_slider.setOrientation(Qt.Orientation.Vertical)
#         self.size_slider.setMinimum(1)
#         self.size_slider.setMaximum(10)
#         self.size_slider.setValue(self.canvas.stroke_width)
#         self.size_slider.valueChanged.connect(self.set_stroke_width)

#         self.refresh_scene_list()

#     def setup_layout(self):
#         main_layout = QHBoxLayout(self)

#         left_layout = QVBoxLayout()
#         left_layout.addWidget(self.scene_list)
#         left_layout.addWidget(self.text_edit)
#         left_layout.addWidget(self.canvas)

#         btn_layout = QHBoxLayout()
#         for btn in [self.add_btn, self.update_btn, self.clear_btn, self.delete_btn, self.open_player_btn]:
#             btn_layout.addWidget(btn)
#         left_layout.addLayout(btn_layout)

#         main_layout.addLayout(left_layout, stretch=4)

#         right_layout = QVBoxLayout()
#         right_layout.addWidget(self.stroke_color_label)
#         for btn in self.stroke_buttons:
#             right_layout.addWidget(btn)
#         right_layout.addSpacing(20)
#         right_layout.addWidget(self.stroke_size_label)
#         right_layout.addWidget(self.size_slider)

#         main_layout.addLayout(right_layout, stretch=1)

#         self.setLayout(main_layout)

#     def set_stroke_color(self, color_name):
#         self.canvas.stroke_color = QColor(color_name)
#         self.canvas.update()

#     def set_stroke_width(self, val):
#         self.canvas.stroke_width = val
#         self.canvas.update()

#     def refresh_scene_list(self):
#         self.scene_list.clear()
#         for i, scene in enumerate(self.scenes):
#             txt = scene.sentence or "(no sentence)"
#             display = txt if len(txt) < 30 else txt[:27] + "..."
#             self.scene_list.addItem(f"{i+1}: {display}")
#         if self.scenes:
#             self.scene_list.setCurrentRow(0)
#         else:
#             self.text_edit.clear()
#             self.canvas.set_scene(None)

#     def add_scene(self):
#         text = self.text_edit.toPlainText().strip()
#         if not text:
#             QMessageBox.warning(self, "Empty Sentence", "Please enter a sentence.")
#             return
#         self.scenes.append(Scene(text))
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
#         self.scenes[row].sentence = text
#         self.refresh_scene_list()

#     def clear_drawing(self):
#         row = self.scene_list.currentRow()
#         if row < 0:
#             return
#         scene = self.scenes[row]
#         scene.strokes.clear()
#         scene.images.clear()
#         scene.bg_pixmap = None
#         self.canvas.set_scene(scene)

#     def delete_scene(self):
#         row = self.scene_list.currentRow()
#         if row < 0:
#             return
#         del self.scenes[row]
#         self.refresh_scene_list()

#     def load_scene(self, row):
#         if row < 0 or row >= len(self.scenes):
#             self.text_edit.clear()
#             self.canvas.set_scene(None)
#             return
#         scene = self.scenes[row]
#         self.text_edit.setText(scene.sentence)
#         self.canvas.set_scene(scene)

#     def open_player(self):
#         if not self.scenes:
#             QMessageBox.warning(self, "No Scenes", "Please add some scenes first.")
#             return
#         self.player = ScenePlayer(self.scenes)
#         self.player.show()




