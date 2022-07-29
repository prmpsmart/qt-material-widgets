from .core.ripple_overlay import *


class QMaterialToggleThumb(QWidget):
    def __init__(self, parent: "QMaterialToggle"):
        QWidget.__init__(self, parent)

        self.m_toggle = parent
        self.m_thumbColor = QColor()
        self.m_shift = 0
        self.m_offset = 0

        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(6)
        effect.setColor(QColor(0, 0, 0, 80))
        effect.setOffset(QPointF(0, 1))
        self.setGraphicsEffect(effect)

        parent.installEventFilter(self)

    def setShift(self, shift: float) -> None:
        if self.m_shift == shift:
            return

        self.m_shift = shift
        self.updateOffset()

    def shift(self) -> float:
        return self.m_shift

    def offset(self) -> float:
        return self.m_offset

    def setThumbColor(self, color: QColor) -> None:
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

    def paintEvent(self, event: QPaintEvent) -> None:
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

    def updateOffset(self) -> None:
        s = QSize(
            self.size()
            if Qt.Horizontal == self.m_toggle.orientation()
            else self.size().transposed()
        )
        self.m_offset = self.m_shift * s.width() - s.height()
        self.update()

    _shift = Property(float, fset=setShift, fget=shift)
    _thumbColor = Property(QColor, fset=setThumbColor, fget=thumbColor)


class QMaterialToggleTrack(QWidget):
    def __init__(self, parent: "QMaterialToggle"):
        QWidget.__init__(self, parent)
        self.m_toggle = parent
        self.m_trackColor = QColor()

        parent.installEventFilter(self)

    def setTrackColor(self, color: QColor) -> None:
        self.m_trackColor = color
        self.update()

    def trackColor(self) -> QColor:
        return self.m_trackColor

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        type: QEvent.Type = event.type()

        if QEvent.Resize == type or QEvent.Move == type:
            self.setGeometry(self.m_toggle.rect())

        return QWidget.eventFilter(self, obj, event)

    def paintEvent(self, event: QPaintEvent) -> None:
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

    _trackColor = Property(QColor, fset=setTrackColor, fget=trackColor)


class QMaterialToggleRippleOverlay(QMaterialRippleOverlay):
    def __init__(
        self,
        thumb: QMaterialToggleThumb,
        track: QMaterialToggleTrack,
        parent: "QMaterialToggle",
    ):
        QMaterialRippleOverlay.__init__(self, parent)

        self.m_toggle = parent
        self.m_thumb = thumb
        self.m_track = track

        parent.toggled.connect(self.addToggleRipple)

        thumb.installEventFilter(self)

    def addToggleRipple(self) -> None:
        if not self.m_toggle.isEnabled():
            return

        if Qt.Horizontal == self.m_toggle.orientation():
            t: int = self.m_toggle.height() / 2
            w: int = self.m_thumb.height() / 2 + 10
        else:
            t: int = self.m_toggle.width() / 2
            w: int = self.m_thumb.width() / 2 + 10

        ripple = QMaterialRipple(QPoint(10 + t, 20 + t))
        ripple.setColor(self.m_track.trackColor())
        ripple.setRadiusEndValue(w)
        ripple.setOpacityStartValue(0.8)

        self.addRipple(ripple)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if QEvent.Paint == event.type():
            self.setGeometry(self.overlayGeometry())

            items: List[QMaterialRipple] = self.ripples()

            color: QColor = self.m_track.trackColor()
            for i in items:
                i.setColor(color)

        return QMaterialRippleOverlay.eventFilter(self, obj, event)

    def overlayGeometry(self) -> QRect:
        offset: float = self.m_thumb.offset()
        if Qt.Horizontal == self.m_toggle.orientation():
            return self.m_toggle.geometry().adjusted(-10 + offset, -20, 10 + offset, 20)
        else:
            return self.m_toggle.geometry().adjusted(-10, -20 + offset, 10, 20 + offset)


class QMaterialToggle(QAbstractButton):
    def __init__(self, parent: QWidget = None):
        QAbstractButton.__init__(self, parent)

        self.m_track = QMaterialToggleTrack(self)
        self.m_thumb = QMaterialToggleThumb(self)
        self.m_rippleOverlay = QMaterialToggleRippleOverlay(
            self.m_thumb, self.m_track, self
        )
        self.m_stateMachine = QStateMachine(self)
        self.m_offState = QState()
        self.m_onState = QState()
        self.m_orientation = Qt.Horizontal
        self.m_useThemeColors = True

        self.setCheckable(True)
        self.setChecked(False)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.m_stateMachine.addState(self.m_offState)
        self.m_stateMachine.addState(self.m_onState)
        self.m_stateMachine.setInitialState(self.m_offState)

        self.m_offState.assignProperty(self.m_thumb, "_shift", 0)
        self.m_onState.assignProperty(self.m_thumb, "_shift", 1)

        transition = QSignalTransition(self.m_toggled)
        transition.setTargetState(self.m_onState)
        self.m_offState.addTransition(transition)

        animation = QPropertyAnimation(self)
        animation.setPropertyName(b"_shift")
        animation.setTargetObject(self.m_thumb)
        animation.setDuration(200)
        animation.setEasingCurve(QEasingCurve.OutQuad)
        transition.addAnimation(animation)

        animation = QPropertyAnimation(self)
        animation.setPropertyName(b"_trackColor")
        animation.setTargetObject(self.m_track)
        animation.setDuration(150)
        transition.addAnimation(animation)

        animation = QPropertyAnimation(self)
        animation.setPropertyName(b"_thumbColor")
        animation.setTargetObject(self.m_thumb)
        animation.setDuration(150)
        transition.addAnimation(animation)

        self.setupProperties()

        self.m_stateMachine.start()
        QCoreApplication.processEvents()

    def setupProperties(self) -> None:
        if self.isEnabled():
            shift: float = self.m_thumb.shift()
            if qFuzzyCompare(shift, 1):
                self.m_thumb.setThumbColor(self.activeColor())
                self.m_track.setTrackColor(self.activeColor().lighter(110))
            elif qFuzzyCompare(1 + shift, 1):
                self.m_thumb.setThumbColor(self.inactiveColor())
                self.m_track.setTrackColor(self.trackColor())

        self.m_offState.assignProperty(
            self.m_track, "trackColor", self.trackColor().lighter(110)
        )
        self.m_onState.assignProperty(
            self.m_track, "trackColor", self.activeColor().lighter(110)
        )

        self.m_offState.assignProperty(self.m_thumb, "thumbColor", self.inactiveColor())
        self.m_onState.assignProperty(self.m_thumb, "thumbColor", self.activeColor())

        self.update()

    def setUseThemeColors(self, value: bool) -> None:
        self.m_useThemeColors = value
        self.setupProperties()

    def useThemeColors(self) -> bool:
        return self.m_useThemeColors

    def setDisabledColor(self, color: QColor) -> None:
        self.m_disabledColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.setupProperties()

    def disabledColor(self) -> QColor:
        if self.m_useThemeColors or not self.m_disabledColor.isValid():
            return QMaterialStyle.instance().themeColor("disabled")
        else:
            return self.m_disabledColor

    def setActiveColor(self, color: QColor) -> None:
        self.m_activeColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.setupProperties()

    def activeColor(self) -> QColor:
        if self.m_useThemeColors or not self.m_activeColor.isValid():
            return QMaterialStyle.instance().themeColor("primary1")
        else:
            return self.m_activeColor

    def setInactiveColor(self, color: QColor) -> None:
        self.m_inactiveColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.m_setupProperties()

    def inactiveColor(self) -> QColor:
        if self.m_useThemeColors or not self.m_inactiveColor.isValid():
            return QMaterialStyle.instance().themeColor("canvas")
        else:
            return self.m_inactiveColor

    def setTrackColor(self, color: QColor) -> None:
        self.m_trackColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.m_setupProperties()

    def trackColor(self) -> QColor:
        if self.m_useThemeColors or not self.m_trackColor.isValid():
            return QMaterialStyle.instance().themeColor("accent3")
        else:
            return self.m_trackColor

    def setOrientation(self, orientation: Qt.Orientation) -> None:
        if self.m_orientation == orientation:
            return

        self.m_orientation = orientation
        self.updateGeometry()

    def orientation(self) -> Qt.Orientation:
        return self.m_orientation

    def sizeHint(self) -> QSize:
        return QSize(64, 48) if Qt.Horizontal == self.m_orientation else QSize(48, 64)

    def event(self, event: QEvent) -> bool:
        if event.type() == QEvent.ParentChange:
            widget = self.parentWidget()
            if widget:
                self.m_rippleOverlay.setParent(widget)

        return QAbstractButton.event(self, event)

    def paintEvent(self, event: QPaintEvent) -> None:
        ...

    _disabledColor = Property(QColor, fset=setDisabledColor, fget=disabledColor)
    _activeColor = Property(QColor, fset=setActiveColor, fget=activeColor)
    _inactiveColor = Property(QColor, fset=setInactiveColor, fget=inactiveColor)
    _trackColor = Property(QColor, fset=setTrackColor, fget=trackColor)
