from PyQt6.QtCore import QObject, pyqtSignal, QEvent
from PyQt6.QtGui import QInputMethodEvent

class IMEHandler(QObject):
    imeEventReceived = pyqtSignal(QInputMethodEvent)

    def __init__(self, parent=None):
        super().__init__(parent)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.InputMethod:
            if isinstance(event, QInputMethodEvent):
                self.imeEventReceived.emit(event)
                # Don't return True unless you want to block the widget from handling the input
        return False