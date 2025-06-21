from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QLineEdit, QPushButton, QListWidget
)
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Styled Window with Random Widgets")
        self.resize(800, 600)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #222222;
            }

            QWidget {
                background-color: #222222;
                font-family: "Meiryo";
                color: #FFFFFF;
                font-size: 14pt;
            }

            QLineEdit, QListWidget, QPushButton {
                background-color: #333333;
                border: 1px solid #555;
                padding: 6px;
                border-radius: 4px;
            }

            QLineEdit:focus, QListWidget:focus, QPushButton:focus {
                border: 1px solid #88C;
            }
        """)

        central = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLineEdit("Type something..."))
        layout.addWidget(QPushButton("Click Me"))
        list_widget = QListWidget()
        list_widget.addItems(["Item 1", "Item 2", "Item 3"])
        layout.addWidget(list_widget)

        central.setLayout(layout)
        self.setCentralWidget(central)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
