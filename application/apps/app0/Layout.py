from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from application.FrontEnd.C_Grouper.SpliterGroupConfiguration import *
from application.FrontEnd.C_Grouper.TabGroupConfigureation import *
from application.FrontEnd.C_Grouper.widgetGroupFrameworks import *

from application.FrontEnd.D_WindowFolder.windowConfigureation import *

# from .widgets.CUSTOMWIDGET import YOURWIDGET



"""
When you press enter after you type it should either go to the category selection or the next text box below
"""
class Layout(LayoutManager):
    def __init__(self):
        super().__init__()