"""
pyqt6 - v. 6.7 (G) || 6.9 (G)
pyqt6-webengine - v. 6.7 (G)
"""
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtPrintSupport import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtWebEngineCore import *
import sys
import os

# os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--use-gl=angle --gpu --gpu-launcher --in-process-gpu --ignore-gpu-blacklist --ignore-gpu-blocklist'

# Add the root directory of your project to the sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.core.Connect.AppConnector import *


import importlib
import os

def load_apps():
    base_path = "src.apps"
    app_dir = os.path.join(os.path.dirname(__file__), "src", "apps")
    pages = []

    for name in os.listdir(app_dir):
        app_path = os.path.join(app_dir, name)
        if not os.path.isdir(app_path):
            continue
        if name.startswith("__") or name.lower() == "widgets":
            continue

        try:
            layout_mod = importlib.import_module(f"{base_path}.{name}.Layout")
            logic_mod = importlib.import_module(f"{base_path}.{name}.Functions")
            conn_mod = importlib.import_module(f"{base_path}.{name}.Connections")
        except ModuleNotFoundError as e:
            print(f"[WARNING] Missing module for {name}: {e}")
            continue

        try:
            layout_cls = getattr(layout_mod, "Layout")
            logic_cls = getattr(logic_mod, "Logic")
            conn_cls = getattr(conn_mod, "Connections")
        except AttributeError as e:
            print(f"[WARNING] Missing class for {name}: {e}")
            continue

        pages.append((name, layout_cls, logic_cls, conn_cls))

    if not pages:
        print("[ERROR] No valid apps found in src/apps")

    return pages


class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UI")
        self.resize(800, 480)
        self.setup_stylesheets()

        self.stack = QStackedWidget()

        # Your dynamic page creation
        # Define pages with: name, UI class, Logic class, Controller class
        pages = load_apps()

        # Step 1: Create UIs
        self.apps = {name: layout_class() for name, layout_class, _, _ in pages}

        # Step 2: Create Logic
        self.logic = {name: logic_class(self.apps[name]) for name, _, logic_class, _ in pages}

        # Step 3: Create Per-Page Controllers
        self.page_controllers = {
            name: controller_class(self.apps[name], self.logic[name])
            for name, _, _, controller_class in pages
        }

        # Add pages to the stack
        for page in self.apps.values():
            self.stack.addWidget(page)

        # Create the controller
        self.controller = AppConnector(self.apps, self.logic)


        menubar = QMenuBar(self)
        app_menu = menubar.addMenu("Apps")

        for name in self.apps:
            action = QAction(name.capitalize(), self)
            action.triggered.connect(lambda _, n=name: self.switch_to(n))
            app_menu.addAction(action)

        self.setMenuBar(menubar)

        # Main container setup
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(self.stack)
        self.setCentralWidget(container)

        self.switch_to("SentenceChunks")

    def switch_to(self, app_name):
        try:
            self.stack.setCurrentWidget(self.apps[app_name])
        except KeyError:
            print(f"Invalid app name: {app_name}")
            print("Valid app names are:", list(self.apps.keys()))


    def setup_stylesheets(self):
        # Yu Gothic UI
        """
            QMainWindow {
                background-color: #1a0d1c;
            }
            QLabel {
                background-color: #AAAAAA;
            }
        """
        self.setStyleSheet("""
            QWidget {
                font-family: "Meiryo";
                color: #FFFFFF;
                background-color: #222222;
            }

            QLineEdit, QListWidget {
                font-size: 16pt;
                selection-background-color: #5555aa;
                selection-color: #ffffff;
                background-color: #222222;
            }

            QListWidget::item:selected {
                background-color: #5555aa;
                color: white;
            }
            
            QLineEdit:focus, QListWidget:focus {
                border: 1px solid #88C;
            }

        """)


# ----- Entry Point -----
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Dashboard()
    win.show()
    sys.exit(app.exec())
