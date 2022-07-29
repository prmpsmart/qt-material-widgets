from ..core.overlay_widget import *


class QMaterialDialogWindow(QWidget):
    def __init__(self, dialog: "QMaterialDialog", parent: QWidget = None):
        QWidget.__init__(self, parent)

        self.m_dialog = dialog

    def setOffset(self, offset: int) -> None:
        margins: QMargins = self.m_dialog.layout().contentsMargins()
        margins.setBottom(offset)
        self.m_dialog.layout().setContentsMargins(margins)

    def offset(self) -> int:
        return self.m_dialog.layout().contentsMargins().bottom()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(Qt.white)
        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)
        painter.drawRect(self.rect())

    _offset = Property(int, fset=setOffset, fget=offset)


class QMaterialDialog(QMaterialOverlayWidget):

    _showDialog = Signal()
    _hideDialog = Signal()

    def __init__(self, parent: QWidget = None):
        QMaterialOverlayWidget.__init__(self, parent)

        self.m_dialogWindow = QMaterialDialogWindow(self)
        self.m_proxyStack = QStackedLayout()
        self.m_stateMachine = QStateMachine(self)

        from .dialog_proxy import QMaterialDialogProxy

        self.m_proxy = QMaterialDialogProxy(
            self.m_dialogWindow, self.m_proxyStack, self
        )

        layout = QVBoxLayout()
        self.setLayout(layout)

        widget = QWidget()
        widget.setLayout(self.m_proxyStack)
        widget.setMinimumWidth(400)

        effect = QGraphicsDropShadowEffect()
        effect.setColor(QColor(0, 0, 0, 200))
        effect.setBlurRadius(64)
        effect.setOffset(0, 13)
        widget.setGraphicsEffect(effect)

        layout.addWidget(widget)
        layout.setAlignment(widget, Qt.AlignCenter)

        self.m_proxyStack.addWidget(self.m_dialogWindow)
        self.m_proxyStack.addWidget(self.m_proxy)
        self.m_proxyStack.setCurrentIndex(1)

        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        hiddenState = QState()
        visibleState = QState()

        self.m_stateMachine.addState(hiddenState)
        self.m_stateMachine.addState(visibleState)
        self.m_stateMachine.setInitialState(hiddenState)

        transition = QMaterialStateTransition(
            QMaterialStateTransitionType.DialogShowTransition
        )
        transition.setTargetState(visibleState)
        hiddenState.addTransition(transition)

        transition = QMaterialStateTransition(
            QMaterialStateTransitionType.DialogHideTransition
        )
        transition.setTargetState(hiddenState)
        visibleState.addTransition(transition)

        visibleState.assignProperty(self.m_proxy, "opacity", 1)
        visibleState.assignProperty(effect, "color", QColor(0, 0, 0, 200))
        visibleState.assignProperty(self.m_dialogWindow, "offset", 0)
        hiddenState.assignProperty(self.m_proxy, "opacity", 0)
        hiddenState.assignProperty(effect, "color", QColor(0, 0, 0, 0))
        hiddenState.assignProperty(self.m_dialogWindow, "offset", 200)

        animation = QPropertyAnimation(self.m_proxy, b"_opacity", self)
        animation.setDuration(280)
        self.m_stateMachine.addDefaultAnimation(animation)

        animation = QPropertyAnimation(effect, b"color", self)
        animation.setDuration(280)
        self.m_stateMachine.addDefaultAnimation(animation)

        animation = QPropertyAnimation(self.m_dialogWindow, b"_offset", self)
        animation.setDuration(280)
        animation.setEasingCurve(QEasingCurve.OutCirc)
        self.m_stateMachine.addDefaultAnimation(animation)

        visibleState.propertiesAssigned.connect(self.m_proxy.makeOpaque)
        hiddenState.propertiesAssigned.connect(self.m_proxy.makeTransparent)

        self.m_stateMachine.start()
        QCoreApplication.processEvents()

    def windowLayout(self) -> QLayout:
        return self.m_dialogWindow.layout()

    def setWindowLayout(self, layout: QLayout) -> None:
        self.m_dialogWindow.setLayout(layout)

    def showDialog(self) -> None:
        # self.m_stateMachine.postEvent(
        #     QMaterialStateTransitionEvent(
        #         QMaterialStateTransitionType.DialogShowTransition
        #     )
        # )
        self.raise_()

    def hideDialog(self) -> None:
        self.m_stateMachine.postEvent(
            QMaterialStateTransitionEvent(
                QMaterialStateTransitionType.DialogHideTransition
            )
        )
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.m_proxyStack.setCurrentIndex(1)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(Qt.black)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.setOpacity(self.m_proxy.opacity() / 2.4)
        painter.drawRect(self.rect())
