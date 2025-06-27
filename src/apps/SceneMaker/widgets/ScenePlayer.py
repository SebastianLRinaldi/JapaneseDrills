from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

class ScenePlayer(QWidget):
    def __init__(self, scenes):
        super().__init__()
        self.setWindowTitle("Scene Player")
        self.setMinimumSize(400, 300)
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

        w, h = self.width(), self.height()
        for stroke, pen in scene.strokes:
            painter.setPen(pen)
            for i in range(len(stroke) - 1):
                p1 = QPointF(stroke[i].x() * w, stroke[i].y() * h)
                p2 = QPointF(stroke[i + 1].x() * w, stroke[i + 1].y() * h)
                painter.drawLine(p1, p2)

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