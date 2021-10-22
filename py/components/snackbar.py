from .lib.qtmaterial import *


class QtMaterialSnackbar:
    ...


class QtMaterialSnackbarStateMachine(QStateMachine):
    def __init__(self, parent: QtMaterialSnackbar):
        QStateMachine.__init__(self, parent)

        self.self.m_snackbar = parent
        self.self.m_timer = QTimer()
        self.self.m_offset = qreal()

        self.m_timer.setSingleShot(true)

        hiddenState = QState()
        visibleState = QState()
        finalState = QState()

        self.addState(hiddenState)
        self.addState(visibleState)
        self.addState(finalState)

        self.setInitialState(hiddenState)

        transition = QtMaterialStateTransition(
            QtMaterialStateTransitionType.SnackbarShowTransition
        )
        transition.setTargetState(visibleState)
        hiddenState.addTransition(transition)

        transition = QtMaterialStateTransition(
            QtMaterialStateTransitionType.SnackbarHideTransition
        )
        transition.setTargetState(visibleState)
        hiddenState.addTransition(transition)

        transition = QtMaterialStateTransition(
            QtMaterialStateTransitionType.SnackbarHideTransition
        )
        transition.setTargetState(finalState)
        visibleState.addTransition(transition)

        transition = QtMaterialStateTransition(
            QtMaterialStateTransitionType.SnackbarWaitTransition
        )
        transition.setTargetState(hiddenState)
        finalState.addTransition(transition)

        transition = QtMaterialStateTransition(
            QtMaterialStateTransitionType.SnackbarNextTransition
        )
        transition.setTargetState(visibleState)
        finalState.addTransition(transition)

        visibleState.propertiesAssigned.connect(self.snackbarShown)
        finalState.propertiesAssigned.connect(self.m_snackbar.dequeue)

        animation = QPropertyAnimation(self, "offset", self)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        animation.setDuration(300)
        self.addDefaultAnimation(animation)

        hiddenState.assignProperty(self, "offset", 1)
        visibleState.assignProperty(self, "offset", 0)
        finalState.assignProperty(self, "offset", 1)

        self.m_timer.timeout.connect(self.progress)
        self.m_snackbar.installEventFilter(self)

    def setOffset(self, offset: qreal) -> void:
        self.m_offset = offset
        self.m_snackbar.update()

    def offset(self) -> qreal:
        return self.m_offset

    def progress(self) -> void:
        self.m_timer.stop()
        self.postEvent(
            QtMaterialStateTransitionEvent(
                QtMaterialStateTransitionType.SnackbarHideTransition
            )
        )
        if self.m_snackbar.clickToDismissMode():
            self.m_snackbar.setAttribute(Qt.WA_TransparentForMouseEvents, true)

    def snackbarShown(self) -> void:
        self.m_timer.start(self.m_snackbar.autoHideDuration())
        if self.m_snackbar.clickToDismissMode():
            self.m_snackbar.setAttribute(Qt.WA_TransparentForMouseEvents, false)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if (
            QEvent.MouseButtonPress == event.type()
            and self.m_snackbar.clickToDismissMode()
        ):
            self.progress()

        return QStateMachine.eventFilter(watched, event)


class QtMaterialSnackbarPrivate:
    def __init__(self, q: QtMaterialSnackbar):
        self.q = q
        self.stateMachine = QtMaterialSnackbarStateMachine()
        self.backgroundColor = QColor()
        self.textColor = QColor()
        self.bgOpacity = qreal()
        self.messages = QList()
        self.duration = int()
        self.boxWidth = int()
        self.clickDismiss = bool()
        self.useThemeColors = bool()

    def init(self) -> void:
        self.stateMachine = QtMaterialSnackbarStateMachine(self.q)
        self.bgOpacity = 0.9
        self.duration = 3000
        self.boxWidth = 300
        self.clickDismiss = false
        self.useThemeColors = true

        self.q.setAttribute(Qt.WA_TransparentForMouseEvents)

        font = QFont("Roboto", 10, QFont.Medium)
        font.setCapitalization(QFont.AllUppercase)
        self.q.setFont(font)

        self.stateMachine.start()
        QCoreApplication.processEvents()


class QtMaterialSnackbar(QtMaterialOverlayWidget):
    def __init__(self, parent: QWidget = None):
        QtMaterialOverlayWidget.__init__(self, parent)
        self.d = QtMaterialSnackbarPrivate(self)
        self.d.init()

    def setAutoHideDuration(self, duration: int) -> void:
        self.d.duration = duration

    def autoHideDuration(self) -> int:
        return self.d.duration

    def setUseThemeColors(self, value: bool) -> void:
        if self.d.useThemeColors == value:
            return

        self.d.useThemeColors = value
        self.update()

    def useThemeColors(self) -> bool:
        return self.d.useThemeColors

    def setBackgroundColor(self, color: QColor) -> void:
        self.d.backgroundColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.update()

    def backgroundColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.backgroundColor.isValid():
            return QtMaterialStyle.instance().themeColor("text")
        else:
            return self.d.backgroundColor

    def setBackgroundOpacity(self, opacity: qreal) -> void:
        self.d.bgOpacity = opacity
        self.update()

    def backgroundOpacity(self) -> qreal:
        return self.d.bgOpacity

    def setTextColor(self, color: QColor) -> void:
        self.d.textColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.update()

    def textColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.textColor.isValid():
            return QtMaterialStyle.instance().themeColor("canvas")
        else:
            return self.d.textColor

    def setFontSize(self, size: qreal) -> void:
        f = QFont(self.font())
        f.setPointSizeF(size)
        self.setFont(f)

        self.update()

    def fontSize(self) -> qreal:
        return self.font().pointSizeF()

    def setBoxWidth(self, width: int) -> void:
        self.d.boxWidth = width
        self.update()

    def boxWidth(self) -> int:
        return self.d.boxWidth

    def setClickToDismissMode(self, value: bool) -> void:
        self.d.clickDismiss = value

    def clickToDismissMode(self) -> bool:
        return self.d.clickDismiss

    def addMessage(self, message: QString) -> void:
        self.d.messages.push_back(message)
        self.d.stateMachine.postEvent(
            QtMaterialStateTransitionEvent(
                QtMaterialStateTransitionType.SnackbarShowTransition
            )
        )
        self.raise_()

    def addInstantMessage(self, message: QString) -> void:
        if self.d.messages.isEmpty():
            self.d.messages.push_back(message)
        else:
            self.d.messages.insert(1, message)

        self.d.stateMachine.progress()

    def dequeue(self) -> void:
        if self.d.messages.isEmpty():
            return

        self.d.messages.removeFirst()

        if not self.d.messages.isEmpty():
            self.d.stateMachine.postEvent(
                QtMaterialStateTransitionEvent(
                    QtMaterialStateTransitionType.SnackbarNextTransition
                )
            )
        else:
            self.d.stateMachine.postEvent(
                QtMaterialStateTransitionEvent(
                    QtMaterialStateTransitionType.SnackbarWaitTransition
                )
            )

    def paintEvent(self, event: QPaintEvent) -> void:

        if self.d.messages.isEmpty():
            return

        message: QString = self.d.messages.first()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(self.backgroundColor())
        painter.setBrush(brush)
        painter.setOpacity(self.d.bgOpacity)

        r = QRect(0, 0, self.d.boxWidth, 40)

        painter.setPen(Qt.white)
        br: QRect = painter.boundingRect(
            r, Qt.AlignHCenter | Qt.AlignTop | Qt.TextWordWrap, message
        )

        painter.setPen(Qt.NoPen)
        r = br.united(r).adjusted(-10, -10, 10, 20)

        s: qreal = 1 - self.d.stateMachine.offset()

        painter.translate(
            (self.width() - (r.width() - 20)) / 2, self.height() + 10 - s * (r.height())
        )

        br.moveCenter(r.center())
        painter.drawRoundedRect(r.adjusted(0, 0, 0, 3), 3, 3)
        painter.setPen(self.textColor())
        painter.drawText(br, Qt.AlignHCenter | Qt.AlignTop | Qt.TextWordWrap, message)
