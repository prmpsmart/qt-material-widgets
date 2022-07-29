from ..core._core import *


class QMaterialFlatButtonStateMachine(QStateMachine):
    buttonPressed = Signal()
    buttonChecked = Signal()
    buttonUnchecked = Signal()

    def __init__(self, parent):
        QStateMachine.__init__(self, parent)

        self.m_button = parent
        self.m_topLevelState = QState(QState.ParallelStates)
        self.m_configState = QState(self.m_topLevelState)
        self.m_checkableState = QState(self.m_topLevelState)
        self.m_checkedState = QState(self.m_checkableState)
        self.m_uncheckedState = QState(self.m_checkableState)
        self.m_neutralState = QState(self.m_configState)
        self.m_neutralFocusedState = QState(self.m_configState)
        self.m_hoveredState = QState(self.m_configState)
        self.m_hoveredFocusedState = QState(self.m_configState)
        self.m_pressedState = QState(self.m_configState)
        self.m_haloAnimation = QSequentialAnimationGroup()

        self.m_overlayOpacity = 0
        self.m_checkedOverlayProgress = 1 if parent and parent.isChecked else 0
        self.m_haloOpacity = 0
        self.m_haloSize = 0.8
        self.m_haloScaleFactor = 1
        self.m_wasChecked = False

        if parent:
            parent.installEventFilter(self)

        self.m_configState.setInitialState(self.m_neutralState)
        self.addState(self.m_topLevelState)
        self.setInitialState(self.m_topLevelState)

        self.m_checkableState.setInitialState(
            self.m_checkedState
            if parent and parent.isChecked()
            else self.m_uncheckedState
        )

        transition = QMaterialStateTransition(
            QMaterialStateTransitionType.FlatButtonCheckedTransition
        )
        transition.setTargetState(self.m_checkedState)
        self.m_uncheckedState.addTransition(transition)

        animation = QPropertyAnimation(self, b"_checkedOverlayProgress")
        animation.setDuration(200)
        transition.addAnimation(animation)

        transition = QMaterialStateTransition(
            QMaterialStateTransitionType.FlatButtonUncheckedTransition
        )
        transition.setTargetState(self.m_uncheckedState)
        self.m_checkedState.addTransition(transition)

        animation = QPropertyAnimation(self, b"_checkedOverlayProgress", self)
        animation.setDuration(200)
        transition.addAnimation(animation)

        self.addTransition(
            self.m_button,
            QEvent.FocusIn,
            self.m_neutralState,
            self.m_neutralFocusedState,
        )
        self.addTransition(
            self.m_button,
            QEvent.FocusOut,
            self.m_neutralFocusedState,
            self.m_neutralState,
        )
        self.addTransition(
            self.m_button, QEvent.Enter, self.m_neutralState, self.m_hoveredState
        )
        self.addTransition(
            self.m_button, QEvent.Leave, self.m_hoveredState, self.m_neutralState
        )
        self.addTransition(
            self.m_button,
            QEvent.Enter,
            self.m_neutralFocusedState,
            self.m_hoveredFocusedState,
        )
        self.addTransition(
            self.m_button,
            QEvent.Leave,
            self.m_hoveredFocusedState,
            self.m_neutralFocusedState,
        )
        self.addTransition(
            self.m_button,
            QEvent.FocusIn,
            self.m_hoveredState,
            self.m_hoveredFocusedState,
        )
        self.addTransition(
            self.m_button,
            QEvent.FocusOut,
            self.m_hoveredFocusedState,
            self.m_hoveredState,
        )

        transition = QMaterialStateTransition(
            QMaterialStateTransitionType.FlatButtonPressedTransition
        )
        transition.setTargetState(self.m_pressedState)
        self.m_hoveredState.addTransition(transition)

        self.addTransition(
            self.m_button, QEvent.Leave, self.m_pressedState, self.m_neutralFocusedState
        )
        self.addTransition(
            self.m_button, QEvent.FocusOut, self.m_pressedState, self.m_hoveredState
        )

        self.m_neutralState.assignProperty(self, "_haloSize", 0)
        self.m_neutralFocusedState.assignProperty(self, "_haloSize", 0.7)
        self.m_hoveredState.assignProperty(self, "_haloSize", 0)
        self.m_pressedState.assignProperty(self, "_haloSize", 4)
        self.m_hoveredFocusedState.assignProperty(self, "_haloSize", 0.7)

        grow = QPropertyAnimation(self)
        shrink = QPropertyAnimation(self)

        grow.setTargetObject(self)
        grow.setPropertyName(b"_haloScaleFactor")
        grow.setStartValue(0.56)
        grow.setEndValue(0.63)
        grow.setEasingCurve(QEasingCurve.InOutSine)
        grow.setDuration(840)

        shrink.setTargetObject(self)
        shrink.setPropertyName(b"_haloScaleFactor")
        shrink.setStartValue(0.63)
        shrink.setEndValue(0.56)
        shrink.setEasingCurve(QEasingCurve.InOutSine)
        shrink.setDuration(840)

        self.m_haloAnimation.addAnimation(grow)
        self.m_haloAnimation.addAnimation(shrink)
        self.m_haloAnimation.setLoopCount(-1)

    def setOverlayOpacity(self, opacity: float) -> None:
        self.m_overlayOpacity = opacity
        self.m_button.update()

    def overlayOpacity(self) -> float:
        return self.m_overlayOpacity

    def setCheckedOverlayProgress(self, progress: float) -> None:
        self.m_checkedOverlayProgress = progress
        self.m_button.update()

    def checkedOverlayProgress(self) -> float:
        return self.m_checkedOverlayProgress

    def setHaloOpacity(self, opacity: float) -> None:
        self.m_haloOpacity = opacity
        self.m_button.update()

    def haloOpacity(self) -> float:
        return self.m_haloOpacity

    def setHaloSize(self, size: float) -> None:
        self.m_haloSize = size
        self.m_button.update()

    def haloSize(self) -> float:
        return self.m_haloSize

    def setHaloScaleFactor(self, factor: float) -> None:
        self.m_haloScaleFactor = factor
        self.m_button.update()

    def haloScaleFactor(self) -> float:
        return self.m_haloScaleFactor

    def startAnimations(self) -> None:
        self.m_haloAnimation.start()
        self.start()

    def setupProperties(self) -> None:
        baseOpacity: float = self.m_button.baseOpacity()

        self.m_neutralState.assignProperty(self, "_overlayOpacity", 0)
        self.m_neutralState.assignProperty(self, "_haloOpacity", 0)
        self.m_neutralFocusedState.assignProperty(self, "_overlayOpacity", 0)
        self.m_neutralFocusedState.assignProperty(self, "_haloOpacity", baseOpacity)
        self.m_hoveredState.assignProperty(self, "_overlayOpacity", baseOpacity)
        self.m_hoveredState.assignProperty(self, "_haloOpacity", 0)
        self.m_hoveredFocusedState.assignProperty(self, "_overlayOpacity", baseOpacity)
        self.m_hoveredFocusedState.assignProperty(self, "_haloOpacity", baseOpacity)
        self.m_pressedState.assignProperty(self, "_overlayOpacity", baseOpacity)
        self.m_pressedState.assignProperty(self, "_haloOpacity", 0)
        self.m_checkedState.assignProperty(self, "_checkedOverlayProgress", 1)
        self.m_uncheckedState.assignProperty(self, "_checkedOverlayProgress", 0)

        self.m_button.update()

    def updateCheckedStatus(self) -> None:
        checked: bool = self.m_button.isChecked()
        if self.m_wasChecked != checked:
            self.m_wasChecked = checked
            if checked:
                # this causes the main thread to suddenly exit,
                # I dont know the reason yet..
                self.postEvent(
                    QMaterialStateTransitionEvent(
                        QMaterialStateTransitionType.FlatButtonCheckedTransition
                    )
                )
            else:
                # this causes the main thread to suddenly exit,
                # I dont know the reason yet..
                self.postEvent(
                    QMaterialStateTransitionEvent(
                        QMaterialStateTransitionType.FlatButtonUncheckedTransition
                    )
                )

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if QEvent.FocusIn == event.type():
            focusEvent: QFocusEvent = event
            if Qt.MouseFocusReason == focusEvent.reason():
                ev = QMaterialStateTransitionEvent(
                    QMaterialStateTransitionType.FlatButtonPressedTransition
                )
                # this causes the main thread to suddenly exit,
                # I dont know the reason yet..
                # self.postDelayedEvent(ev, 2)
                ...
            return True
        return QStateMachine.eventFilter(self, watched, event)

    def addTransition(
        self,
        object: QObject = None,
        eventType: QEvent.Type = None,
        fromState: QState = None,
        toState: QState = None,
        # transition: QAbstractTransition = None,
    ) -> None:
        # reordering

        transition = (
            object
            if isinstance(object, QAbstractTransition)
            else QEventTransition(object, eventType)
        )
        if transition == object:
            toState = fromState
            fromState = eventType

        transition.setTargetState(toState)

        animation = QPropertyAnimation(self, b"_overlayOpacity", self)
        animation.setDuration(150)
        transition.addAnimation(animation)

        animation = QPropertyAnimation(self, b"_haloOpacity", self)
        animation.setDuration(170)
        transition.addAnimation(animation)

        animation = QPropertyAnimation(self, b"_haloSize", self)
        animation.setDuration(350)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        transition.addAnimation(animation)

        fromState.addTransition(transition)

    _overlayOpacity = Property(float, fset=setOverlayOpacity, fget=overlayOpacity)
    _checkedOverlayProgress = Property(
        float, fset=setCheckedOverlayProgress, fget=checkedOverlayProgress
    )
    _haloOpacity = Property(float, fset=setHaloOpacity, fget=haloOpacity)
    _haloSize = Property(float, fset=setHaloSize, fget=haloSize)
    _haloScaleFactor = Property(float, fset=setHaloScaleFactor, fget=haloScaleFactor)
