from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

"""
Working Cards with mouse wheel zoom
"""
# class Card(QGraphicsRectItem):
#     def __init__(self, text, x, y):
#         super().__init__(QRectF(0, 0, 40, 60))
#         self.setBrush(QBrush(QColor(240,240,240)))
#         self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable)
#         self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable)
#         self.setPos(x, y)

        
#         # Add text label as a child
#         self.label = QGraphicsTextItem(text, self)
#         self.label.setDefaultTextColor(QColor(30, 30, 30))
#         self.label.setPos(10, 20)  # Slight padding inside the card

# class View(QGraphicsView):
#     def wheelEvent(self, event):
#         zoom = 1.2 if event.angleDelta().y() > 0 else 1/1.2
#         self.scale(zoom, zoom)

# app = QApplication([])
# scene = QGraphicsScene()
# view = View(scene)

# scene.addItem(Card("猫", 0, 0))
# scene.addItem(Card("犬", 200, 200))
# scene.addItem(Card("竜", -200, 100))

# view.show()
# app.exec()



"""
Bounding box works for card groups
"""
# class Card(QGraphicsRectItem):
#     def __init__(self, text, x, y):
#         super().__init__(QRectF(0, 0, 120, 60))
#         self.setBrush(QBrush(QColor(240, 240, 240)))

#         self.groups = []

#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)

#         self.setPos(x, y)

#         label = QGraphicsTextItem(text, self)
#         label.setDefaultTextColor(QColor(30, 30, 30))
#         label.setPos(10, 20)

        

#     def itemChange(self, change, value):
#         if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
#             for g in self.groups:
#                 g.update_group_boundary()
#         return super().itemChange(change, value)


# class ClusterGroup(QGraphicsItem):
#     def __init__(self, cards):
#         super().__init__()
#         self.cards = cards
#         for c in cards:
#             c.groups.append(self)
#         self.padding = 30
#         self.update_group_boundary()

#     def update_group_boundary(self):
#         self.prepareGeometryChange()

#         rects = [
#             c.mapToScene(c.boundingRect()).boundingRect()
#             for c in self.cards
#         ]
#         x1 = min(r.left() for r in rects) - self.padding
#         y1 = min(r.top() for r in rects) - self.padding
#         x2 = max(r.right() for r in rects) + self.padding
#         y2 = max(r.bottom() for r in rects) + self.padding

#         # Move the group to the top-left corner of bounding area
#         self.setPos(x1, y1)

#         # Store the local rect relative to (0,0)
#         self.bounds = QRectF(
#             0, 0,
#             x2 - x1,
#             y2 - y1
#         )

#         self.update()

#     def boundingRect(self):
#         return self.bounds

#     def paint(self, painter, option, widget):
#         painter.setRenderHint(QPainter.RenderHint.Antialiasing)
#         painter.setPen(QPen(QColor(120, 120, 255), 3))
#         painter.drawRoundedRect(self.bounds, 25, 25)


# class View(QGraphicsView):
#     def __init__(self, scene):
#         super().__init__(scene)

#     def wheelEvent(self, event):
#         zoom = 1.2 if event.angleDelta().y() > 0 else 1/1.2
#         self.scale(zoom, zoom)


# app = QApplication([])
# scene = QGraphicsScene()

# # Create cards
# c1 = Card("猫", 500, 0)
# c2 = Card("犬", 500, 200)
# c3 = Card("竜", -500, 100)

# scene.addItem(c1)
# scene.addItem(c2)
# scene.addItem(c3)

# # Create group that circles these cards
# group = ClusterGroup([c1, c2, c3])
# scene.addItem(group)

# view = View(scene)
# view.setWindowTitle("Cards with Dynamic Group Outline")
# view.show()

# app.exec()





# from PyQt6.QtCore import QRectF
# from PyQt6.QtWidgets import (
#     QApplication, QGraphicsView, QGraphicsScene,
#     QGraphicsRectItem, QGraphicsTextItem, QGraphicsItem
# )
# from PyQt6.QtGui import QBrush, QColor, QPainter, QPen

# class Card(QGraphicsRectItem):
#     def __init__(self, text, x, y):
#         super().__init__(QRectF(0, 0, 120, 60))
#         self.setBrush(QBrush(QColor(240, 240, 240)))

#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)

#         self.setPos(x, y)

#         label = QGraphicsTextItem(text, self)
#         label.setDefaultTextColor(QColor(30, 30, 30))
#         label.setPos(10, 20)

#     def itemChange(self, change, value):
#         if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
#             # Update selection outline if this card is selected
#             if self.isSelected():
#                 for item in self.scene().items():
#                     if isinstance(item, SelectionGroup):
#                         item.update_group_boundary()
#         return super().itemChange(change, value)


# class SelectionGroup(QGraphicsItem):
#     def __init__(self, scene):
#         super().__init__()
#         self.scene = scene
#         self.padding = 30
#         self.bounds = QRectF()
#         self.setZValue(-1)  # draw behind cards

#     def update_group_boundary(self):
#         selected = [item for item in self.scene.selectedItems() if isinstance(item, Card)]
#         if not selected:
#             self.prepareGeometryChange()
#             self.bounds = QRectF()  # hide when no selection
#             self.update()
#             return

#         rects = [c.mapToScene(c.boundingRect()).boundingRect() for c in selected]
#         x1 = min(r.left() for r in rects) - self.padding
#         y1 = min(r.top() for r in rects) - self.padding
#         x2 = max(r.right() for r in rects) + self.padding
#         y2 = max(r.bottom() for r in rects) + self.padding

#         self.prepareGeometryChange()
#         self.bounds = QRectF(x1, y1, x2 - x1, y2 - y1)  # store in scene coordinates
#         self.update()

#     def boundingRect(self):
#         return self.bounds

#     def paint(self, painter, option, widget):
#         if self.bounds.isNull():
#             return
#         painter.setRenderHint(QPainter.RenderHint.Antialiasing)
#         painter.setPen(QPen(QColor(120, 120, 255), 3))
#         painter.drawRoundedRect(self.bounds, 25, 25)



# class View(QGraphicsView):
#     def __init__(self, scene):
#         super().__init__(scene)

#     def wheelEvent(self, event):
#         zoom = 1.2 if event.angleDelta().y() > 0 else 1/1.2
#         self.scale(zoom, zoom)


# # --- Application setup ---
# app = QApplication([])
# scene = QGraphicsScene()

# # Create cards
# c1 = Card("猫", 500, 0)
# c2 = Card("犬", 500, 200)
# c3 = Card("竜", -500, 100)

# scene.addItem(c1)
# scene.addItem(c2)
# scene.addItem(c3)

# # Create dynamic selection outline
# selection_outline = SelectionGroup(scene)
# scene.addItem(selection_outline)

# # Update outline when selection changes
# scene.selectionChanged.connect(selection_outline.update_group_boundary)

# view = View(scene)
# view.setWindowTitle("Cards with Dynamic Selection Outline")
# view.show()

# app.exec()



"""
Working selection Cluster Sets
"""
# class Card(QGraphicsRectItem):
#     def __init__(self, text, x, y):
#         super().__init__(QRectF(0, 0, 120, 60))
#         self.setBrush(QBrush(QColor(240, 240, 240)))
#         self.groups = []

#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)

#         self.setPos(x, y)

#         label = QGraphicsTextItem(text, self)
#         label.setDefaultTextColor(QColor(30, 30, 30))
#         label.setPos(10, 20)

#     def itemChange(self, change, value):
#         if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
#             for g in self.groups:
#                 g.update_group_boundary()
#         return super().itemChange(change, value)


# class ClusterGroup(QGraphicsItem):
#     def __init__(self, cards):
#         super().__init__()
#         self.cards = cards
#         for c in cards:
#             c.groups.append(self)
#         self.padding = 30
#         self.update_group_boundary()

#     def update_group_boundary(self):
#         if not self.cards:
#             return
#         self.prepareGeometryChange()
#         rects = [c.mapToScene(c.boundingRect()).boundingRect() for c in self.cards]
#         x1 = min(r.left() for r in rects) - self.padding
#         y1 = min(r.top() for r in rects) - self.padding
#         x2 = max(r.right() for r in rects) + self.padding
#         y2 = max(r.bottom() for r in rects) + self.padding

#         self.setPos(x1, y1)
#         self.bounds = QRectF(0, 0, x2 - x1, y2 - y1)
#         self.update()

#     def boundingRect(self):
#         return getattr(self, "bounds", QRectF())

#     def paint(self, painter, option, widget):
#         painter.setRenderHint(QPainter.RenderHint.Antialiasing)
#         painter.setPen(QPen(QColor(120, 120, 255), 3))
#         painter.drawRoundedRect(self.bounds, 25, 25)


# class View(QGraphicsView):
#     def __init__(self, scene):
#         super().__init__(scene)
#         self.scene = scene
#         self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

#     def mouseReleaseEvent(self, event):
#         super().mouseReleaseEvent(event)

#         # Get all selected cards
#         selected_cards = [item for item in self.scene.selectedItems() if isinstance(item, Card)]
#         if selected_cards:
#             # Check if these cards already belong to a group to prevent duplicates
#             already_grouped = any(len(c.groups) > 0 for c in selected_cards)
#             if not already_grouped:
#                 group = ClusterGroup(selected_cards)
#                 self.scene.addItem(group)

#         # Clear selection after creating group
#         for card in selected_cards:
#             card.setSelected(False)

#     def wheelEvent(self, event):
#         zoom = 1.2 if event.angleDelta().y() > 0 else 1 / 1.2
#         self.scale(zoom, zoom)


# # --- Application ---
# app = QApplication([])
# scene = QGraphicsScene()

# # Create cards
# cards = [
#     Card("猫", 0, 0),
#     Card("犬", 0, 150),
#     Card("竜", 200, 50),
#     Card("猿", 200, 200),
#     Card("鳥", -200, 100),
# ]

# for c in cards:
#     scene.addItem(c)

# view = View(scene)
# view.setWindowTitle("Drag-Select Cluster Groups")
# view.show()

# app.exec()





"""
Working Selection to  Cluster, and moveable clusters, with moveable cards/
"""
# class Card(QGraphicsRectItem):
#     def __init__(self, text, x, y):
#         super().__init__(QRectF(0, 0, 120, 60))
#         self.setBrush(QBrush(QColor(240, 240, 240)))
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)

#         self.setPos(x, y)

#         label = QGraphicsTextItem(text, self)
#         label.setDefaultTextColor(QColor(30, 30, 30))
#         label.setPos(10, 20)

#     # Optional: update parent's bounding box if moved individually
#     def itemChange(self, change, value):
#         if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
#             if self.parentItem() is not None:
#                 self.parentItem().update_group_boundary()
#         return super().itemChange(change, value)


# class ClusterGroup(QGraphicsItem):
#     def __init__(self, cards):
#         super().__init__()
#         self.padding = 20
#         self.bounds = QRectF()

#         # Make the cards children of the group
#         for c in cards:
#             c.setParentItem(self)

#         self.update_group_boundary()

#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

#     def update_group_boundary(self):
#         if not self.childItems():
#             return
#         self.prepareGeometryChange()

#         # Get bounding rect in group's coordinates
#         rects = [c.mapToParent(c.boundingRect()).boundingRect() for c in self.childItems()]
#         x1 = min(r.left() for r in rects) - self.padding
#         y1 = min(r.top() for r in rects) - self.padding
#         x2 = max(r.right() for r in rects) + self.padding
#         y2 = max(r.bottom() for r in rects) + self.padding

#         # Update local bounds
#         self.bounds = QRectF(x1, y1, x2 - x1, y2 - y1)
#         self.update()

#     def boundingRect(self):
#         return self.bounds

#     def paint(self, painter, option, widget):
#         painter.setRenderHint(QPainter.RenderHint.Antialiasing)
#         painter.setPen(QPen(QColor(120, 120, 255), 3))
#         painter.drawRoundedRect(self.bounds, 15, 15)


# class View(QGraphicsView):
#     def __init__(self, scene):
#         super().__init__(scene)
#         self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

#     def mouseReleaseEvent(self, event):
#         super().mouseReleaseEvent(event)

#         scene = self.scene()
#         selected_cards = [item for item in scene.selectedItems() if isinstance(item, Card)]

#         if selected_cards:
#             # Make a new cluster from selected cards
#             already_grouped = any(c.parentItem() is not None for c in selected_cards)
#             if not already_grouped:
#                 group = ClusterGroup(selected_cards)
#                 scene.addItem(group)

#         # Clear selection
#         for card in selected_cards:
#             card.setSelected(False)


# # --- App ---
# app = QApplication([])
# scene = QGraphicsScene()

# # Create cards
# cards = [
#     Card("猫", 0, 0),
#     Card("犬", 0, 150),
#     Card("竜", 200, 50),
#     Card("猿", 200, 200),
#     Card("鳥", -200, 100),
# ]

# for c in cards:
#     scene.addItem(c)

# view = View(scene)
# view.setWindowTitle("Movable Cluster with Cards Attached")
# view.show()
# app.exec()



"""
Working Selection to Cluster, and moveable clusters, with moveable cards  + deselection of cards from clusters + moving selected cards without making a cluster on selection
+ and - cursor for selection and deselection

"""
# class Card(QGraphicsRectItem):
#     def __init__(self, text, x, y):
#         super().__init__(QRectF(0, 0, 120, 60))
#         self.setBrush(QBrush(QColor(240, 240, 240)))
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)

#         self.setPos(x, y)

#         label = QGraphicsTextItem(text, self)
#         label.setDefaultTextColor(QColor(30, 30, 30))
#         label.setPos(10, 20)

#     def itemChange(self, change, value):
#         if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
#             parent = self.parentItem()
#             if isinstance(parent, ClusterGroup):
#                 parent.update_group_boundary()
#         return super().itemChange(change, value)


# class ClusterGroup(QGraphicsItem):
#     def __init__(self, cards):
#         super().__init__()
#         self.padding = 20
#         self.bounds = QRectF()
#         self.cards = cards.copy()

#         for c in self.cards:
#             c.setParentItem(self)

#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
#         self.update_group_boundary()

#     def update_group_boundary(self):
#         if not self.cards:
#             self.prepareGeometryChange()
#             self.bounds = QRectF()
#             self.update()
#             return

#         self.prepareGeometryChange()
#         rects = [c.mapToParent(c.boundingRect()).boundingRect() for c in self.cards]
#         x1 = min(r.left() for r in rects) - self.padding
#         y1 = min(r.top() for r in rects) - self.padding
#         x2 = max(r.right() for r in rects) + self.padding
#         y2 = max(r.bottom() for r in rects) + self.padding

#         self.bounds = QRectF(x1, y1, x2 - x1, y2 - y1)
#         self.update()

#     def remove_card(self, card: Card):
#         if card in self.cards:
#             self.cards.remove(card)
#             card.setParentItem(None)
#             # keep its current position in the scene
#             card.setPos(card.mapToScene(QRectF(0, 0, 0, 0).topLeft()))
#             self.update_group_boundary()

#     def boundingRect(self):
#         return self.bounds

#     def paint(self, painter, option, widget):
#         if self.bounds.isNull():
#             return
#         painter.setRenderHint(QPainter.RenderHint.Antialiasing)
#         painter.setPen(QPen(QColor(120, 120, 255), 3))
#         painter.drawRoundedRect(self.bounds, 15, 15)


# class View(QGraphicsView):
#     def __init__(self, scene):
#         super().__init__(scene)
#         self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
#         self.default_cursor = Qt.CursorShape.ArrowCursor

#         # Create a 32x32 transparent pixmap
#         pix = QPixmap(32, 32)
#         pix.fill(Qt.GlobalColor.transparent)

#         # Draw a simple minus sign
#         painter = QPainter(pix)
#         painter.setPen(Qt.GlobalColor.black)
#         painter.setBrush(Qt.GlobalColor.black)
#         painter.drawRect(8, 14, 16, 4)  # x, y, width, height
#         painter.end()

#         # Create a custom cursor from the pixmap
#         self.minus_cursor = QCursor(pix)


#     def keyPressEvent(self, event):
#         if event.key() == Qt.Key.Key_Shift:
#             self.setCursor(Qt.CursorShape.CrossCursor)  # example: plus-like cursor
#         elif event.key() == Qt.Key.Key_Control:
#             self.setCursor(self.minus_cursor)  # example: minus-like cursor
#         else:
#             super().keyPressEvent(event)

#     def keyReleaseEvent(self, event):
#         # Reset cursor when modifier released
#         if event.key() in (Qt.Key.Key_Control, Qt.Key.Key_Shift):
#             self.setCursor(self.default_cursor)
#         else:
#             super().keyReleaseEvent(event)

#     def mouseReleaseEvent(self, event: QMouseEvent):
#         super().mouseReleaseEvent(event)

#         scene = self.scene()
#         selected_cards = [item for item in scene.selectedItems() if isinstance(item, Card)]

#         if selected_cards:
#             # Create a new cluster for cards that aren't already in a cluster
#             new_cards = [c for c in selected_cards if c.parentItem() is None]

#             if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
#                 if new_cards:
#                     group = ClusterGroup(new_cards)
#                     scene.addItem(group)


#             if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
#                 for card in selected_cards:
#                     if isinstance(card.parentItem(), ClusterGroup):
#                         card.parentItem().remove_card(card)

#         # Clear selection
#         # for card in selected_cards:
#         #     card.setSelected(False)


# # --- Application ---
# app = QApplication([])
# scene = QGraphicsScene()

# cards = [
#     Card("猫", 0, 0),
#     Card("犬", 0, 150),
#     Card("竜", 200, 50),
#     Card("猿", 200, 200),
#     Card("鳥", -200, 100),
# ]

# for c in cards:
#     scene.addItem(c)

# view = View(scene)
# view.setWindowTitle("Cluster with Card Removal (Right-click)")
# view.show()
# app.exec()






"""
Complete Working clusters (full select and deselection) with option to make new cluster with deselection
"""
# class Card(QGraphicsRectItem):
#     def __init__(self, text, x, y):
#         super().__init__(QRectF(0, 0, 120, 60))
#         self.setBrush(QBrush(QColor(240, 240, 240)))
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)

#         self.setPos(x, y)

#         label = QGraphicsTextItem(text, self)
#         label.setDefaultTextColor(QColor(30, 30, 30))
#         label.setPos(10, 20)

#     def itemChange(self, change, value):
#         if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
#             parent = self.parentItem()
#             if isinstance(parent, ClusterGroup):
#                 parent.update_group_boundary()
#         return super().itemChange(change, value)


# class ClusterGroup(QGraphicsItem):
#     def __init__(self, cards):
#         super().__init__()
#         self.padding = 20
#         self.bounds = QRectF()
#         self.cards = cards.copy()

#         for c in self.cards:
#             c.setParentItem(self)

#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
#         self.update_group_boundary()

#     def update_group_boundary(self):
#         if not self.cards:
#             self.prepareGeometryChange()
#             self.bounds = QRectF()
#             self.update()
#             return

#         self.prepareGeometryChange()
#         rects = [c.mapToParent(c.boundingRect()).boundingRect() for c in self.cards]
#         x1 = min(r.left() for r in rects) - self.padding
#         y1 = min(r.top() for r in rects) - self.padding
#         x2 = max(r.right() for r in rects) + self.padding
#         y2 = max(r.bottom() for r in rects) + self.padding

#         self.bounds = QRectF(x1, y1, x2 - x1, y2 - y1)
#         self.update()

#     def remove_card(self, card: Card):
#         if card in self.cards:
#             self.cards.remove(card)
#             card.setParentItem(None)
#             # keep its current position in the scene
#             card.setPos(card.mapToScene(QRectF(0, 0, 0, 0).topLeft()))
#             self.update_group_boundary()

#     def boundingRect(self):
#         return self.bounds

#     def paint(self, painter, option, widget):
#         if self.bounds.isNull():
#             return
#         painter.setRenderHint(QPainter.RenderHint.Antialiasing)
#         painter.setPen(QPen(QColor(120, 120, 255), 3))
#         painter.drawRoundedRect(self.bounds, 15, 15)


# class View(QGraphicsView):
#     def __init__(self, scene):
#         super().__init__(scene)
#         self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
#         self.default_cursor = Qt.CursorShape.ArrowCursor

#         # Create a 32x32 transparent pixmap
#         pix = QPixmap(32, 32)
#         pix.fill(Qt.GlobalColor.transparent)

#         # Draw a simple minus sign
#         painter = QPainter(pix)
#         painter.setPen(Qt.GlobalColor.black)
#         painter.setBrush(Qt.GlobalColor.black)
#         painter.drawRect(8, 14, 16, 4)  # x, y, width, height
#         painter.end()

#         # Create a custom cursor from the pixmap
#         self.minus_cursor = QCursor(pix)


#     def keyPressEvent(self, event):
#         if event.key() == Qt.Key.Key_Shift:
#             self.setCursor(Qt.CursorShape.CrossCursor)  # example: plus-like cursor
#         elif event.key() == Qt.Key.Key_Control:
#             self.setCursor(self.minus_cursor)  # example: minus-like cursor
#         else:
#             super().keyPressEvent(event)

#     def keyReleaseEvent(self, event):
#         # Reset cursor when modifier released
#         if event.key() in (Qt.Key.Key_Control, Qt.Key.Key_Shift):
#             self.setCursor(self.default_cursor)
#         else:
#             super().keyReleaseEvent(event)
            
#     # OLD BUT IT WORKS FOR SIMPLE DESELECTION
#     # def mouseReleaseEvent(self, event: QMouseEvent):
#     #     super().mouseReleaseEvent(event)

#     #     scene = self.scene()
#     #     selected_items = scene.selectedItems()

#     #     # Separate cards and clusters
#     #     selected_cards = [item for item in selected_items if isinstance(item, Card)]
#     #     selected_clusters = [item for item in selected_items if isinstance(item, ClusterGroup)]

#     #     # --- Merge clusters if multiple selected ---
#     #     if len(selected_clusters) > 1:
#     #         merged_cards = []
#     #         for cluster in selected_clusters:
#     #             merged_cards.extend(cluster.cards)
#     #             scene.removeItem(cluster)
#     #         new_group = ClusterGroup(merged_cards)
#     #         scene.addItem(new_group)

#     #     # --- Handle creating new cluster from unclustered cards ---
#     #     if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
#     #         new_cards = [c for c in selected_cards if c.parentItem() is None]
#     #         if new_cards:
#     #             group = ClusterGroup(new_cards)
#     #             scene.addItem(group)

#     #     # --- Handle removing cards from clusters ---
#     #     if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
#     #         for card in selected_cards:
#     #             if isinstance(card.parentItem(), ClusterGroup):
#     #                 card.parentItem().remove_card(card)


#     def mouseReleaseEvent(self, event: QMouseEvent):
#         super().mouseReleaseEvent(event)

#         scene = self.scene()
#         selected_items = scene.selectedItems()

#         # Separate cards and clusters
#         selected_cards = [item for item in selected_items if isinstance(item, Card)]
#         selected_clusters = [item for item in selected_items if isinstance(item, ClusterGroup)]

#         # --- Merge clusters if multiple selected ---
#         if len(selected_clusters) > 1:
#             merged_cards = []
#             for cluster in selected_clusters:
#                 merged_cards.extend(cluster.cards)
#                 scene.removeItem(cluster)
#             new_group = ClusterGroup(merged_cards)
#             scene.addItem(new_group)

#         # --- Handle splitting cards from cluster with Alt ---
#         if event.modifiers() & Qt.KeyboardModifier.AltModifier:
#             # Cards that already belong to a cluster
#             cards_to_split = [c for c in selected_cards if isinstance(c.parentItem(), ClusterGroup)]
#             if cards_to_split:
#                 # Remove from original cluster(s)
#                 for card in cards_to_split:
#                     card.parentItem().remove_card(card)
#                 # Make a new cluster with them
#                 new_group = ClusterGroup(cards_to_split)
#                 scene.addItem(new_group)

#         # --- Handle creating new cluster from unclustered cards with Shift ---
#         if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
#             new_cards = [c for c in selected_cards if c.parentItem() is None]
#             if new_cards:
#                 group = ClusterGroup(new_cards)
#                 scene.addItem(group)

#         # --- Handle removing cards from clusters with Control ---
#         if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
#             for card in selected_cards:
#                 if isinstance(card.parentItem(), ClusterGroup):
#                     card.parentItem().remove_card(card)



# # --- Application ---
# app = QApplication([])
# scene = QGraphicsScene()

# cards = [
#     Card("猫", 0, 0),
#     Card("犬", 0, 150),
#     Card("竜", 200, 50),
#     Card("猿", 200, 200),
#     Card("鳥", -200, 100),
# ]

# for c in cards:
#     scene.addItem(c)

# view = View(scene)
# view.setWindowTitle("Cluster with Card Removal (Right-click)")
# view.show()
# app.exec()














"""
Fuly working cards, group selection/deselection/spliting, defintion, and zoom
"""
import sys
import os
from jisho_api.word import Word
from jisho_api import scrape
import threading
import time

# add the root folder to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.helper_classes import *
recall_tracker = RecallTracker()
stored_words = list(recall_tracker.get_stored_words())

class Card(QGraphicsRectItem):
    def __init__(self, text, x, y, definition=None):
        super().__init__(QRectF(0, 0, 40, 60))
        self.text = text
        self.definition = definition if definition else []
        
        self.setBrush(QBrush(QColor(240, 240, 240)))
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)

        self.setPos(x, y)

        label = QGraphicsTextItem(text, self)
        label.setDefaultTextColor(QColor(30, 30, 30))
        label.setPos(0, 20)

        # Fetch definition in background
        # threading.Thread(target=self.fetch_definition, daemon=True).start()

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            parent = self.parentItem()
            if isinstance(parent, ClusterGroup):
                parent.update_group_boundary()
        return super().itemChange(change, value)

    def fetch_definition(self):
        try:
            word = Word()
            result = word.request(self.text)
            self.definition = result.data[0].senses
        except Exception as e:
            print(f"Failed to fetch definition for {self.text}: {e}")

    def mouseDoubleClickEvent(self, event):
        os.system("cls")
        print(f"Definitions for {self.text}:")
        if self.definition:
            for sense in self.definition:
                print(sense.english_definitions)
        else:
            print("Loading definition…")
        event.accept()


class ClusterGroup(QGraphicsItem):
    def __init__(self, cards):
        super().__init__()
        self.padding = 20
        self.bounds = QRectF()
        self.cards = cards.copy()

        for c in self.cards:
            c.setParentItem(self)

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.update_group_boundary()

    def update_group_boundary(self):
        if not self.cards:
            self.prepareGeometryChange()
            self.bounds = QRectF()
            self.update()
            return

        self.prepareGeometryChange()
        rects = [c.mapToParent(c.boundingRect()).boundingRect() for c in self.cards]
        x1 = min(r.left() for r in rects) - self.padding
        y1 = min(r.top() for r in rects) - self.padding
        x2 = max(r.right() for r in rects) + self.padding
        y2 = max(r.bottom() for r in rects) + self.padding

        self.bounds = QRectF(x1, y1, x2 - x1, y2 - y1)
        self.update()

    def add_card(self, card: Card):
        if card not in self.cards:
            # Map the card's current scene position to the cluster's local coordinates
            scene_pos = card.mapToScene(card.boundingRect().topLeft())
            local_pos = self.mapFromScene(scene_pos)
            
            card.setParentItem(self)
            card.setPos(local_pos)
            self.cards.append(card)
            self.update_group_boundary()

    def remove_card(self, card: Card):
        if card in self.cards:
            self.cards.remove(card)
            card.setParentItem(None)
            # keep its current position in the scene
            card.setPos(card.mapToScene(QRectF(0, 0, 0, 0).topLeft()))
            self.update_group_boundary()

    def boundingRect(self):
        return self.bounds

    def paint(self, painter, option, widget):
        if self.bounds.isNull():
            return
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor(120, 120, 255), 3))
        painter.drawRoundedRect(self.bounds, 15, 15)

    def mousePressEvent(self, event):
        modifiers = QApplication.keyboardModifiers()
        if modifiers & (Qt.KeyboardModifier.ShiftModifier |
                        Qt.KeyboardModifier.ControlModifier |
                        Qt.KeyboardModifier.AltModifier):
            # Ignore press so the cluster itself doesn't move
            event.ignore()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        modifiers = QApplication.keyboardModifiers()
        if modifiers & (Qt.KeyboardModifier.ShiftModifier |
                        Qt.KeyboardModifier.ControlModifier |
                        Qt.KeyboardModifier.AltModifier):
            # Ignore movement
            event.ignore()
        else:
            super().mouseMoveEvent(event)


class View(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.default_cursor = Qt.CursorShape.ArrowCursor

        # Create a 32x32 transparent pixmap
        pix = QPixmap(32, 32)
        pix.fill(Qt.GlobalColor.transparent)

        # Draw a simple minus sign
        painter = QPainter(pix)
        painter.setPen(Qt.GlobalColor.black)
        painter.setBrush(Qt.GlobalColor.black)
        painter.drawRect(8, 14, 16, 4)  # x, y, width, height
        painter.end()

        # Create a custom cursor from the pixmap
        self.minus_cursor = QCursor(pix)
        
        # --- Create Alt (division) cursor ---
        pix_alt = QPixmap(32, 32)
        pix_alt.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pix_alt)
        painter.setPen(QPen(Qt.GlobalColor.black))
        # Draw top dot
        painter.drawEllipse(14, 6, 4, 4)
        # Draw horizontal line
        painter.drawLine(8, 16, 24, 16)
        # Draw bottom dot
        painter.drawEllipse(14, 22, 4, 4)

        painter.end()

        self.alt_cursor = QCursor(pix_alt)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Shift:
            self.setCursor(Qt.CursorShape.CrossCursor)
        elif event.key() == Qt.Key.Key_Control:
            self.setCursor(self.minus_cursor)
        elif event.key() == Qt.Key.Key_Alt:
            self.setCursor(self.alt_cursor)
        # Disable moving clusters if any modifier is pressed
        for item in self.scene().selectedItems():
            if isinstance(item, ClusterGroup):
                # item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
                item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
            
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() in (Qt.Key.Key_Control, Qt.Key.Key_Shift, Qt.Key.Key_Alt):
            self.setCursor(self.default_cursor)
        # Re-enable moving clusters after modifier is released
        for item in self.scene().selectedItems():
            if isinstance(item, ClusterGroup):
                # item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
                item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)

        super().keyReleaseEvent(event)


    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.setCursor(Qt.CursorShape.ClosedHandCursor)  # Hand or move cursor
        else:
            super().mousePressEvent(event)

                

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)

        scene = self.scene()
        selected_items = scene.selectedItems()

        # Separate cards and clusters
        selected_cards = [item for item in selected_items if isinstance(item, Card)]
        selected_clusters = [item for item in selected_items if isinstance(item, ClusterGroup)]

        # # --- Merge clusters if multiple selected ---
        # if len(selected_clusters) > 1:
        #     merged_cards = []
        #     for cluster in selected_clusters:
        #         merged_cards.extend(cluster.cards)
        #         scene.removeItem(cluster)
        #     new_group = ClusterGroup(merged_cards)
        #     scene.addItem(new_group)

        # # --- Handle splitting cards from cluster with Alt ---
        # if event.modifiers() & Qt.KeyboardModifier.AltModifier:
        #     # Cards that already belong to a cluster
        #     cards_to_split = [c for c in selected_cards if isinstance(c.parentItem(), ClusterGroup)]
        #     if cards_to_split:
        #         # Remove from original cluster(s)
        #         for card in cards_to_split:
        #             card.parentItem().remove_card(card)
        #         # Make a new cluster with them
        #         new_group = ClusterGroup(cards_to_split)
        #         scene.addItem(new_group)

        # # --- Handle creating new cluster from unclustered cards with Shift ---
        # if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
        #     new_cards = [c for c in selected_cards if c.parentItem() is None]
        #     if new_cards:
        #         group = ClusterGroup(new_cards)
        #         scene.addItem(group)

        # # --- Handle removing cards from clusters with Control ---
        # if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
        #     for card in selected_cards:
        #         if isinstance(card.parentItem(), ClusterGroup):
        #             card.parentItem().remove_card(card)


        # --- Merge clusters if multiple selected ---
        if len(selected_clusters) > 1:
            merged_cards = []
            for cluster in selected_clusters:
                merged_cards.extend(cluster.cards)
                scene.removeItem(cluster)
            new_group = ClusterGroup(merged_cards)
            scene.addItem(new_group)
            selected_clusters = [new_group]  # update to the new merged cluster

        # --- Merge unclustered cards into a selected cluster ---
        if len(selected_clusters) == 1:
            cluster = selected_clusters[0]
            unclustered_cards = [c for c in selected_cards if c.parentItem() is None]
            if unclustered_cards:
                for card in unclustered_cards:
                    cluster.add_card(card)  # make sure your ClusterGroup has add_card()

        # --- Handle splitting cards from cluster with Alt ---
        if event.modifiers() & Qt.KeyboardModifier.AltModifier:
            cards_to_split = [c for c in selected_cards if isinstance(c.parentItem(), ClusterGroup)]
            if cards_to_split:
                for card in cards_to_split:
                    card.parentItem().remove_card(card)
                new_group = ClusterGroup(cards_to_split)
                scene.addItem(new_group)

        # --- Handle creating new cluster from unclustered cards with Shift ---
        if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            new_cards = [c for c in selected_cards if c.parentItem() is None]
            if new_cards:
                group = ClusterGroup(new_cards)
                scene.addItem(group)

        # --- Handle removing cards from clusters with Control ---
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            for card in selected_cards:
                if isinstance(card.parentItem(), ClusterGroup):
                    card.parentItem().remove_card(card)

        if event.button() == Qt.MouseButton.MiddleButton:
            self.setCursor(self.default_cursor)

    def wheelEvent(self, event):
        #TODO Zoom in should happen on the point where the mouse is
        zoom = 1.2 if event.angleDelta().y() > 0 else 1/1.2
        self.scale(zoom, zoom)



# --- Application ---
app = QApplication([])
scene = QGraphicsScene()

# ['water', 'fire']
# stored_words

# cards = []
# for idx, word in enumerate(stored_words[:14]):
#     cards.append(Card(word, idx*4, 0))
# cards = [
#     Card("猫", 0, 0),
#     Card("犬", 0, 150),
#     Card("竜", 200, 50),
#     Card("猿", 200, 200),
#     Card("鳥", -200, 100),
# ]


# # Scrape all definitions at once
# # print(stored_words)
# results = scrape(Word, ['water', 'fire'], r'F:\_Small\344 School Python\JapaneseDrills\jisho_cache')

# # Create cards with definitions
# cards = []
# for idx, word in enumerate(['water', 'fire']):
#     print(word)
#     definition = results.get(word).data[0].senses if word in results and results[word].data else []
#     cards.append(Card(word, idx*50, 0, definition))  # adjust spacing


chunk_size = 5
cards = []

for start_idx in range(0, len(stored_words), chunk_size):
    chunk = stored_words[start_idx:start_idx + chunk_size]
    for idx, word in enumerate(chunk):
        # Position can be adjusted however you like; here we lay them out horizontally
        x = (start_idx + idx) * 4  # or any spacing logic you prefer
        y = 0
        cards.append(Card(word, x, y))
    print(f"Chunk {chunk}: done")
    # time.sleep(1)



for c in cards:
    scene.addItem(c)

view = View(scene)
view.setWindowTitle("Cluster with Card Removal (Right-click)")
view.show()
app.exec()


"""
Middle mouse to move canvas
naming of groups
counter for ungrouped cards
counter for 3 of groups
search feature to find specifc card or group
cards ungrouped should have a different bg or outline
maybe dotted cluster for internal group (but then if a group emerges make it into another group just linked by proximiity but could like cluster with lines)
Zoom in and out 
once a group is made should be able to drag cards into groups
undo and redo for actions
-flip these
    labels inside for word double click defintions
    and labels inside for word tripple click furigana
way to save and view and reconstruct grouped item and ungrouped items after a session
a timer that starts from 0 to see how long I spend grouping
"""