from PyQt6.QtCore import pyqtSignal, Qt, QEvent, QObject

class UndoKeyHandler(QObject):
    undoPressed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def eventFilter(self, obj, event):
        if (event.type() == QEvent.Type.KeyPress 
                and event.key() == Qt.Key.Key_Z 
                and event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            self.undoPressed.emit()
            return True
        return False