from typing import List, Dict
import enum


from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtUiTools import *
from PySide6.QtStateMachine import *


true = True
false = False

# Qt_Property names are prefixed with "_"
# to avoid conflict with the getter of the properties.
Q_PROPERTY = Property


class QString(str):
    def isEmpty(self) -> bool:
        return self == ""

    def trimmed(self) -> str:
        return self.strip()

    def toLower(self) -> str:
        return self.lower()

    def indexOf(self) -> int:
        return self.index()

    def arg(self, val) -> str:
        return self % val

    number = int


QChar = QString

qreal = float
void = None


class QStringList(list):
    def push_back(self, obj):
        return self.append(obj)

    def count(self):
        return len(self)

    def removeOne(self, one):
        return self.remove(one)

    length = count


QList = QStringList
