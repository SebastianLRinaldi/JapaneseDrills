from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.gui.layout_builder import LayoutBuilder
from .blueprint import Blueprint

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


class Structure(LayoutBuilder, Blueprint):
    """
    how you arrange and decorate the hardware before anyone touches it.
    """

    def __init__(self, component: QMainWindow):
        super().__init__()  # just calls UiManager.__init__ with no args | WidgetTypes has no init so dont need it 
        self.component = component
        self._map_widgets(component)
        self.set_widgets()
        self.setup_stylesheets()
        # self.layout_data = [self.stack]

        # self.apply_layout(component, self)

        self.apps = {}
        self.docks = {}
        self.actions_dock = {}
        self.actions_center = {}
        # self.dock_home()
        self.stack_home()

################## DOCK APPS FOR HOME ################################

    def dock_home(self):
        self.load_apps()
        
        menubar = self.component.menuBar()
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
            dock_action = QAction(name.capitalize(), self.component)
            dock_action.setCheckable(True)
            dock_menu.addAction(dock_action)
            self.actions_dock[name] = dock_action

            # Center menu action
            center_action = QAction(name.capitalize(), self.component)
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
            self.component.addDockWidget(area, dock)

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
            self.component.restoreGeometry(geo)
        if state:
            self.component.restoreState(state)

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
            self.component.setCentralWidget(wrapped)
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

################## STACK APPS FOR HOME ################################

    def stack_home(self):
        self.load_apps()
        self.add_apps_to_stack()
        self.setup_menu()
        self.switch_to("textEdior")
    
    def add_apps_to_stack(self):
        for name, widget in self.apps.items():
            self.stack.addWidget(widget)

    def setup_menu(self):
        menubar = QMenuBar(self.component)
        app_menu = menubar.addMenu("Apps")

        for name in self.apps:
            action = QAction(name.capitalize(), self.component)
            action.triggered.connect(lambda _, n=name: self.switch_to(n))
            app_menu.addAction(action)

        self.component.setMenuBar(menubar)

    def switch_to(self, app_name):
        widget = self.apps.get(app_name)
        if widget:
            self.stack.setCurrentWidget(widget)
        else:
            print(f"Invalid app name: {app_name}")
            print("Valid apps:", list(self.apps.keys()))

    def load_apps(self):
        for name in self.__annotations__:
            if name != "stack":
                widget = getattr(self, name)
                if isinstance(widget, QWidget):
                    self.apps[name] = widget

    def set_widgets(self):
        self.component.setWindowTitle("Widget Dashboard")
        self.component.resize(800, 600)
        self.component.setCentralWidget(self.stack)

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
        self.component.setStyleSheet("""
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






