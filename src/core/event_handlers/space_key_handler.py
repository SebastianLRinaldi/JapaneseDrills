from PyQt6.QtCore import QObject, pyqtSignal, QEvent, Qt

class SpaceKeyHandler(QObject):
    spacePressed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Space:
            self.spacePressed.emit()
        return False