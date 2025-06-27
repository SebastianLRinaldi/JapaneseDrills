import sys
import os
import requests
from urllib.parse import urlparse, parse_qs, unquote
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QPixmap, QImage, QPaintEvent
from PyQt6.QtCore import Qt, QByteArray, QPointF

def get_direct_image_url(google_url):
    parsed = urlparse(google_url)
    qs = parse_qs(parsed.query)
    if 'imgurl' in qs:
        return unquote(qs['imgurl'][0])
    return google_url  # fallback

class DrawingCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag & Drop Image Canvas")
        self.setMinimumSize(600, 400)
        self.setAcceptDrops(True)
        self.images = []

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() or event.mimeData().hasImage():
            print("Drag enter with data")
            event.acceptProposedAction()
        else:
            print("Drag enter rejected")
            event.ignore()

    def dropEvent(self, event):
        mime = event.mimeData()

        if mime.hasImage():
            print("Dropped raw image data")
            img = mime.imageData()
            pix = QPixmap.fromImage(img)
            # Scale to canvas size, keep aspect ratio by expanding to fill
            pix = pix.scaled(self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)
            # Position at top-left corner
            x, y = 0, 0
            self.images.append({'pixmap': pix, 'pos': QPointF(x, y)})
            self.update()
            return

        if mime.hasUrls():
            for url in mime.urls():
                url_str = url.toString()
                print(f"Dropped URL: {url_str}")
                real_url = get_direct_image_url(url_str)
                print(f"Real image URL extracted: {real_url}")

                if url.isLocalFile():
                    path = url.toLocalFile()
                    print(f"Local file path: {path}")
                    if os.path.isfile(path):
                        pix = QPixmap(path)
                    else:
                        print("Local file not found")
                        continue
                else:
                    try:
                        resp = requests.get(real_url)
                        if resp.status_code == 200:
                            image_data = resp.content
                            image = QImage.fromData(QByteArray(image_data))
                            if not image.isNull():
                                pix = QPixmap.fromImage(image)
                            else:
                                print("Downloaded data is not a valid image")
                                continue
                        else:
                            print(f"Failed to download image: {resp.status_code}")
                            continue
                    except Exception as e:
                        print(f"Exception downloading image: {e}")
                        continue

                # Scale image to fill the whole canvas (ignore aspect ratio)
                pix = pix.scaled(self.width(), self.height(), Qt.AspectRatioMode.IgnoreAspectRatio)
                x, y = 0, 0
                self.images.append({'pixmap': pix, 'pos': QPointF(x, y)})

            self.update()

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.GlobalColor.white)
        print("Painting canvas with", len(self.images), "images")
        for img in self.images:
            pos = img['pos']
            pix = img['pixmap']
            painter.drawPixmap(int(pos.x()), int(pos.y()), pix)

def main():
    app = QApplication(sys.argv)
    w = DrawingCanvas()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
