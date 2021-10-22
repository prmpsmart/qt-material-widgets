from .lib.qtmaterial import *


class QtMaterialDrawer:
    ...


class QtMaterialDrawerWidget:
    ...


class QtMaterialDrawerStateMachine(QStateMachine):

    signalOpen = Signal()
    signalClose = Signal()

    def __init__(self, drawer: QtMaterialDrawerWidget, parent: QtMaterialDrawer):
        QStateMachine.__init__(self, parent)

        self.m_drawer = drawer
        self.m_main = parent
        self.m_openingState = QState()
        self.m_openedState = QState()
        self.m_closingState = QState()
        self.m_closedState = QState()
        self.m_opacity = qreal(0)

        self.addState(self.m_openingState)
        self.addState(self.m_openedState)
        self.addState(self.m_closingState)
        self.addState(self.m_closedState)

        self.setInitialState(self.m_closedState)

        transition = QSignalTransition(self.signalOpen)
        transition.setTargetState(self.m_openingState)
        self.m_closedState.addTransition(transition)

        animation = QPropertyAnimation(drawer, b"offset", self)
        animation.setDuration(220)
        animation.setEasingCurve(QEasingCurve.OutCirc)
        transition.addAnimation(animation)

        animation = QPropertyAnimation(self, b"opacity")
        animation.setDuration(220)
        transition.addAnimation(animation)

        transition = QSignalTransition(self.finished)
        transition.setTargetState(self.m_openedState)
        self.m_openingState.addTransition(transition)

        transition = QSignalTransition(self.signalClose)
        transition.setTargetState(self.m_closingState)
        self.m_openingState.addTransition(transition)

        animation = QPropertyAnimation(self, b"opacity")
        animation.setDuration(220)
        transition.addAnimation(animation)

        animation = QPropertyAnimation(drawer, b"offset")
        animation.setDuration(220)
        animation.setEasingCurve(QEasingCurve.InCirc)
        transition.addAnimation(animation)

        transition = QSignalTransition(self.finished)
        transition.setTargetState(self.m_closedState)
        self.m_closingState.addTransition(transition)

        transition = QSignalTransition(self.signalClose)
        transition.setTargetState(self.m_closingState)
        self.m_openedState.addTransition(transition)

        animation = QPropertyAnimation(drawer, b"offset", self)
        animation.setDuration(220)
        animation.setEasingCurve(QEasingCurve.InCirc)
        transition.addAnimation(animation)

        animation = QPropertyAnimation(self, b"opacity", self)
        animation.setDuration(220)
        transition.addAnimation(animation)

        transition = QSignalTransition(self.finished)
        transition.setTargetState(self.m_closedState)
        self.m_closingState.addTransition(transition)

        self.updatePropertyAssignments()

    def setOpacity(self, opacity: qreal) -> void:
        self.m_opacity = opacity
        self.m_main.update()

    def opacity(self) -> qreal:
        return self.m_opacity

    opacity = Property(qreal, opacity, setOpacity)

    def isInClosedState(self) -> bool:
        return self.m_closedState.active()

    def updatePropertyAssignments(self) -> void:
        closedOffset: qreal = -(self.m_drawer.width() + 32)

        self.m_closingState.assignProperty(self.m_drawer, "offset", closedOffset)
        self.m_closedState.assignProperty(self.m_drawer, "offset", closedOffset)

        self.m_closingState.assignProperty(self, "opacity", 0)
        self.m_closedState.assignProperty(self, "opacity", 0)

        self.m_openingState.assignProperty(self.m_drawer, "offset", 0)
        self.m_openingState.assignProperty(self, "opacity", 0.4)

    opacity = Q_PROPERTY(qreal, fset=setOpacity, fget=opacity)


class QtMaterialDrawerWidget(QtMaterialOverlayWidget):
    def __init__(self, parent: QWidget = None):
        QtMaterialOverlayWidget.__init__(self, parent)

        self.m_offset = int(0)

    def setOffset(self, offset: int) -> void:
        self.m_offset = offset

        widget: QWidget = self.parentWidget()
        if widget:
            self.setGeometry(widget.rect().translated(offset, 0))
        self.update()

    def offset(self) -> int:
        return self.m_offset

    offset = Property(int, offset, setOffset)

    def paintEvent(self, event: QPaintEvent) -> void:
        painter = QPainter(self)

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(Qt.white)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)

        painter.drawRect(self.rect().adjusted(0, 0, -16, 0))

        gradient = QLinearGradient(
            QPointF(self.width() - 16, 0), QPointF(self.width(), 0)
        )
        gradient.setColorAt(0, QColor(0, 0, 0, 80))
        gradient.setColorAt(0.5, QColor(0, 0, 0, 20))
        gradient.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(gradient))

        painter.drawRect(self.width() - 16, 0, 16, self.height())

    def overlayGeometry(self) -> QRect:
        return QtMaterialOverlayWidget.overlayGeometry(self).translated(
            self.m_offset, 0
        )

    offset = Q_PROPERTY(int, fset=setOffset, fget=offset)


class QtMaterialDrawerPrivate:
    def __init__(self, q: QtMaterialDrawer) -> None:
        self.q = q

    def init(self) -> void:
        self.widget = QtMaterialDrawerWidget()
        self.stateMachine = QtMaterialDrawerStateMachine(self.widget, self.q)
        self.window = QWidget()
        self.width = 250
        self.clickToClose = false
        self.autoRaise = true
        self.closed = true
        self.overlay = false

        layout = QVBoxLayout()
        layout.addWidget(self.window)

        self.widget.setLayout(layout)
        self.widget.setFixedWidth(self.width + 16)

        self.widget.setParent(self.q)

        self.stateMachine.start()
        QCoreApplication.processEvents()

    def setClosed(self, value: bool = true) -> void:
        ...


class QtMaterialDrawer(QtMaterialOverlayWidget):
    def __init__(self, parent: QWidget = None):
        QtMaterialOverlayWidget.__init__(self, parent)

        self.d = QtMaterialDrawerPrivate(self)
        self.d.init()

    def setDrawerWidth(self, width: int) -> void:
        self.d.width = width
        self.d.stateMachine.updatePropertyAssignments()
        self.d.widget.setFixedWidth(width + 16)

    def drawerWidth(self) -> int:
        return self.d.width

    def setDrawerLayout(self, layout: QLayout) -> void:
        self.d.window.setLayout(layout)

    def drawerLayout(self) -> QLayout:
        return self.d.window.layout()

    def setClickOutsideToClose(self, state: bool) -> void:
        self.d.clickToClose = state

    def clickOutsideToClose(self) -> bool:
        return self.d.clickToClose

    def setAutoRaise(self, state: bool) -> void:
        self.d.autoRaise = state

    def autoRaise(self) -> bool:
        return self.d.autoRaise

    def setOverlayMode(self, value: bool) -> void:
        self.d.overlay = value
        self.update()

    def overlayMode(self) -> bool:
        return self.d.overlay

    def openDrawer(self) -> void:
        self.d.stateMachine.signalOpen.emit()

        if self.d.autoRaise:
            self.raise_()

        self.setAttribute(Qt.WA_TransparentForMouseEvents, false)
        self.setAttribute(Qt.WA_NoSystemBackground, false)

    def closeDrawer(self) -> void:
        self.d.stateMachine.signalClose.emit()

        if self.d.overlay:
            self.setAttribute(Qt.WA_TransparentForMouseEvents)
            self.setAttribute(Qt.WA_NoSystemBackground)

    def event(self, event: QEvent) -> bool:
        e = event.type()
        if e in [QEvent.Move, QEvent.Resize]:
            if not self.d.overlay:
                self.setMask(QRegion(self.d.widget.rect()))

        return QtMaterialOverlayWidget.event(self, event)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        e = event.type()

        if e == QEvent.MouseButtonPress:
            canClose: bool = self.d.clickToClose or self.d.overlay
            if not self.d.widget.geometry().contains(event.pos()) and canClose:
                self.closeDrawer()
        elif e in [QEvent.Move, QEvent.Resize]:
            lw: QLayout = self.d.widget.layout()
            if lw and 16 != lw.contentsMargins().right():
                lw.setContentsMargins(0, 0, 16, 0)

        return QtMaterialOverlayWidget.eventFilter(self, obj, event)

    def paintEvent(self, event: QPaintEvent) -> void:
        if not self.d.overlay or self.d.stateMachine.isInClosedState():
            return
        painter = QPainter(self)
        painter.setOpacity(self.d.stateMachine.opacity)
        painter.fillRect(self.rect(), Qt.SolidPattern)
