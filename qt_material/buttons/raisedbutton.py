from .flatbutton import *


class QMaterialRaisedButton(QMaterialFlatButton):
    def __init__(self, text: str = None, parent: QWidget = None, **kwargs):
        QMaterialFlatButton.__init__(self, text=text, parent=parent, **kwargs)

        self.setText(text)

        self.m_shadowStateMachine = QStateMachine(self)
        self.m_normalState = QState()
        self.m_pressedState = QState()
        self.m_effect = QGraphicsDropShadowEffect()

        self.m_effect.setBlurRadius(7)
        self.m_effect.setOffset(QPointF(0, 2))
        self.m_effect.setColor(QColor(0, 0, 0, 75))

        self.setBackgroundMode(Qt.OpaqueMode)
        self.setMinimumHeight(42)
        self.setGraphicsEffect(self.m_effect)
        self.setBaseOpacity(0.3)

        self.m_shadowStateMachine.addState(self.m_normalState)
        self.m_shadowStateMachine.addState(self.m_pressedState)

        self.m_normalState.assignProperty(self.m_effect, "offset", QPointF(0, 2))
        self.m_normalState.assignProperty(self.m_effect, "blurRadius", 7)

        self.m_pressedState.assignProperty(self.m_effect, "offset", QPointF(0, 5))
        self.m_pressedState.assignProperty(self.m_effect, "blurRadius", 29)

        transition = QEventTransition(self, QEvent.MouseButtonPress)
        transition.setTargetState(self.m_pressedState)
        self.m_normalState.addTransition(transition)

        transition = QEventTransition(self, QEvent.MouseButtonDblClick)
        transition.setTargetState(self.m_pressedState)
        self.m_normalState.addTransition(transition)

        transition = QEventTransition(self, QEvent.MouseButtonRelease)
        transition.setTargetState(self.m_normalState)
        self.m_pressedState.addTransition(transition)

        animation = QPropertyAnimation(self.m_effect, b"offset", self)
        animation.setDuration(100)
        self.m_shadowStateMachine.addDefaultAnimation(animation)

        animation = QPropertyAnimation(self.m_effect, b"blurRadius", self)
        animation.setDuration(100)
        self.m_shadowStateMachine.addDefaultAnimation(animation)

        self.m_shadowStateMachine.setInitialState(self.m_normalState)
        self.m_shadowStateMachine.start()

    def event(self, event: QEvent) -> bool:
        if QEvent.EnabledChange == event.type():
            if self.isEnabled():
                self.m_shadowStateMachine.start()
                self.m_effect.setEnabled(True)
            else:
                self.m_shadowStateMachine.stop()
                self.m_effect.setEnabled(False)

        return QMaterialFlatButton.event(self, event)
