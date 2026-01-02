from PyQt6.QtCore import QObject, pyqtSignal

class GlobalSignalManager(QObject):
    # card_selected = pyqtSignal(object)
    # request_refresh = pyqtSignal()
    # gas_flow_changed = pyqtSignal(int, float)
    kana_timer_started = pyqtSignal()
    kana_timer_stopped = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._log(self.kana_timer_started, "kana timer_started")
        self._log(self.kana_timer_stopped, "kana timer_stopped")

    def _log(self, signal, name: str):
        signal.connect(
            lambda *args: print(f"[SignalManager] {name}", *args)
        )

global_signal_manager = GlobalSignalManager()
