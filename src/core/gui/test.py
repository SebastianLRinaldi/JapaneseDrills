import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class PolicyDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QSizePolicy Detailed Demo")
        self.setMinimumSize(800, 600)
        self.build_ui()

    def build_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Define policies for horizontal and vertical demonstration
        policies = [
            # (QSizePolicy.Policy.Ignored, "Ignored"),
            (QSizePolicy.Policy.Fixed, "Fixed"),
            # (QSizePolicy.Policy.Minimum, "Minimum"),
            # (QSizePolicy.Policy.Maximum, "Maximum"),

            (QSizePolicy.Policy.MinimumExpanding, "MinimumExpanding"),
            (QSizePolicy.Policy.Expanding, "Expanding"),
            # (QSizePolicy.Policy.Preferred, "Preferred"),
        ]

        description_label = QLabel(
            "Resize the window to see how each policy behaves horizontally (width) and vertically (height).",
            self
        )
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        main_layout.addWidget(description_label)

        # Horizontal layout demo
        main_layout.addWidget(QLabel("Horizontal Policies:"))
        h_layout = QHBoxLayout()
        h_layout.setSpacing(10)

        for policy, name in policies:
            w = QFrame()
            w.setFrameShape(QFrame.Shape.Box)
            w.setStyleSheet("background-color: lightblue;")
            w.setMinimumHeight(50)
            w.setMinimumWidth(60)

            # Horizontal policy affects width
            sp = QSizePolicy(policy, QSizePolicy.Policy.Fixed)
            w.setSizePolicy(sp)

            label = QLabel(name, w)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            font = QFont()
            font.setPointSize(10)
            font.setBold(True)
            label.setFont(font)

            h_layout.addWidget(w)

        main_layout.addLayout(h_layout)

        # Vertical layout demo
        main_layout.addWidget(QLabel("Vertical Policies:"))
        v_layout = QVBoxLayout()
        v_layout.setSpacing(10)

        for policy, name in policies:
            w = QFrame()
            w.setFrameShape(QFrame.Shape.Box)
            w.setStyleSheet("background-color: lightgreen;")
            w.setMinimumHeight(40)
            w.setMinimumWidth(150)

            # Vertical policy affects height
            sp = QSizePolicy(QSizePolicy.Policy.Fixed, policy)
            w.setSizePolicy(sp)

            label = QLabel(name, w)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            font = QFont()
            font.setPointSize(10)
            font.setBold(True)
            label.setFont(font)

            v_layout.addWidget(w)

        main_layout.addLayout(v_layout)

        # Show how flags work
        main_layout.addWidget(QLabel("Flags Example: MinimumExpanding with/without ExpandFlag"))
        flags_layout = QHBoxLayout()
        flags_layout.setSpacing(10)

        # Widget with MinimumExpanding (default GrowFlag)
        w1 = QFrame()
        w1.setFrameShape(QFrame.Shape.Box)
        w1.setStyleSheet("background-color: lightcoral;")
        w1.setMinimumWidth(60)
        w1.setMinimumHeight(50)
        sp1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        w1.setSizePolicy(sp1)
        w1_label = QLabel("MinExpanding\n(GrowFlag)", w1)
        w1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        flags_layout.addWidget(w1)

        # Widget with MinimumExpanding + Expanding flag
        w2 = QFrame()
        w2.setFrameShape(QFrame.Shape.Box)
        w2.setStyleSheet("background-color: lightpink;")
        w2.setMinimumWidth(60)
        w2.setMinimumHeight(50)
        sp2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sp2.setHorizontalStretch(1)
        w2.setSizePolicy(sp2)
        w2_label = QLabel("MinExpanding + ExpandingFlag", w2)
        w2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        flags_layout.addWidget(w2)

        main_layout.addLayout(flags_layout)

        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = PolicyDemo()
    demo.show()
    sys.exit(app.exec())







# from PyQt6.QtCore import *
# from PyQt6.QtWidgets import * 
# from PyQt6.QtGui import *

# import sys

# class SizeConstraintDemo(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("QLayout SizeConstraint Demo")

#         # Create main layout
#         layout = QVBoxLayout()

#         # Buttons to visualize constraints
#         layout.addWidget(QPushButton("Button 1"))
#         layout.addWidget(QPushButton("Button 2"))
#         layout.addWidget(QPushButton("Button 3"))

#         # Apply different size constraints here
#         # Uncomment one at a time to see its effect

#         # 1. Default constraint
#         # layout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)

#         # 2. No constraint (layout can shrink or grow freely)
#         # layout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)

#         # 3. Minimum size (layout enforces minimum size)
#         # layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

#         # 4. Fixed size (layout cannot grow or shrink)
#         # layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

#         # 5. Maximum size (layout enforces maximum size)
#         # layout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)

#         # 6. Min and max size (layout enforces both)
#         layout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)

#         # Optional: remove default margins and spacing
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.setSpacing(0)

#         self.setLayout(layout)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     demo = SizeConstraintDemo()
#     demo.resize(300, 200)
#     demo.show()
#     sys.exit(app.exec())





# import sys
# from PyQt6 import QtWidgets, QtCore

# class LayoutDemo(QtWidgets.QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Layout Alignment & SizeConstraint Demo")
        
#         # Buttons in the layout
#         self.buttons = [QtWidgets.QPushButton(f"Button {i}") for i in range(1, 4)]
        
#         # Layout
#         self.layout = QtWidgets.QVBoxLayout()
#         for btn in self.buttons:
#             self.layout.addWidget(btn)
        
#         self.setLayout(self.layout)
        
#         # Alignment and SizeConstraint options
#         self.alignments = [
#             QtCore.Qt.AlignmentFlag.AlignLeft,
#             QtCore.Qt.AlignmentFlag.AlignRight,
#             QtCore.Qt.AlignmentFlag.AlignHCenter,
#             QtCore.Qt.AlignmentFlag.AlignJustify,
#         ]
#         self.constraints = [
#             QtWidgets.QLayout.SizeConstraint.SetNoConstraint,
#             QtWidgets.QLayout.SizeConstraint.SetMinimumSize,
#             QtWidgets.QLayout.SizeConstraint.SetFixedSize,
#             QtWidgets.QLayout.SizeConstraint.SetMaximumSize,
#             QtWidgets.QLayout.SizeConstraint.SetMinAndMaxSize,
#         ]
#         self.current_alignment = 0
#         self.current_constraint = 0

#         # Buttons to cycle through settings
#         self.cycle_alignment_btn = QtWidgets.QPushButton("Cycle Alignment")
#         self.cycle_alignment_btn.clicked.connect(self.cycle_alignment)
#         self.cycle_constraint_btn = QtWidgets.QPushButton("Cycle SizeConstraint")
#         self.cycle_constraint_btn.clicked.connect(self.cycle_constraint)

#         self.layout.addWidget(self.cycle_alignment_btn)
#         self.layout.addWidget(self.cycle_constraint_btn)

#         self.show()

#     def cycle_alignment(self):
#         # Pick the next alignment
#         self.current_alignment = (self.current_alignment + 1) % len(self.alignments)
#         alignment = self.alignments[self.current_alignment]

#         # Apply alignment to each widget in the layout
#         for i in range(self.layout.count() - 2):  # exclude the last two cycle buttons
#             item = self.layout.itemAt(i)
#             self.layout.setAlignment(item.widget(), alignment)
        
#         print("Applied alignment:", alignment)

#     def cycle_constraint(self):
#         # Pick the next size constraint
#         self.current_constraint = (self.current_constraint + 1) % len(self.constraints)
#         constraint = self.constraints[self.current_constraint]

#         # Apply size constraint to the layout
#         self.layout.setSizeConstraint(constraint)
#         self.layout.activate()  # force re-layout
#         print("Applied size constraint:", constraint)


# app = QtWidgets.QApplication(sys.argv)
# demo = LayoutDemo()
# sys.exit(app.exec())
