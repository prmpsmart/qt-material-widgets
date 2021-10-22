from .lib.qtmaterial import *


class QtMaterialDialog: ...
class QtMaterialDialogWindow: ...


class QtMaterialDialogProxy(QWidget):

    class TransparencyMode(enum.Enum):
        Transparent = enum.auto()
        SemiTransparent = enum.auto()
        Opaque = enum.auto()
    Transparent = TransparencyMode.Transparent
    SemiTransparent = TransparencyMode.SemiTransparent
    Opaque = TransparencyMode.Opaque

    def __init__(self, source: QtMaterialDialogWindow, layout: QStackedLayout, dialog: QtMaterialDialog, parent: QWidget=None):
        QWidget.__init__(self, parent)

        self.m_source = source
        self.m_layout = layout
        self.m_dialog = dialog
        self.m_opacity = qreal()
        self.m_mode = self.Transparent

    def setOpacity(self, opacity: qreal) -> void:
        self.m_opacity = opacity
        self.m_mode = self.SemiTransparent
        self.update()
        self.m_dialog.update()

    def opacity(self) -> qreal:
        return self.m_opacity

    def makeOpaque(self) -> void:
        self.m_dialog.setAttribute(Qt.WA_TransparentForMouseEvents, false)
        self.m_layout.setCurrentIndex(0)
        self.m_opacity = 1.0
        self.m_mode = self.Opaque
        self.update()

    def makeTransparent(self) -> void:
        self.m_opacity = 0.0
        self.m_mode = self.Transparent
        self.update()

    def sizeHint(self) -> QSize:
        return self.m_source.sizeHint()

    def event(self, event: QEvent) -> bool:
        type: QEvent.Type = event.type()

        if (QEvent.Move == type or QEvent.Resize == type):
            self.m_source.setGeometry(self.geometry())

        return QWidget.event(self, event)

    def paintEvent(self, event: QPaintEvent) -> void:
        painter = QPainter(self)

        if (self.Transparent == self.m_mode):
            return
        elif (self.Opaque != self.m_mode):
            painter.setOpacity(self.m_opacity)
        
        pm: QPixmap = self.m_source.grab(self.m_source.rect())
        painter.drawPixmap(0, 0, pm)


class QtMaterialDialogWindow(QWidget):

    def __init__(self, dialog: QtMaterialDialog, parent: QWidget=None):
        QWidget.__init__(self, parent)

        self.m_dialog = dialog

    def setOffset(self, offset: int) -> void:
        margins: QMargins = self.m_dialog.layout().contentsMargins()
        margins.setBottom(offset)
        self.m_dialog.layout().setContentsMargins(margins)

    def offset(self) -> int:
        return self.m_dialog.layout().contentsMargins().bottom()

    def paintEvent(self, event: QPaintEvent) -> void:
        painter = QPainter(self)

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(Qt.white)
        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)
        painter.drawRect(self.rect())


class QtMaterialDialogPrivate:

    def __init__(self, q: QtMaterialDialog):

        self.q = q
        self.dialogWindow = QtMaterialDialogWindow()
        self.proxyStack = QStackedLayout()
        self.stateMachine = QStateMachine()
        self.proxy = QtMaterialDialogProxy()

    def init(self) -> void:
        q = self.q

        self.dialogWindow = QtMaterialDialogWindow(q)
        self.proxyStack   = QStackedLayout()
        self.stateMachine = QStateMachine(q)
        self.proxy        = QtMaterialDialogProxy(self.dialogWindow, self.proxyStack, q)

        layout = QVBoxLayout()
        self.q.setLayout(layout)

        widget = QWidget()
        widget.setLayout(self.proxyStack)
        widget.setMinimumWidth(400)

        effect = QGraphicsDropShadowEffect()
        effect.setColor(QColor(0, 0, 0, 200))
        effect.setBlurRadius(64)
        effect.setOffset(0, 13)
        widget.setGraphicsEffect(effect)

        layout.addWidget(widget)
        layout.setAlignment(widget, Qt.AlignCenter)

        self.proxyStack.addWidget(self.dialogWindow)
        self.proxyStack.addWidget(self.proxy)
        self.proxyStack.setCurrentIndex(1)

        self.q.setAttribute(Qt.WA_TransparentForMouseEvents)

        hiddenState = QState()
        visibleState = QState()

        self.stateMachine.addState(hiddenState)
        self.stateMachine.addState(visibleState)
        self.stateMachine.setInitialState(hiddenState)

        transition = QtMaterialStateTransition(QtMaterialStateTransitionType.DialogShowTransition)
        transition.setTargetState(visibleState)
        hiddenState.addTransition(transition)

        transition = QtMaterialStateTransition(QtMaterialStateTransitionType.DialogHideTransition)
        transition.setTargetState(hiddenState)
        visibleState.addTransition(transition)

        visibleState.assignProperty(self.proxy, "opacity", 1)
        visibleState.assignProperty(effect, "color", QColor(0, 0, 0, 200))
        visibleState.assignProperty(self.dialogWindow, "offset", 0)
        hiddenState.assignProperty(self.proxy, "opacity", 0)
        hiddenState.assignProperty(effect, "color", QColor(0, 0, 0, 0))
        hiddenState.assignProperty(self.dialogWindow, "offset", 200)

        animation = QPropertyAnimation()

        animation = QPropertyAnimation(self.proxy, "opacity", q)
        animation.setDuration(280)
        self.stateMachine.addDefaultAnimation(animation)

        animation = QPropertyAnimation(effect, "color", q)
        animation.setDuration(280)
        self.dialogWindowstateMachine.addDefaultAnimation(animation)

        animation = QPropertyAnimation(self.dialogWindow, "offset", q)
        animation.setDuration(280)
        animation.setEasingCurve(QEasingCurve.OutCirc)
        self.stateMachine.addDefaultAnimation(animation)

        QObject.connect(visibleState, SIGNAL(self.propertiesAssigned()),
                        self.proxy, SLOT(self.makeOpaque()))
        QObject.connect(hiddenState, SIGNAL(self.propertiesAssigned()),
                        self.proxy, SLOT(self.makeTransparent()))

        self.stateMachine.start()
        QCoreApplication.processEvents()


class QtMaterialDialog(QtMaterialOverlayWidget):

    showDialog = Signal()
    hideDialog = Signal()

    def __init__(self, parent: QWidget=None):
        QtMaterialOverlayWidget.__init__(self, parent)
        
        self.d = QtMaterialDialogPrivate(self)
        self.d.init()

    def windowLayout(self) -> QLayout:
        return self.d.dialogWindow.layout()

    def setWindowLayout(self, layout: QLayout) -> void:
        self.d.dialogWindow.setLayout(layout)

    def showDialog(self) -> void:
        self.d.stateMachine.postEvent(QtMaterialStateTransitionEvent(QtMaterialStateTransitionType.DialogShowTransition))
        self.raise_()

    def hideDialog(self) -> void:

        self.d.stateMachine.postEvent(QtMaterialStateTransitionEvent(QtMaterialStateTransitionType.DialogHideTransition))
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.d.proxyStack.setCurrentIndex(1)

    def paintEvent(self, event: QPaintEvent) -> void:
        painter = QPainter(self)

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(Qt.black)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.setOpacity(self.d.proxy.opacity()/2.4)
        painter.drawRect(self.rect())


