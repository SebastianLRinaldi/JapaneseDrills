from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from typing import Literal
from src.contracts.component_interface import *

Orientation = Literal["horizontal", "vertical"]
LayoutType = Literal["group", "splitter", "tabs", "grid", "stacked"]


class LayoutBuilder():
    def __init__(self):
        super().__init__()

    def apply_layout(self, component:ComponentInterface, structure: StructureInterface):
        layout = self.build_layout(structure.layout_data)
        layout.setContentsMargins(0, 0, 0, 0)
        component.setLayout(layout)
    
    def build_layout(self, data) -> QWidget | QLayout:
        if isinstance(data, QWidget):
            return data
        elif isinstance(data, str):
            return getattr(self, data)


        if isinstance(data, list):
            layout = QVBoxLayout()
            for item in data:
                w = self.build_layout(item)
                if isinstance(w, QWidget):
                    layout.addWidget(w)
                else:
                    layout.addLayout(w)
            return layout

        if isinstance(data, dict):
            if "group" in data:
                info = data["group"]
                orient = info.get("orientation", "vertical")
                children = info.get("children", [])

                layout = QVBoxLayout() if orient == "vertical" else QHBoxLayout()
                for item in children:
                    w = self.build_layout(item)
                    if isinstance(w, QWidget):
                        layout.addWidget(w)
                    else:
                        layout.addLayout(w)

                return layout

            if "box" in data:
                info = data["box"]
                title = info.get("title", "")
                orient = info.get("orientation", "vertical")
                children = info.get("children", [])
                
                groupbox = QGroupBox(title) 
                layout = QVBoxLayout() if orient == "vertical" else QHBoxLayout()
                for item in children:
                    w = self.build_layout(item)
                    if isinstance(w, QWidget):
                        layout.addWidget(w) # bloats space --> layout.addWidget(w,  stretch=1)
                    else:
                        container = QWidget()
                        container.setLayout(w)
                        layout.addWidget(container) # bloats space --> layout.addWidget(container, stretch=1)

                # layout.setContentsMargins(0, 0, 0, 0)
                # layout.setSpacing(0)
                # groupbox.setFlat(True)  # Optional: removes border if you want
                # groupbox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

                groupbox.setLayout(layout)

                return groupbox

            if "splitter" in data:
                info = data["splitter"]
                orient = Qt.Orientation.Vertical if info.get("orientation") == "vertical" else Qt.Orientation.Horizontal
                splitter = QSplitter(orient)
                for item in info["children"]:
                    w = self.build_layout(item)
                    if isinstance(w, QWidget):
                        splitter.addWidget(w)
                    else:
                        container = QWidget()
                        container.setLayout(w)
                        splitter.addWidget(container)

                return splitter

            if "tabs" in data:
                info = data["tabs"]
                tab_labels = info.get("tab_labels", [])  # Expecting a list
                tabs = QTabWidget()
                for idx, item in enumerate(info["children"]):
                    w = self.build_layout(item)
                    if not isinstance(w, QWidget):
                        container = QWidget()
                        container.setLayout(w)
                        w = container
                    if tab_labels is not None:
                        title = tab_labels[idx] if idx < len(tab_labels) else f"Tab {idx + 1}"
                        tabs.addTab(w, title)


                return tabs

            if "grid" in data:
                info = data["grid"]
                layout = QGridLayout()
                children = info["children"]
                rows = info.get("rows", 1)
                cols = info.get("columns", len(children))
                for i, item in enumerate(children):
                    w = self.build_layout(item)
                    if isinstance(w, QWidget):
                        layout.addWidget(w, i // cols, i % cols)
                    else:
                        container = QWidget()
                        container.setLayout(w)
                        layout.addWidget(container, i // cols, i % cols)
                return layout

            if "stacked" in data:
                info = data["stacked"]
                layout = QStackedLayout()
                for item in info["children"]:
                    w = self.build_layout(item)
                    if isinstance(w, QWidget):
                        layout.addWidget(w)
                    else:
                        container = QWidget()
                        container.setLayout(w)
                        layout.addWidget(container)
                container = QWidget()
                container.setLayout(layout)
                return container


            if "form" in data:
                info = data["form"]
                layout = QFormLayout()
                for label, widget_name in info["children"]:
                    # widget = getattr(self, widget_name)
                    widget = self.build_layout(widget_name)
                    layout.addRow(label, widget)
                return layout


            if "scroll" in data:
                info = data["scroll"]
                child_spec = info["child"]
                w = self.build_layout(child_spec)

                scroll_area = QScrollArea()
                scroll_area.setFrameShape(QFrame.Shape.NoFrame)
                scroll_area.setWidgetResizable(True)

                if isinstance(w, QWidget):
                    scroll_area.setWidget(w)
                else:
                    container = QWidget()
                    container.setLayout(w)
                    scroll_area.setWidget(container)

                return scroll_area

        raise TypeError(f"Invalid type in set_layout:  | isQWidget:{isinstance(data, QWidget)} | isQLayout:{isinstance(data, QLayout)} | = Given TYPE: {type(data)}")

    def group(self, orientation: Orientation = None, children: list | None = None):
        """ 
        A simple way to create a group of widgets
        - Helpful for things like making differnt orientations of widgets in the same component
        """
        return {
            "group": {
                "orientation": orientation,
                "children": children
            }
        }

    def box(self, orientation: Orientation = None, title: str | None = None,children: list | None = None):
        """
        Functions like group but with an optional title for a group of widgets
        - Adds a nice border around the group
        """
        return {
            "box": {
                "title":title,
                "orientation": orientation,
                "children": children
            }
        }

    def splitter(self, orientation: Orientation = None, children: list | None = None):
        """
        Will add a draggable splitter bar between each widget.
        - The widgets will be stacked with a spliter line in that orientation 
        """
        return {
            "splitter": {
                "orientation": orientation,
                "children": children
            }
        }

    def tabs(self, tab_labels: list = None, children: list | None = None):
        """
        Will make a new tab for each widget in children
        - tab labels and tab widgets are not matched like form (label, widget)
        - You will need to make sure order of widgets follows order of labels
        """
        return {
            "tabs": {
                "tab_labels": tab_labels,
                "children": children
            }
        }

    def grid(self, children: list | None = None, rows=1, columns=None):
        return {
            "grid": {
                "children": children,
                "rows": rows,
                "columns": columns or len(children)
            }
        }

    def stacked(self, children: list | None = None):
        return {
            "stacked": {
                "children": children
            }
        }

    def form(self, children: list[tuple[str, str]]):
        """
        A way to make label:widget pairings as one row
        - Children are made as (label, widget)
        - Stacks vertically for each paring
        """
        return {
            "form": {
                "children": children
            }
        }

    def scroll(self, child):
        return {
            "scroll": {
                "child": child
            }
        }