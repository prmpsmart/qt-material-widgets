from .drawer_widget import *
from .drawer_statemachine import *



class QMaterialDrawer(QMaterialOverlayWidget):
    def __init__(self, parent: QWidget = None):
        QMaterialOverlayWidget.__init__(self, parent)

        self.m_widget = QMaterialDrawerWidget()
        self.m_stateMachine = QMaterialDrawerStateMachine(self.m_widget, self)
        self.m_window = QWidget()
        self.m_width = 250
        self.m_clickToClose = False
        self.m_autoRaise = True
        self.m_closed = True
        self.m_overlay = False

        layout = QVBoxLayout()
        layout.addWidget(self.m_window)

        self.m_widget.setLayout(layout)
        self.m_widget.setFixedWidth(self.m_width + 16)

        self.m_widget.setParent(self)

        self.m_stateMachine.start()
        QCoreApplication.processEvents()

    def setDrawerWidth(self, width: int) -> None:
        self.m_width = width
        self.m_stateMachine.updatePropertyAssignments()
        self.m_widget.setFixedWidth(width + 16)

    def drawerWidth(self) -> int:
        return self.m_width

    def setDrawerLayout(self, layout: QLayout) -> None:
        self.m_window.setLayout(layout)

    def drawerLayout(self) -> QLayout:
        return self.m_window.layout()

    def setClickOutsideToClose(self, state: bool) -> None:
        self.m_clickToClose = state

    def clickOutsideToClose(self) -> bool:
        return self.m_clickToClose

    def setAutoRaise(self, state: bool) -> None:
        self.m_autoRaise = state

    def autoRaise(self) -> bool:
        return self.m_autoRaise

    def setOverlayMode(self, value: bool) -> None:
        self.m_overlay = value
        self.update()

    def overlayMode(self) -> bool:
        return self.m_overlay

    def openDrawer(self) -> None:
        self.m_stateMachine.signalOpen.emit()

        if self.m_autoRaise:
            self.raise_()

        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.setAttribute(Qt.WA_NoSystemBackground, False)

    def closeDrawer(self) -> None:
        self.m_stateMachine.signalClose.emit()

        if self.m_overlay:
            self.setAttribute(Qt.WA_TransparentForMouseEvents)
            self.setAttribute(Qt.WA_NoSystemBackground)

    def event(self, event: QEvent) -> bool:
        e = event.type()
        if e in [QEvent.Move, QEvent.Resize]:
            if not self.m_overlay:
                self.setMask(QRegion(self.m_widget.rect()))

        return QMaterialOverlayWidget.event(self, event)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        e = event.type()

        if e == QEvent.MouseButtonPress:
            canClose: bool = self.m_clickToClose or self.m_overlay
            if not self.m_widget.geometry().contains(event.pos()) and canClose:
                self.closeDrawer()
        elif e in [QEvent.Move, QEvent.Resize]:
            lw: QLayout = self.m_widget.layout()
            if lw and 16 != lw.contentsMargins().right():
                lw.setContentsMargins(0, 0, 16, 0)

        return QMaterialOverlayWidget.eventFilter(self, obj, event)

    def paintEvent(self, event: QPaintEvent) -> None:
        if not self.m_overlay or self.m_stateMachine.isInClosedState():
            return
        painter = QPainter(self)
        painter.setOpacity(self.m_stateMachine.opacity())
        painter.fillRect(self.rect(), Qt.SolidPattern)
