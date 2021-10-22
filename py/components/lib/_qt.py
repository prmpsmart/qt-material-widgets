from typing import List, Dict
import enum


from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtUiTools import *
from PySide6.QtStateMachine import *


true = True
false = False

Q_PROPERTY = Property


class QString(str):
    def trimmed(self):
        return self.strip()

    def toLower(self):
        return self.lower()

    def indexOf(self):
        return self.index()

    def arg(self, val):
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
