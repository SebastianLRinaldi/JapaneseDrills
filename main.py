"""
pyqt6 - v. 6.7 (G) || 6.9 (G)
pyqt6-webengine - v. 6.7 (G)
PyQt6-WebEngine==6.7
"""
from PyQt6.QtWidgets import *

import sys
import os

from src.home import Component as Home
# ----- Entry Point -----
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Home()
    win.showMaximized()  
    sys.exit(app.exec())
