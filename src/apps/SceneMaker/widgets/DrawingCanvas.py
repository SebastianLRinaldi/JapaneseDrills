from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *

import sys
import os
import requests
from urllib.parse import urlparse, parse_qs, unquote


from src.core.GUI.UiManager import *

"""
Something to Override a Known widgte
"""
# class ChunkHolder(QListWidget):

#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Chunk Holder")


"""
If you just need another window with complexlayout in the app
"""
# class ChunkInput(UiManager):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Media Controls")

def get_direct_image_url(google_url):
    parsed = urlparse(google_url)
    qs = parse_qs(parsed.query)
    if 'imgurl' in qs:
        return unquote(qs['imgurl'][0])
    return google_url



class DrawingCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 300)
        self.setStyleSheet("background-color: white;")
        self.scene = None
        self.current_stroke = []  # normalized points QPointF(x/w, y/h)
        self.setAcceptDrops(True)
        self.bg_image = None
        self.bg_pixmap = None
        self.stroke_color = QColor('black')
        self.stroke_width = 2
        self._base_size = self.size()  # store initial size for scaling stroke width if needed

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
        pos = event.position()
        norm_pos = QPointF(pos.x() / self.width(), pos.y() / self.height())
        self.current_stroke = [norm_pos]
        self.update()

    def mouseMoveEvent(self, event):
        if not self.scene or not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        pos = event.position()
        norm_pos = QPointF(pos.x() / self.width(), pos.y() / self.height())
        self.current_stroke.append(norm_pos)
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
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.bg_pixmap:
            painter.drawPixmap(self.rect(), self.bg_pixmap)
        else:
            painter.fillRect(self.rect(), Qt.GlobalColor.white)

        if not self.scene:
            return

        w, h = self.width(), self.height()

        for stroke, pen in self.scene.strokes:
            painter.setPen(pen)
            for i in range(len(stroke) - 1):
                p1 = QPointF(stroke[i].x() * w, stroke[i].y() * h)
                p2 = QPointF(stroke[i + 1].x() * w, stroke[i + 1].y() * h)
                painter.drawLine(p1, p2)

        # Draw current stroke being drawn with current color/width
        painter.setPen(QPen(self.stroke_color, self.stroke_width))
        for i in range(len(self.current_stroke) - 1):
            p1 = QPointF(self.current_stroke[i].x() * w, self.current_stroke[i].y() * h)
            p2 = QPointF(self.current_stroke[i + 1].x() * w, self.current_stroke[i + 1].y() * h)
            painter.drawLine(p1, p2)
