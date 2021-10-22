from .lib.qtmaterial import *


class QtMaterialToggle:
    ...


class QtMaterialToggleThumb(QWidget):
    def __init__(self, parent: QtMaterialToggle):
        QWidget.__init__(self, parent)

        self.m_toggle = parent
        self.m_thumbColor = QColor()
        self.m_shift = qreal(0)
        self.m_offset = qreal(0)

        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(6)
        effect.setColor(QColor(0, 0, 0, 80))
        effect.setOffset(QPointF(0, 1))
        self.setGraphicsEffect(effect)

        parent.installEventFilter(self)

    def setShift(self, shift: qreal) -> void:
        if self.m_shift == shift:
            return

        self.m_shift = shift
        self.updateOffset()

    def shift(self) -> qreal:
        return self.m_shift

    def offset(self) -> qreal:
        return self.m_offset

    def setThumbColor(self, color: QColor) -> void:
        self.m_thumbColor = color
        self.update()

    def thumbColor(self) -> QColor:
        return self.m_thumbColor

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        type: QEvent.Type = event.type()

        if QEvent.Resize == type or QEvent.Move == type:
            self.setGeometry(self.m_toggle.rect().adjusted(8, 8, -8, -8))
            self.updateOffset()

        return QWidget.eventFilter(self, obj, event)

    def paintEvent(self, event: QPaintEvent) -> void:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(self.m_thumbColor if self.m_toggle.isEnabled() else Qt.white)

        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)

        if Qt.Horizontal == self.m_toggle.orientation():
            s: int = self.height() - 10
            r: QRectF = QRectF(5 + self.m_offset, 5, s, s)
        else:
            s: int = self.width() - 10
            r: QRectF = QRectF(5, 5 + self.m_offset, s, s)

        painter.drawEllipse(r)

        if not self.m_toggle.isEnabled():
            brush.setColor(self.m_toggle.disabledColor())
            painter.setBrush(brush)
            painter.drawEllipse(r)

    def updateOffset(self) -> void:
        s = QSize(
            self.size()
            if Qt.Horizontal == self.m_toggle.orientation()
            else self.size().transposed()
        )
        self.m_offset = self.m_shift * s.width() - s.height()
        self.update()

    shift = Q_PROPERTY(qreal, fset=setShift, fget=shift)
    thumbColor = Q_PROPERTY(QColor, fset=setThumbColor, fget=thumbColor)


class QtMaterialToggleTrack(QWidget):
    def __init__(self, parent: QtMaterialToggle):
        QWidget.__init__(self, parent)
        self.m_toggle = parent
        self.m_trackColor = QColor()

        parent.installEventFilter(self)

    def setTrackColor(self, color: QColor) -> void:
        self.m_trackColor = color
        self.update()

    def trackColor(self) -> QColor:
        return self.m_trackColor

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        type: QEvent.Type = event.type()

        if QEvent.Resize == type or QEvent.Move == type:
            self.setGeometry(self.m_toggle.rect())

        return QWidget.eventFilter(self, obj, event)

    def paintEvent(self, event: QPaintEvent) -> void:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        brush = QBrush()
        if self.m_toggle.isEnabled():
            brush.setColor(self.m_trackColor)
            painter.setOpacity(0.8)
        else:
            brush.setColor(self.m_toggle.disabledColor())
            painter.setOpacity(0.6)

        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)

        if Qt.Horizontal == self.m_toggle.orientation():
            h: int = self.height() / 2
            r = QRect(0, h / 2, self.width(), h)
            painter.drawRoundedRect(r.adjusted(14, 4, -14, -4), h / 2 - 4, h / 2 - 4)
        else:
            w: int = self.width() / 2
            r = QRect(w / 2, 0, w, self.height())
            painter.drawRoundedRect(r.adjusted(4, 14, -4, -14), w / 2 - 4, w / 2 - 4)

    trackColor = Q_PROPERTY(QColor, fset=setTrackColor, fget=trackColor)


class QtMaterialToggleRippleOverlay(QtMaterialRippleOverlay):
    def __init__(
        self,
        thumb: QtMaterialToggleThumb,
        track: QtMaterialToggleTrack,
        parent: QtMaterialToggle,
    ):
        QtMaterialRippleOverlay.__init__(self, parent)

        self.m_toggle = parent
        self.m_thumb = thumb
        self.m_track = track

        parent.toggled.connect(self.addToggleRipple)

        thumb.installEventFilter(self)

    def addToggleRipple(self) -> void:
        if not self.m_toggle.isEnabled():
            return

        if Qt.Horizontal == self.m_toggle.orientation():
            t: int = self.m_toggle.height() / 2
            w: int = self.m_thumb.height() / 2 + 10
        else:
            t: int = self.m_toggle.width() / 2
            w: int = self.m_thumb.width() / 2 + 10

        ripple = QtMaterialRipple(QPoint(10 + t, 20 + t))
        ripple.setColor(self.m_track.trackColor())
        ripple.setRadiusEndValue(w)
        ripple.setOpacityStartValue(0.8)

        self.addRipple(ripple)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if QEvent.Paint == event.type():
            self.setGeometry(self.overlayGeometry())

            items: List[QtMaterialRipple] = self.ripples()

            color: QColor = self.m_track.trackColor()
            for i in items:
                i.setColor(color)

        return QtMaterialRippleOverlay.eventFilter(self, obj, event)

    def overlayGeometry(self) -> QRect:
        offset: qreal = self.m_thumb.offset()
        if Qt.Horizontal == self.m_toggle.orientation():
            return self.m_toggle.geometry().adjusted(-10 + offset, -20, 10 + offset, 20)
        else:
            return self.m_toggle.geometry().adjusted(-10, -20 + offset, 10, 20 + offset)


class QtMaterialTogglePrivate:
    def __init__(self, q: QtMaterialToggle):
        self.q: QtMaterialToggle = q
        self.track: QtMaterialToggleTrack = None
        self.thumb: QtMaterialToggleThumb = None
        self.rippleOverlay: QtMaterialToggleRippleOverlay = None
        self.stateMachine: QStateMachine = None
        self.offState: QState = None
        self.onState: QState = None
        self.orientation: Qt = None
        self.disabledColor: QColor = QColor()
        self.activeColor: QColor = QColor()
        self.inactiveColor: QColor = QColor()
        self.trackColor: QColor = QColor()
        self.useThemeColors: bool = None

    def init(self) -> void:
        self.track = QtMaterialToggleTrack(self.q)
        self.thumb = QtMaterialToggleThumb(self.q)
        self.rippleOverlay = QtMaterialToggleRippleOverlay(
            self.thumb, self.track, self.q
        )
        self.stateMachine = QStateMachine(self.q)
        self.offState = QState()
        self.onState = QState()
        self.orientation = Qt.Horizontal
        self.useThemeColors = true

        self.q.setCheckable(true)
        self.q.setChecked(false)
        self.q.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.stateMachine.addState(self.offState)
        self.stateMachine.addState(self.onState)
        self.stateMachine.setInitialState(self.offState)

        self.offState.assignProperty(self.thumb, "shift", 0)
        self.onState.assignProperty(self.thumb, "shift", 1)

        transition = QSignalTransition(self.q.toggled)
        transition.setTargetState(self.onState)
        self.offState.addTransition(transition)

        animation = QPropertyAnimation(self.q)
        animation.setPropertyName(b"shift")
        animation.setTargetObject(self.thumb)
        animation.setDuration(200)
        animation.setEasingCurve(QEasingCurve.OutQuad)
        transition.addAnimation(animation)
        print(self.thumb.dynamicPropertyNames())

        animation = QPropertyAnimation(self.q)
        animation.setPropertyName(b"trackColor")
        animation.setTargetObject(self.track)
        animation.setDuration(150)
        transition.addAnimation(animation)

        animation = QPropertyAnimation(self.q)
        animation.setPropertyName(b"thumbColor")
        animation.setTargetObject(self.thumb)
        animation.setDuration(150)
        transition.addAnimation(animation)

        self.setupProperties()

        self.stateMachine.start()
        QCoreApplication.processEvents()

    def setupProperties(self) -> void:
        if self.q.isEnabled():
            shift: qreal = self.thumb.shift()
            if qFuzzyCompare(shift, 1):
                self.thumb.setThumbColor(self.q.activeColor())
                self.track.setTrackColor(self.q.activeColor().lighter(110))
            elif qFuzzyCompare(1 + shift, 1):
                self.thumb.setThumbColor(self.q.inactiveColor())
                self.track.setTrackColor(self.q.trackColor())

        self.offState.assignProperty(
            self.track, "trackColor", self.q.trackColor().lighter(110)
        )
        self.onState.assignProperty(
            self.track, "trackColor", self.q.activeColor().lighter(110)
        )

        self.offState.assignProperty(self.thumb, "thumbColor", self.q.inactiveColor())
        self.onState.assignProperty(self.thumb, "thumbColor", self.q.activeColor())

        self.q.update()


class QtMaterialToggle(QAbstractButton):
    def __init__(self, parent: QWidget = None):
        QAbstractButton.__init__(self, parent)
        self.d = QtMaterialTogglePrivate(self)
        self.d.init()

    def setUseThemeColors(self, value: bool) -> void:
        self.d.useThemeColors = value
        self.d.setupProperties()

    def useThemeColors(self) -> bool:
        return self.d.useThemeColors

    def setDisabledColor(self, color: QColor) -> void:
        self.d.disabledColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.d.setupProperties()

    def disabledColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.disabledColor.isValid():
            return QtMaterialStyle.instance().themeColor("disabled")
        else:
            return self.d.disabledColor

    def setActiveColor(self, color: QColor) -> void:
        self.d.activeColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.d.setupProperties()

    def activeColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.activeColor.isValid():
            return QtMaterialStyle.instance().themeColor("primary1")
        else:
            return self.d.activeColor

    def setInactiveColor(self, color: QColor) -> void:
        self.d.inactiveColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.d.setupProperties()

    def inactiveColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.inactiveColor.isValid():
            return QtMaterialStyle.instance().themeColor("canvas")
        else:
            return self.d.inactiveColor

    def setTrackColor(self, color: QColor) -> void:
        self.d.trackColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.d.setupProperties()

    def trackColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.trackColor.isValid():
            return QtMaterialStyle.instance().themeColor("accent3")
        else:
            return self.d.trackColor

    def setOrientation(self, orientation: Qt.Orientation) -> void:
        if self.d.orientation == orientation:
            return

        self.d.orientation = orientation
        self.updateGeometry()

    def orientation(self) -> Qt.Orientation:
        return self.d.orientation

    def sizeHint(self) -> QSize:
        return QSize(64, 48) if Qt.Horizontal == self.d.orientation else QSize(48, 64)

    def event(self, event: QEvent) -> bool:
        if event.type() == QEvent.ParentChange:
            widget = self.parentWidget()
            if widget:
                self.d.rippleOverlay.setParent(widget)

        return QAbstractButton.event(self, event)

    def paintEvent(self, event: QPaintEvent) -> void:
        ...

    disabledColor = Q_PROPERTY(QColor, fset=setDisabledColor, fget=disabledColor)
    activeColor = Q_PROPERTY(QColor, fset=setActiveColor, fget=activeColor)
    inactiveColor = Q_PROPERTY(QColor, fset=setInactiveColor, fget=inactiveColor)
    trackColor = Q_PROPERTY(QColor, fset=setTrackColor, fget=trackColor)
