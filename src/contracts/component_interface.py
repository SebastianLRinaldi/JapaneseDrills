from typing import Protocol, List
import collections, re, typing, enum
from .structure_interface import StructureInterface
from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

class ComponentInterface(Protocol):
    structure: StructureInterface    # your existing interface
    logic: object                   # could be a LogicInterface if you define one
    connection: object              # could be a ConnectionsInterface

    def setLayout(self, a0: typing.Optional[QLayout]) -> None: ...