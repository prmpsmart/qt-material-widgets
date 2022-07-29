from typing import *
from .presets import *
from .resources import *

from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtUiTools import *
from PySide6.QtStateMachine import *


def MATERIAL_DISABLE_THEME_COLORS(self):
    if self.m_useThemeColors == True:
        self.m_useThemeColors = False


class QMaterialStateTransition(QAbstractTransition):
    def __init__(self, type: QMaterialStateTransitionType):
        QAbstractTransition.__init__(self)
        self.m_type = QMaterialStateTransitionType(type)

    def eventTest(self, event: QEvent) -> bool:
        if event.type() != QEvent.Type(QEvent.User + 1):
            return False

        transition = QMaterialStateTransitionEvent(event)
        return self.m_type == transition.type

    def onTransition(self, event: QEvent) -> None:
        ...
