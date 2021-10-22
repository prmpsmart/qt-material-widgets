from .flatbutton import *


class QtMaterialRaisedButton:
    ...


class QtMaterialRaisedButtonPrivate(QtMaterialFlatButtonPrivate):
    def __init__(self, q: QtMaterialRaisedButton):
        QtMaterialFlatButtonPrivate.__init__(self, q)

        self.shadowStateMachine: QStateMachine = None
        self.normalState: QState = None
        self.pressedState: QState = None
        self.effect: QGraphicsDropShadowEffect = None

    def init(self) -> void:
        self.shadowStateMachine = QStateMachine(self.q)
        self.normalState = QState()
        self.pressedState = QState()
        self.effect = QGraphicsDropShadowEffect()

        self.effect.setBlurRadius(7)
        self.effect.setOffset(QPointF(0, 2))
        self.effect.setColor(QColor(0, 0, 0, 75))

        self.q.setBackgroundMode(Qt.OpaqueMode)
        self.q.setMinimumHeight(42)
        self.q.setGraphicsEffect(self.effect)
        self.q.setBaseOpacity(0.3)

        self.shadowStateMachine.addState(self.normalState)
        self.shadowStateMachine.addState(self.pressedState)

        self.normalState.assignProperty(self.effect, "offset", QPointF(0, 2))
        self.normalState.assignProperty(self.effect, "blurRadius", 7)

        self.pressedState.assignProperty(self.effect, "offset", QPointF(0, 5))
        self.pressedState.assignProperty(self.effect, "blurRadius", 29)

        transition = QEventTransition(self.q, QEvent.MouseButtonPress)
        transition.setTargetState(self.pressedState)
        self.normalState.addTransition(transition)

        transition = QEventTransition(self.q, QEvent.MouseButtonDblClick)
        transition.setTargetState(self.pressedState)
        self.normalState.addTransition(transition)

        transition = QEventTransition(self.q, QEvent.MouseButtonRelease)
        transition.setTargetState(self.normalState)
        self.pressedState.addTransition(transition)

        animation = QPropertyAnimation(self.effect, "offset", self.q)
        animation.setDuration(100)
        self.shadowStateMachine.addDefaultAnimation(animation)

        animation = QPropertyAnimation(self.effect, "blurRadius", self.q)
        animation.setDuration(100)
        self.shadowStateMachine.addDefaultAnimation(animation)

        self.shadowStateMachine.setInitialState(self.normalState)
        self.shadowStateMachine.start()


class QtMaterialRaisedButton(QtMaterialFlatButton):
    def __init__(
        self,
        text: QString = None,
        parent: QWidget = None,
        d: QtMaterialFlatButtonPrivate = None,
    ):
        QtMaterialFlatButton.__init__(self, text=text, parent=parent, d=d)

        self.d = d or QtMaterialFlatButtonPrivate(q=self)
        self.setText(text)
        self.d.init()

    def event(self, event: QEvent) -> bool:
        if QEvent.EnabledChange == event.type():
            if self.isEnabled():
                self.d.shadowStateMachine.start()
                self.d.effect.setEnabled(true)
            else:
                self.d.shadowStateMachine.stop()
                self.d.effect.setEnabled(false)

        return QtMaterialFlatButton.event(self, event)
