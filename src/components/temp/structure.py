from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.gui.layout_builder import LayoutBuilder
from .blueprint import Blueprint

class Structure(LayoutBuilder, Blueprint):
    """
    how you arrange and decorate the hardware before anyone touches it.
    """

    def __init__(self, component):
        super().__init__()  # just calls UiManager.__init__ with no args | WidgetTypes has no init so dont need it 
        
        self._map_widgets(component)
    
        self.set_widgets()
        self.layout_data = [
            self.form()
            
                
            ]

        self.apply_layout(component, self)


    def set_widgets(self):
        self.label1.setText("Header 1")
        self.label2.setText("Header 2")
        self.label3.setText("Header 3")
        self.label4.setText("Header 4")
        self.label5.setText("Header 5")

        for i, btn in enumerate([self.btn1, self.btn2, self.btn3, self.btn4], 1):
            btn.setText(f"Button {i}")

        for i, lst in enumerate([self.list1, self.list2, self.list3, self.list4], 1):
            lst.addItems([f"Item {j}" for j in range(5)])






