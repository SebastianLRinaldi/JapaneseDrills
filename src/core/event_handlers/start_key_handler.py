from PyQt6.QtCore import pyqtSignal, Qt, QEvent, QObject

class StartKeyHandler(QObject):
    startPressed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def eventFilter(self, obj, event):
        if (event.type() == QEvent.Type.KeyPress 
                and event.key() == Qt.Key.Key_S 
                and event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            self.startPressed.emit()
            return True
        return False