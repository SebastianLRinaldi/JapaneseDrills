from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from application.apps.BasicApp.basicLayout import BasicLayout, ChunkInput

class BasicLogic:
    def __init__(self, ui: BasicLayout):
        self.ui = ui

    def update_widget(self) -> None:
        self.ui.label.setText("Im on 1, I have been updated by 1!")

    def reset_widget(self) -> None:
        self.ui.label.setText("Im on 1, I have been reset by 1!")

    def show_context_menu(self, pos: QPoint):
        menu = QMenu()

        add_row_above_action = QAction("Add 1 Above", self.ui.chunk_holder)
        add_row_above_action.triggered.connect(self.add_row_above)
        menu.addAction( add_row_above_action)

        
        add_row_action = QAction("Add 1 Below", self.ui.chunk_holder)
        add_row_action.triggered.connect(self.add_row_below)
        menu.addAction(add_row_action)


        remove_row_action = QAction("Remove Row", self.ui.chunk_holder)
        remove_row_action.triggered.connect(self.remove_row)
        menu.addAction(remove_row_action)
        

        menu.exec(self.ui.chunk_holder.mapToGlobal(pos))

    def add_row(self):
        """Add an empty EditableItem"""
        item_widget = ChunkInput()
        item = QListWidgetItem()
        item.setSizeHint(item_widget.sizeHint())
        self.ui.chunk_holder.addItem(item)
        self.ui.chunk_holder.setItemWidget(item, item_widget)

    def add_row_below(self):
        item_widget = ChunkInput()
        item = QListWidgetItem()
        item.setSizeHint(item_widget.sizeHint())

        current_row = self.ui.chunk_holder.currentRow()
        if current_row >= 0:
            # Insert below selected row
            self.ui.chunk_holder.insertItem(current_row + 1, item)
        else:
            # Append at end
            self.ui.chunk_holder.addItem(item)

        self.ui.chunk_holder.setItemWidget(item, item_widget)

    
    def add_row_above(self):
        item_widget = ChunkInput()
        item = QListWidgetItem()
        item.setSizeHint(item_widget.sizeHint())

        current_row = self.ui.chunk_holder.currentRow()
        if current_row >= 0:
            # Insert above selected row
            self.ui.chunk_holder.insertItem(current_row, item)
        else:
            # Insert at top if nothing selected
            self.ui.chunk_holder.insertItem(0, item)

        self.ui.chunk_holder.setItemWidget(item, item_widget)


    def remove_row(self):
        selected_items = self.ui.chunk_holder.selectedItems()

        if selected_items:
            # Remove selected rows
            selected_rows = [self.ui.chunk_holder.row(item) for item in selected_items]
            selected_rows.sort(reverse=True)

            for row in selected_rows:
                item = self.ui.chunk_holder.takeItem(row)
                widget = self.ui.chunk_holder.itemWidget(item)
                if widget:
                    widget.deleteLater()
                del item
