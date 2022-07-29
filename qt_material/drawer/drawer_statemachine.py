from ..core._core import *


class QMaterialDrawerStateMachine(QStateMachine):

    signalOpen = Signal()
    signalClose = Signal()

    def __init__(self, drawer: "QMaterialDrawerWidget", parent: "QMaterialDrawer"):
        QStateMachine.__init__(self, parent)

        self.m_drawer = drawer
        self.m_main = parent
        self.m_openingState = QState()
        self.m_openedState = QState()
        self.m_closingState = QState()
        self.m_closedState = QState()
        self.m_opacity = float(0)

        self.addState(self.m_openingState)
        self.addState(self.m_openedState)
        self.addState(self.m_closingState)
        self.addState(self.m_closedState)

        self.setInitialState(self.m_closedState)

        transition = QSignalTransition(self.signalOpen)
        transition.setTargetState(self.m_openingState)
        self.m_closedState.addTransition(transition)

        animation = QPropertyAnimation(drawer, b"_offset", self)
        animation.setDuration(220)
        animation.setEasingCurve(QEasingCurve.OutCirc)
        transition.addAnimation(animation)

        animation = QPropertyAnimation(self, b"_opacity")
        animation.setDuration(220)
        transition.addAnimation(animation)

        transition = QSignalTransition(self.finished)
        transition.setTargetState(self.m_openedState)
        self.m_openingState.addTransition(transition)

        transition = QSignalTransition(self.signalClose)
        transition.setTargetState(self.m_closingState)
        self.m_openingState.addTransition(transition)

        animation = QPropertyAnimation(self, b"_opacity")
        animation.setDuration(220)
        transition.addAnimation(animation)

        animation = QPropertyAnimation(drawer, b"_offset")
        animation.setDuration(220)
        animation.setEasingCurve(QEasingCurve.InCirc)
        transition.addAnimation(animation)

        transition = QSignalTransition(self.finished)
        transition.setTargetState(self.m_closedState)
        self.m_closingState.addTransition(transition)

        transition = QSignalTransition(self.signalClose)
        transition.setTargetState(self.m_closingState)
        self.m_openedState.addTransition(transition)

        animation = QPropertyAnimation(drawer, b"_offset", self)
        animation.setDuration(220)
        animation.setEasingCurve(QEasingCurve.InCirc)
        transition.addAnimation(animation)

        animation = QPropertyAnimation(self, b"_opacity", self)
        animation.setDuration(220)
        transition.addAnimation(animation)

        transition = QSignalTransition(self.finished)
        transition.setTargetState(self.m_closedState)
        self.m_closingState.addTransition(transition)

        self.updatePropertyAssignments()

    def setOpacity(self, opacity: float) -> None:
        self.m_opacity = opacity
        self.m_main.update()

    def opacity(self) -> float:
        return self.m_opacity

    def isInClosedState(self) -> bool:
        return self.m_closedState.active()

    def updatePropertyAssignments(self) -> None:
        closedOffset: float = -(self.m_drawer.width() + 32)

        self.m_closingState.assignProperty(self.m_drawer, "_offset", closedOffset)
        self.m_closedState.assignProperty(self.m_drawer, "_offset", closedOffset)

        self.m_closingState.assignProperty(self, "_opacity", 0)
        self.m_closedState.assignProperty(self, "_opacity", 0)

        self.m_openingState.assignProperty(self.m_drawer, "_offset", 0)
        self.m_openingState.assignProperty(self, "_opacity", 0.4)

    _opacity = Property(float, fset=setOpacity, fget=opacity)

