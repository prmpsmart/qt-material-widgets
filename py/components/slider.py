from .lib.qtmaterial import *

QT_MATERIAL_SLIDER_MARGIN = 30


class QtMaterialSlider:
    ...


class QtMaterialSliderThumb(QtMaterialOverlayWidget):
    def __init__(self, slider: QtMaterialSlider):
        QtMaterialOverlayWidget.__init__(self, slider.parentWidget())

        self.m_slider = slider
        self.m_borderColor = QColor()
        self.m_fillColor = QColor()
        self.m_haloColor = QColor()
        self.m_diameter = qreal(11)
        self.m_borderWidth = qreal(2)
        self.m_haloSize = qreal(0)
        self.m_offset = int(0)

        slider.installEventFilter(self)

        self.setAttribute(Qt.WA_TransparentForMouseEvents, true)

    def setDiameter(self, diameter: qreal) -> void:
        self.m_diameter = diameter
        self.update()

    def diameter(self) -> qreal:
        return self.m_diameter

    def setBorderWidth(self, width: qreal) -> void:
        self.m_borderWidth = width
        self.update()

    def borderWidth(self) -> qreal:
        return self.m_borderWidth

    def setBorderColor(self, color: QColor) -> void:
        self.m_borderColor = color
        self.update()

    def borderColor(self) -> QColor:
        return self.m_borderColor

    def setFillColor(self, color: QColor) -> void:
        self.m_fillColor = color
        self.update()

    def fillColor(self) -> QColor:
        return self.m_fillColor

    def setHaloSize(self, size: qreal) -> void:
        self.m_haloSize = size
        self.update()

    def haloSize(self) -> qreal:
        return self.m_haloSize

    def setHaloColor(self, color: QColor) -> void:
        self.m_haloColor = color
        self.update()

    def haloColor(self) -> QColor:
        return self.m_haloColor

    def setOffset(self, offset: int) -> void:
        self.m_offset = offset
        self.update()

    def offset(self) -> int:
        return self.m_offset

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if QEvent.ParentChange == event.type():
            self.setParent(self.m_slider.parentWidget())

        return QtMaterialOverlayWidget.eventFilter(self, obj, event)

    def paintEvent(self, event: QPaintEvent) -> void:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # // Halo

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(self.m_haloColor)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)

        disp: QPointF = (
            Qt.Horizontal
            == QPointF(
                QT_MATERIAL_SLIDER_MARGIN + self.m_offset, self.m_slider.height() / 2
            )
            if self.m_slider.orientation()
            else QPointF(
                self.m_slider.width() / 2, QT_MATERIAL_SLIDER_MARGIN + self.m_offset
            )
        )

        halo = QRectF(
            (self.m_slider.pos() - QPointF(self.m_haloSize, self.m_haloSize) / 2)
            + disp,
            QSizeF(self.m_haloSize, self.m_haloSize),
        )

        painter.setOpacity(0.15)
        painter.drawEllipse(halo)

        # // Knob

        isMin: bool = self.m_slider.value() == self.m_slider.minimum()

        brush.setColor(
            self.m_fillColor
            if self.m_slider.isEnabled()
            else self.m_slider.disabledColor()
        )
        painter.setBrush(
            Qt.NoBrush if (not self.m_slider.isEnabled() and isMin) else brush
        )

        if self.m_slider.isEnabled() or isMin:
            pen = QPen()
            pen.setColor(self.m_borderColor)
            pen.setWidthF(
                1.7 if (isMin and not self.m_slider.isEnabled()) else self.m_borderWidth
            )
            painter.setPen(pen)
        else:
            painter.setPen(Qt.NoPen)

        geometry: QRectF = (
            QRectF(
                self.m_offset,
                self.m_slider.height() / 2 - QT_MATERIAL_SLIDER_MARGIN,
                QT_MATERIAL_SLIDER_MARGIN * 2,
                QT_MATERIAL_SLIDER_MARGIN * 2,
            ).translated(self.m_slider.pos())
            if Qt.Horizontal == self.m_slider.orientation()
            else QRectF(
                self.m_slider.width() / 2 - QT_MATERIAL_SLIDER_MARGIN,
                self.m_offset,
                QT_MATERIAL_SLIDER_MARGIN * 2,
                QT_MATERIAL_SLIDER_MARGIN * 2,
            ).translated(self.m_slider.pos())
        )

        s: qreal = self.m_diameter if self.m_slider.isEnabled() else 7

        thumb = QRectF(0, 0, s, s)

        thumb.moveCenter(geometry.center())

        painter.setOpacity(1)
        painter.drawEllipse(thumb)

        painter.end()

    _diameter = Q_PROPERTY(qreal, fset=setDiameter, fget=diameter)
    _borderWidth = Q_PROPERTY(qreal, fset=setBorderWidth, fget=borderWidth)
    _borderColor = Q_PROPERTY(QColor, fset=setBorderColor, fget=borderColor)
    _fillColor = Q_PROPERTY(QColor, fset=setFillColor, fget=fillColor)
    _haloSize = Q_PROPERTY(qreal, fset=setHaloSize, fget=haloSize)
    _haloColor = Q_PROPERTY(QColor, fset=setHaloColor, fget=haloColor)


class QtMaterialSliderTrack(QtMaterialOverlayWidget):
    def __init__(self, thumb: QtMaterialSliderThumb, slider: QtMaterialSlider):
        QtMaterialOverlayWidget.__init__(self)
        self.m_slider = slider
        self.m_thumb = thumb
        self.m_fillColor = QColor()
        self.m_trackWidth = int(2)

        slider.installEventFilter(self)

        self.setAttribute(Qt.WA_TransparentForMouseEvents, true)

        slider.sliderMoved.connect(self.update)

    def setFillColor(self, color: QColor) -> void:
        self.m_fillColor = color
        self.update()

    def fillColor(self) -> QColor:
        return self.m_fillColor

    fillColor = Property(QColor, fillColor, setFillColor)

    def setTrackWidth(self, width: int) -> void:
        self.m_trackWidth = width
        self.update()

    def trackWidth(self) -> int:
        return self.m_trackWidth

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if QEvent.ParentChange == event.type():
            self.setParent(self.m_slider.parentWidget())

        return QtMaterialOverlayWidget.eventFilter(self, obj, event)

    def paintEvent(self, event: QPaintEvent) -> void:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        fg = QBrush()
        fg.setStyle(Qt.SolidPattern)
        fg.setColor(
            self.m_slider.thumbColor()
            if self.m_slider.isEnabled()
            else self.m_slider.disabledColor()
        )
        bg = QBrush()
        bg.setStyle(Qt.SolidPattern)
        bg.setColor(
            self.m_fillColor
            if self.m_slider.isEnabled()
            else self.m_slider.disabledColor()
        )

        offset: qreal = self.m_thumb.offset

        if Qt.Horizontal == self.m_slider.orientation():
            painter.translate(
                self.m_slider.x() + QT_MATERIAL_SLIDER_MARGIN,
                self.m_slider.y() + self.m_slider.height() / 2 - self.m_trackWidth / 2,
            )
        else:
            painter.translate(
                self.m_slider.x() + self.m_slider.width() / 2 - self.m_trackWidth / 2,
                self.m_slider.y() + QT_MATERIAL_SLIDER_MARGIN,
            )

        geometry: QRectF = (
            QRectF(
                0,
                0,
                self.m_slider.width() - QT_MATERIAL_SLIDER_MARGIN * 2,
                self.m_trackWidth,
            )
            if Qt.Horizontal == self.m_slider.orientation()
            else QRectF(
                0,
                0,
                self.m_trackWidth,
                self.m_slider.height() - QT_MATERIAL_SLIDER_MARGIN * 2,
            )
        )

        if Qt.Horizontal == self.m_slider.orientation():
            fgRect = QRectF(0, 0, offset, self.m_trackWidth)
            bgRect = QRectF(
                offset, 0, self.m_slider.width(), self.m_trackWidth
            ).intersected(geometry)
        else:
            fgRect = QRectF(0, 0, self.m_trackWidth, offset)
            bgRect = QRectF(
                0, offset, self.m_trackWidth, self.m_slider.height()
            ).intersected(geometry)

        if not self.m_slider.isEnabled():
            fgRect = QRectF() if fgRect.width() < 9 else fgRect.adjusted(0, 0, -6, 0)
            bgRect = QRectF() if bgRect.width() < 9 else bgRect.adjusted(6, 0, 0, 0)

        if self.m_slider.invertedAppearance():
            bgRect, fgRect = fgRect, bgRect

        painter.fillRect(bgRect, bg)
        painter.fillRect(fgRect, fg)


class QtMaterialSliderStateMachine(QStateMachine):
    def __init__(
        self,
        slider: QtMaterialSlider,
        thumb: QtMaterialSliderThumb,
        track: QtMaterialSliderTrack,
    ):
        QStateMachine.__init__(self)
        self.m_slider = slider
        self.m_thumb = thumb
        self.m_track = track
        self.m_topState = QState()
        self.m_fstState = QState(self.m_topState)
        self.m_sndState = QState(self.m_topState)
        self.m_inactiveState = QState(self.m_fstState)
        self.m_focusState = QState(self.m_fstState)
        self.m_slidingState = QState(self.m_fstState)
        self.m_pulseOutState = QState(self.m_focusState)
        self.m_pulseInState = QState(self.m_focusState)
        self.m_minState = QState(self.m_sndState)
        self.m_normalState = QState(self.m_sndState)

        self.addState(self.m_topState)
        self.setInitialState(self.m_topState)

        self.m_fstState.setInitialState(self.m_inactiveState)
        self.m_focusState.setInitialState(self.m_pulseOutState)

        self.m_inactiveState.assignProperty(thumb, "haloSize", 0)
        self.m_slidingState.assignProperty(thumb, "haloSize", 0)

        self.m_pulseOutState.assignProperty(thumb, "haloSize", 35)
        self.m_pulseInState.assignProperty(thumb, "haloSize", 28)

        self.m_inactiveState.assignProperty(thumb, "diameter", 11)
        self.m_focusState.assignProperty(thumb, "diameter", 11)
        self.m_slidingState.assignProperty(thumb, "diameter", 17)

        # // Show halo on mouse enter

        customTransition = QtMaterialStateTransition(
            QtMaterialStateTransitionType.SliderNoFocusMouseEnter
        )
        customTransition.setTargetState(self.m_focusState)

        animation = QPropertyAnimation(thumb, b"haloSize", self)
        animation.setEasingCurve(QEasingCurve.InOutSine)
        customTransition.addAnimation(animation)
        customTransition.addAnimation(QPropertyAnimation(track, b"fillColor", self))
        self.m_inactiveState.addTransition(customTransition)

        # // Show halo on focus in

        transition = QEventTransition(slider, QEvent.FocusIn)
        transition.setTargetState(self.m_focusState)

        animation = QPropertyAnimation(thumb, b"haloSize", self)
        animation.setEasingCurve(QEasingCurve.InOutSine)
        transition.addAnimation(animation)
        transition.addAnimation(QPropertyAnimation(track, b"fillColor", self))
        self.m_inactiveState.addTransition(transition)

        # // Hide halo on focus out

        transition = QEventTransition(slider, QEvent.FocusOut)
        transition.setTargetState(self.m_inactiveState)

        animation = QPropertyAnimation(thumb, b"haloSize", self)
        animation.setEasingCurve(QEasingCurve.InOutSine)
        transition.addAnimation(animation)
        transition.addAnimation(QPropertyAnimation(track, b"fillColor", self))
        self.m_focusState.addTransition(transition)

        # // Hide halo on mouse leave, except if widget has focus

        customTransition = QtMaterialStateTransition(
            QtMaterialStateTransitionType.SliderNoFocusMouseLeave
        )
        customTransition.setTargetState(self.m_inactiveState)

        animation = QPropertyAnimation(thumb, b"haloSize", self)
        animation.setEasingCurve(QEasingCurve.InOutSine)
        customTransition.addAnimation(animation)
        customTransition.addAnimation(QPropertyAnimation(track, b"fillColor", self))
        self.m_focusState.addTransition(customTransition)

        # // Pulse in

        transition = QSignalTransition(self.m_pulseOutState, self.propertiesAssigned)
        transition.setTargetState(self.m_pulseInState)

        animation = QPropertyAnimation(thumb, b"haloSize", self)
        animation.setEasingCurve(QEasingCurve.InOutSine)
        animation.setDuration(1000)
        transition.addAnimation(animation)
        self.m_pulseOutState.addTransition(transition)

        # // Pulse out

        transition = QSignalTransition(self.m_pulseInState, self.propertiesAssigned)
        transition.setTargetState(self.m_pulseOutState)

        animation = QPropertyAnimation(thumb, b"haloSize", self)
        animation.setEasingCurve(QEasingCurve.InOutSine)
        animation.setDuration(1000)
        transition.addAnimation(animation)
        self.m_pulseInState.addTransition(transition)

        # // Slider pressed

        transition = QSignalTransition(slider.sliderPressed)
        transition.setTargetState(self.m_slidingState)
        animation = QPropertyAnimation(thumb, b"diameter", self)
        animation.setDuration(70)
        transition.addAnimation(animation)

        animation = QPropertyAnimation(thumb, b"haloSize", self)
        animation.setEasingCurve(QEasingCurve.InOutSine)
        transition.addAnimation(animation)
        self.m_focusState.addTransition(transition)

        # // Slider released

        transition = QSignalTransition(slider.sliderReleased)
        transition.setTargetState(self.m_focusState)
        animation = QPropertyAnimation(thumb, b"diameter", self)
        animation.setDuration(70)
        transition.addAnimation(animation)

        animation = QPropertyAnimation(thumb, b"haloSize", self)
        animation.setEasingCurve(QEasingCurve.InOutSine)
        transition.addAnimation(animation)
        self.m_slidingState.addTransition(transition)

        # // Min. value transitions

        self.m_minState.assignProperty(thumb, "borderWidth", 2)
        self.m_normalState.assignProperty(thumb, "borderWidth", 0)

        self.m_sndState.setInitialState(self.m_minState)

        customTransition = QtMaterialStateTransition(
            QtMaterialStateTransitionType.SliderChangedFromMinimum
        )
        customTransition.setTargetState(self.m_normalState)

        animation = QPropertyAnimation(thumb, b"fillColor", self)
        animation.setDuration(200)
        customTransition.addAnimation(animation)

        animation = QPropertyAnimation(thumb, b"haloColor", self)
        animation.setDuration(300)
        customTransition.addAnimation(animation)

        animation = QPropertyAnimation(thumb, b"borderColor", self)
        animation.setDuration(200)
        customTransition.addAnimation(animation)

        animation = QPropertyAnimation(thumb, b"borderWidth", self)
        animation.setDuration(200)
        customTransition.addAnimation(animation)

        self.m_minState.addTransition(customTransition)

        customTransition = QtMaterialStateTransition(
            QtMaterialStateTransitionType.SliderChangedToMinimum
        )
        customTransition.setTargetState(self.m_minState)

        animation = QPropertyAnimation(thumb, b"fillColor", self)
        animation.setDuration(200)
        customTransition.addAnimation(animation)

        animation = QPropertyAnimation(thumb, b"haloColor", self)
        animation.setDuration(300)
        customTransition.addAnimation(animation)

        animation = QPropertyAnimation(thumb, b"borderColor", self)
        animation.setDuration(200)
        customTransition.addAnimation(animation)

        animation = QPropertyAnimation(thumb, b"borderWidth", self)
        animation.setDuration(200)
        customTransition.addAnimation(animation)

        self.m_normalState.addTransition(customTransition)
        self.start()

        self.setupProperties()

    def setupProperties(self) -> void:
        trackColor: QColor = self.m_slider.trackColor()
        thumbColor: QColor = self.m_slider.thumbColor()

        self.m_inactiveState.assignProperty(
            self.m_track, "fillColor", trackColor.lighter(130)
        )
        self.m_slidingState.assignProperty(self.m_track, "fillColor", trackColor)
        self.m_focusState.assignProperty(self.m_track, "fillColor", trackColor)

        holeColor: QColor = self.m_slider.palette().color(QPalette.Base)

        if self.m_slider.parentWidget():
            holeColor = (
                self.m_slider.parentWidget()
                .palette()
                .color(self.m_slider.backgroundRole())
            )

        self.m_minState.assignProperty(self.m_thumb, "fillColor", holeColor)

        self.m_minState.assignProperty(self.m_thumb, "haloColor", trackColor)
        self.m_minState.assignProperty(self.m_thumb, "borderColor", trackColor)

        self.m_normalState.assignProperty(self.m_thumb, "fillColor", thumbColor)
        self.m_normalState.assignProperty(self.m_thumb, "haloColor", thumbColor)
        self.m_normalState.assignProperty(self.m_thumb, "borderColor", thumbColor)

        self.m_slider.update()


class QtMaterialSliderPrivate:
    def __init__(self, q: QtMaterialSlider):
        self.q: QtMaterialSlider = q

        self.thumbColor = QColor()
        self.trackColor = QColor()
        self.disabledColor = QColor()
        self.stepTo: int = None
        self.oldValue: int = None
        self.trackWidth: int = None
        self.hoverTrack: bool = None
        self.hoverThumb: bool = None
        self.hover: bool = None
        self.step: bool = None
        self.pageStepMode: bool = None
        self.useThemeColors: bool = None

    def init(self) -> void:
        self.thumb = QtMaterialSliderThumb(self.q)
        self.track = QtMaterialSliderTrack(self.thumb, self.q)
        self.stateMachine = QtMaterialSliderStateMachine(self.q, self.thumb, self.track)
        self.stepTo = 0
        self.oldValue = self.q.value()
        self.trackWidth = 2
        self.hoverTrack = false
        self.hoverThumb = false
        self.hover = false
        self.step = false
        self.pageStepMode = true
        self.useThemeColors = true
        self.stateMachine.start()

        self.q.setMouseTracking(true)
        self.q.setFocusPolicy(Qt.StrongFocus)
        self.q.setPageStep(1)

        sp = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        if self.q.orientation() == Qt.Vertical:
            sp.transpose()

        self.q.setSizePolicy(sp)
        self.q.setAttribute(Qt.WA_WState_OwnSizePolicy, false)

        QCoreApplication.processEvents()

    def trackBoundingRect(self) -> QRectF:
        hw: qreal = self.trackWidth / 2

        return (
            QRectF(
                QT_MATERIAL_SLIDER_MARGIN,
                self.q.height() / 2 - hw,
                self.q.width() - QT_MATERIAL_SLIDER_MARGIN * 2,
                hw * 2,
            )
            if Qt.Horizontal == self.q.orientation()
            else QRectF(
                self.q.width() / 2 - hw,
                QT_MATERIAL_SLIDER_MARGIN,
                hw * 2,
                self.q.height() - QT_MATERIAL_SLIDER_MARGIN * 2,
            )
        )

    def thumbBoundingRect(self) -> QRectF:
        return (
            QRectF(
                self.thumb.offset,
                self.q.height() / 2 - QT_MATERIAL_SLIDER_MARGIN,
                QT_MATERIAL_SLIDER_MARGIN * 2,
                QT_MATERIAL_SLIDER_MARGIN * 2,
            )
            if Qt.Horizontal == self.q.orientation()
            else QRectF(
                self.q.width() / 2 - QT_MATERIAL_SLIDER_MARGIN,
                self.thumb.offset(),
                QT_MATERIAL_SLIDER_MARGIN * 2,
                QT_MATERIAL_SLIDER_MARGIN * 2,
            )
        )

    def valueFromPosition(self, pos: QPoint) -> int:
        position: int = pos.x() if Qt.Horizontal == self.q.orientation() else pos.y()

        span: int = (
            self.q.width() - QT_MATERIAL_SLIDER_MARGIN * 2
            if Qt.Horizontal == self.q.orientation()
            else self.q.height() - QT_MATERIAL_SLIDER_MARGIN * 2
        )

        return QtMaterialStyle.sliderValueFromPosition(
            self.q.minimum(),
            self.q.maximum(),
            position - QT_MATERIAL_SLIDER_MARGIN,
            span,
            self.q.invertedAppearance(),
        )

    def setHovered(self, status: bool) -> void:
        if self.hover == status:
            return

        self.hover = status

        if not self.q.hasFocus():
            if status:
                self.stateMachine.postEvent(
                    QtMaterialStateTransitionEvent(
                        QtMaterialStateTransitionType.SliderNoFocusMouseEnter
                    )
                )
            else:
                self.stateMachine.postEvent(
                    QtMaterialStateTransitionEvent(
                        QtMaterialStateTransitionType.SliderNoFocusMouseLeave
                    )
                )

        self.q.update()


class QtMaterialSlider(QAbstractSlider):
    def __init__(self, parent: QWidget = None, d: QtMaterialSliderPrivate = None):
        QAbstractSlider.__init__(self, parent)

        self.d = d or QtMaterialSliderPrivate(self)
        self.d.init()

    def setUseThemeColors(self, value: bool) -> void:
        if self.d.useThemeColors == value:
            return

        self.d.useThemeColors = value
        self.d.stateMachine.setupProperties()

    def useThemeColors(self) -> bool:
        return self.d.useThemeColors

    def setThumbColor(self, color: QColor) -> void:
        self.d.thumbColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.d.stateMachine.setupProperties()
        self.update()

    def thumbColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.thumbColor.isValid():
            return QtMaterialStyle.instance().themeColor("primary1")
        else:
            return self.d.thumbColor

    def setTrackColor(self, color: QColor) -> void:
        self.d.trackColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.d.stateMachine.setupProperties()
        self.update()

    def trackColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.trackColor.isValid():
            return QtMaterialStyle.instance().themeColor("accent3")
        else:
            return self.d.trackColor

    def setDisabledColor(self, color: QColor) -> void:
        self.d.disabledColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.d.stateMachine.setupProperties()
        self.update()

    def disabledColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.disabledColor.isValid():
            return QtMaterialStyle.instance().themeColor("disabled")
        else:
            return self.d.disabledColor

    def setPageStepMode(self, pageStep: bool) -> void:
        self.d.pageStepMode = pageStep

    def pageStepMode(self) -> bool:
        return self.d.pageStepMode

    def minimumSizeHint(self) -> QSize:
        return QSize(130, 34) if Qt.Horizontal == self.orientation() else QSize(34, 130)

    def setInvertedAppearance(self, value: bool) -> void:
        QAbstractSlider.setInvertedAppearance(self, value)

        self.updateThumbOffset()

    def sliderChange(self, change: QAbstractSlider.SliderChange) -> void:
        if QAbstractSlider.SliderOrientationChange == change:
            sp = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            if self.orientation() == Qt.Vertical:
                sp.transpose()
            self.setSizePolicy(sp)

        elif QAbstractSlider.SliderValueChange == change:
            if self.minimum() == self.value():
                self.triggerAction(QAbstractSlider.SliderToMinimum)
                self.d.stateMachine.postEvent(
                    QtMaterialStateTransitionEvent(
                        QtMaterialStateTransitionType.SliderChangedToMinimum
                    )
                )
            elif self.maximum() == self.value():
                self.triggerAction(QAbstractSlider.SliderToMaximum)

            if self.minimum() == self.d.oldValue:
                self.d.stateMachine.postEvent(
                    QtMaterialStateTransitionEvent(
                        QtMaterialStateTransitionType.SliderChangedFromMinimum
                    )
                )

            self.d.oldValue = self.value()

        self.updateThumbOffset()

        QAbstractSlider.sliderChange(self, change)

    def mouseMoveEvent(self, event: QMouseEvent) -> void:
        if self.isSliderDown():
            self.setSliderPosition(self.d.valueFromPosition(event.pos()))
        else:
            track = QRectF(self.d.trackBoundingRect().adjusted(-2, -2, 2, 2))

            if track.contains(event.pos()) != self.d.hoverTrack:
                self.d.hoverTrack = not self.d.hoverTrack
                self.update()

            thumb = QRectF(0, 0, 16, 16)
            thumb.moveCenter(self.d.thumbBoundingRect().center())

            if thumb.contains(event.pos()) != self.d.hoverThumb:
                self.d.hoverThumb = not self.d.hoverThumb
                self.update()

            self.d.setHovered(self.d.hoverTrack or self.d.hoverThumb)

        QAbstractSlider.mouseMoveEvent(self, event)

    def mousePressEvent(self, event: QMouseEvent) -> void:
        pos: QPoint = event.pos()

        thumb = QRectF(0, 0, 16, 16)
        thumb.moveCenter(self.d.thumbBoundingRect().center())

        if thumb.contains(pos):
            self.setSliderDown(true)
            return

        if not self.d.pageStepMode:
            self.setSliderPosition(self.d.valueFromPosition(event.pos()))
            self.d.thumb.setHaloSize(0)
            self.setSliderDown(true)
            return

        self.d.step = true
        self.d.stepTo = self.d.valueFromPosition(pos)

        action: QAbstractSlider.SliderAction = (
            QAbstractSlider.SliderPageStepAdd
            if self.d.stepTo > self.sliderPosition()
            else QAbstractSlider.SliderPageStepSub
        )

        self.triggerAction(action)
        self.setRepeatAction(action, 400, 8)

    def mouseReleaseEvent(self, event: QMouseEvent) -> void:
        if self.isSliderDown():
            self.setSliderDown(false)
        elif self.d.step:
            self.d.step = false
            self.setRepeatAction(QAbstractSlider.SliderNoAction, 0)

        QAbstractSlider.mouseReleaseEvent(self, event)

    def leaveEvent(self, event: QEvent) -> void:
        if self.d.hoverTrack:
            self.d.hoverTrack = false
            self.update()

        if self.d.hoverThumb:
            self.d.hoverThumb = false
            self.update()

        self.d.setHovered(false)

        QAbstractSlider.leaveEvent(self, event)

    def updateThumbOffset(self) -> void:
        offset: int = QtMaterialStyle.sliderPositionFromValue(
            self.minimum(),
            self.maximum(),
            self.sliderPosition(),
            self.width() - QT_MATERIAL_SLIDER_MARGIN * 2
            if Qt.Horizontal == self.orientation()
            else self.height() - QT_MATERIAL_SLIDER_MARGIN * 2,
            self.invertedAppearance(),
        )

        self.d.thumb.setOffset(offset)

    _thumbColor = Q_PROPERTY(QColor, fset=setThumbColor, fget=thumbColor)
    _trackColor = Q_PROPERTY(QColor, fset=setTrackColor, fget=trackColor)
    _disabledColor = Q_PROPERTY(QColor, fset=setDisabledColor, fget=disabledColor)
