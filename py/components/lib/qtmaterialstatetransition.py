from enum import Enum
from PySide6.QtCore import QEvent
from PySide6.QtWidgets import QWidget
from PySide6.QtStateMachine import QAbstractTransition


void = None
false = False


class QtMaterialStateTransitionType(Enum):
    # Snackbar
    SnackbarShowTransition = 1
    SnackbarHideTransition = 2
    SnackbarWaitTransition = 3
    SnackbarNextTransition = 4
    # FlatButton
    FlatButtonPressedTransition = 5
    FlatButtonCheckedTransition = 6
    FlatButtonUncheckedTransition = 7
    # CollapsibleMenu
    CollapsibleMenuExpand = 8
    CollapsibleMenuCollapse = 9
    # Slider
    SliderChangedToMinimum = 10
    SliderChangedFromMinimum = 11
    SliderNoFocusMouseEnter = 12
    SliderNoFocusMouseLeave = 13
    # Dialog
    DialogShowTransition = 14
    DialogHideTransition = 15
    #
    MaxTransitionType = 65535


class QtMaterialStateTransitionEvent(QEvent):
    def __init__(self, type: QtMaterialStateTransitionType):

        QEvent.__init__(self, QEvent.Type(QEvent.User + 1))
        self.type: QtMaterialStateTransitionType = type


class QtMaterialStateTransition(QAbstractTransition):
    def __init__(self, type: QtMaterialStateTransitionType):
        self.m_type: QtMaterialStateTransitionType = type

    def eventTest(self, event: QEvent) -> bool:
        if event.type() != QEvent.Type(QEvent.User + 1):
            return false

        transition: QtMaterialStateTransitionEvent = event
        return self.m_type == transition.type

    def onTransition(self, event: QEvent) -> void:
        ...
