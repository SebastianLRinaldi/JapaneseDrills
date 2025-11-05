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

from src_old.core.Connect.AppConnector import *


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


# class Dashboard(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("UI")
#         self.resize(800, 480)
#         self.setup_stylesheets()

#         self.stack = QStackedWidget()

#         # Your dynamic page creation
#         # Define pages with: name, UI class, Logic class, Controller class
#         pages = load_apps()

#         # Step 1: Create UIs
#         self.apps = {name: layout_class() for name, layout_class, _, _ in pages}

#         # Step 2: Create Logic
#         self.logic = {name: logic_class(self.apps[name]) for name, _, logic_class, _ in pages}

#         # Step 3: Create Per-Page Controllers
#         self.page_controllers = {
#             name: controller_class(self.apps[name], self.logic[name])
#             for name, _, _, controller_class in pages
#         }

#         # Add pages to the stack
#         for page in self.apps.values():
#             self.stack.addWidget(page)

#         # Create the controller
#         self.controller = AppConnector(self.apps, self.logic)


#         menubar = QMenuBar(self)
#         app_menu = menubar.addMenu("Apps")

#         for name in self.apps:
#             action = QAction(name.capitalize(), self)
#             action.triggered.connect(lambda _, n=name: self.switch_to(n))
#             app_menu.addAction(action)

#         self.setMenuBar(menubar)

#         # Main container setup
#         container = QWidget()
#         layout = QVBoxLayout(container)
#         layout.addWidget(self.stack)
#         self.setCentralWidget(container)

#         self.switch_to("SentenceChunks")

#     def switch_to(self, app_name):
#         try:
#             self.stack.setCurrentWidget(self.apps[app_name])
#         except KeyError:
#             print(f"Invalid app name: {app_name}")
#             print("Valid app names are:", list(self.apps.keys()))



# from PyQt6.QtWidgets import QMainWindow, QDockWidget, QAction, QWidget
# from PyQt6.QtCore import Qt



# class Dashboard(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("UI")
#         self.resize(800, 480)
#         self.setup_stylesheets()

#         pages = load_apps()

#         self.apps = {name: layout_class() for name, layout_class, _, _ in pages}
#         self.logic = {name: logic_class(self.apps[name]) for name, _, logic_class, _ in pages}
#         self.page_controllers = {
#             name: controller_class(self.apps[name], self.logic[name])
#             for name, _, _, controller_class in pages
#         }
#         self.controller = AppConnector(self.apps, self.logic)

#         self.docks = {}
#         self.actions = {}

#         menubar = self.menuBar()
#         app_menu = menubar.addMenu("Apps")

#         dock_areas = [
#             Qt.DockWidgetArea.RightDockWidgetArea,
#             Qt.DockWidgetArea.BottomDockWidgetArea,
#             Qt.DockWidgetArea.LeftDockWidgetArea,
#             Qt.DockWidgetArea.TopDockWidgetArea,
#         ]

#         first_app_name = list(self.apps.keys())[5]
#         self.setCentralWidget(self.apps[first_app_name])

#         for i, (name, widget) in enumerate(self.apps.items()):
#             action = QAction(name.capitalize(), self)
#             action.setCheckable(True)
#             app_menu.addAction(action)
#             self.actions[name] = action

#             if name == first_app_name:
#                 action.setChecked(True)
#                 action.triggered.connect(lambda checked, n=name: self.setCentralWidget(self.apps[n]))
#                 continue

#             dock = QDockWidget(name)
#             dock.setObjectName(name)
#             dock.setFeatures(
#                 QDockWidget.DockWidgetFeature.DockWidgetClosable |
#                 QDockWidget.DockWidgetFeature.DockWidgetMovable |
#                 QDockWidget.DockWidgetFeature.DockWidgetFloatable
#             )
#             dock.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
#             dock.setWidget(widget)

#             self.docks[name] = dock

#             dock.visibilityChanged.connect(lambda visible, n=name: self.actions[n].setChecked(visible))
#             action.triggered.connect(lambda checked, n=name: self.docks[n].setVisible(checked))

#             area = dock_areas[(i - 1) % len(dock_areas)]
#             self.addDockWidget(area, dock)
#             dock.hide()

#         # Restore geometry and dock state
#         settings = QSettings("YourCompany", "YourApp")
#         self.restoreGeometry(settings.value("geometry", b""))
#         self.restoreState(settings.value("windowState", b""))



#     def set_central_app(self, name):
#         self.setCentralWidget(self.apps[name])

#     def closeEvent(self, event):
#         settings = QSettings("YourCompany", "YourApp")
#         settings.setValue("geometry", self.saveGeometry())
#         settings.setValue("windowState", self.saveState())
#         super().closeEvent(event)


#     def setup_stylesheets(self):
#         # Yu Gothic UI
#         """
#             QMainWindow {
#                 background-color: #1a0d1c;
#             }
#             QLabel {
#                 background-color: #AAAAAA;
#             }
#         """
#         self.setStyleSheet("""
#             QWidget {
#                 font-family: "Meiryo";
#                 color: #FFFFFF;
#                 background-color: #222222;
#             }

#             QLineEdit, QListWidget {
#                 font-size: 16pt;
#                 selection-background-color: #5555aa;
#                 selection-color: #ffffff;
#                 background-color: #222222;
#             }

#             QListWidget::item:selected {
#                 background-color: #5555aa;
#                 color: white;
#             }
            
#             QLineEdit:focus, QListWidget:focus {
#                 border: 1px solid #88C;
#             }

#         """)


# # ----- Entry Point -----
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     win = Dashboard()
#     win.show()
#     sys.exit(app.exec())

class CenterWrapper(QGroupBox):
    def __init__(self, title: str, content: QWidget):
        super().__init__(f"{title} (Center)")
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(content)
        self.setStyleSheet("""
            QGroupBox {
                border: 2px solid #888;
                border-radius: 4px;
                margin-top: 20px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 2px 4px;
            }
        """)

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UI")
        self.resize(800, 480)
        self.setup_stylesheets()

        pages = load_apps()

        self.apps = {name: layout_class() for name, layout_class, _, _ in pages}
        self.logic = {name: logic_class(self.apps[name]) for name, _, logic_class, _ in pages}
        self.page_controllers = {
            name: controller_class(self.apps[name], self.logic[name])
            for name, _, _, controller_class in pages
        }
        self.controller = AppConnector(self.apps, self.logic)

        self.docks = {}
        self.actions_dock = {}
        self.actions_center = {}

        menubar = self.menuBar()
        dock_menu = menubar.addMenu("Docks")
        center_menu = menubar.addMenu("Center Widget")

        dock_areas = [
            Qt.DockWidgetArea.RightDockWidgetArea,
            Qt.DockWidgetArea.BottomDockWidgetArea,
            Qt.DockWidgetArea.LeftDockWidgetArea,
            Qt.DockWidgetArea.TopDockWidgetArea,
        ]


        self.current_center = None


        for i, (name, widget) in enumerate(self.apps.items()):
            # Dock menu action
            dock_action = QAction(name.capitalize(), self)
            dock_action.setCheckable(True)
            dock_menu.addAction(dock_action)
            self.actions_dock[name] = dock_action

            # Center menu action
            center_action = QAction(name.capitalize(), self)
            center_action.setCheckable(True)
            center_menu.addAction(center_action)
            self.actions_center[name] = center_action

            # Setup dock widgets
            dock = QDockWidget(name)
            dock.setObjectName(name)
            dock.setFeatures(
                QDockWidget.DockWidgetFeature.DockWidgetClosable
                | QDockWidget.DockWidgetFeature.DockWidgetMovable
                | QDockWidget.DockWidgetFeature.DockWidgetFloatable
            )
            dock.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
            dock.setWidget(widget)
            self.docks[name] = dock


            area = dock_areas[(i - 1) % len(dock_areas)]
            self.addDockWidget(area, dock)

            # Connect signals
            dock_action.triggered.connect(self.make_dock_toggle_func(name))
            center_action.triggered.connect(self.make_center_toggle_func(name))
            dock.visibilityChanged.connect(self.make_visibility_sync_func(name))

        # Restore geometry and state if you want:
        settings = QSettings("YourCompany", "YourApp")
        geo = settings.value("geometry")
        state = settings.value("windowState")
        center = settings.value("currentCenter")
        if center in self.actions_center:
            self.actions_center[center].trigger()
        if geo:
            self.restoreGeometry(geo)
        if state:
            self.restoreState(state)


    def make_dock_toggle_func(self, name):
        def toggle(checked):
            if name != self.current_center:
                self.docks[name].setVisible(checked)
            else:
                self.actions_dock[name].setChecked(False)
        return toggle


    def make_center_toggle_func(self, name):
        def toggle(checked):
            # Move current center to dock
            prev = self.current_center
            self.current_center = name

            if prev is not None:
                prev_dock = self.docks[prev]
                prev_dock.setWidget(self.apps[prev])
                prev_dock.hide()

                self.actions_dock[prev].setEnabled(True)
                self.actions_dock[prev].setText(prev.capitalize())
                self.actions_dock[prev].setChecked(prev_dock.isVisible())

                

                self.actions_center[prev].setEnabled(True)
                self.actions_center[prev].setText(f"{prev.capitalize()}")
                self.actions_center[prev].setChecked(prev_dock.isVisible())
                
                self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, prev_dock)
                
                dock = self.docks[name]
                self.removeDockWidget(dock)
                dock.hide()
                dock.setWidget(None)
            
            widget = self.apps[name]
            widget.setParent(None)
            wrapped = CenterWrapper(f"{name.capitalize()}", self.apps[name])
            self.setCentralWidget(wrapped)
            widget.show()

            self.actions_dock[name].setEnabled(False)
            self.actions_dock[name].setText(f"{name.capitalize()} (center)")
            self.actions_dock[name].setChecked(False)

            self.actions_center[name].setEnabled(False)
            self.actions_center[name].setText(f"{name.capitalize()} (center)")
        return toggle


    def make_visibility_sync_func(self, name):
        def sync(visible):
            if name != self.current_center:
                self.actions_dock[name].blockSignals(True)
                self.actions_dock[name].setChecked(visible)
                self.actions_dock[name].blockSignals(False)
        return sync

    

    def closeEvent(self, event):
        settings = QSettings("YourCompany", "YourApp")
        settings.setValue("currentCenter", self.current_center)
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        super().closeEvent(event)

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

            QMenu::item:disabled {
                color: #777777;
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
