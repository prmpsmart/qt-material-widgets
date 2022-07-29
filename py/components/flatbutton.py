from .lib.qtmaterial import *


class QtMaterialFlatButtonStateMachine(QStateMachine):
    buttonPressed = Signal()
    buttonChecked = Signal()
    buttonUnchecked = Signal()

    def __init__(self, parent):
        QStateMachine.__init__(self, parent)

        self.m_button = parent
        self.m_topLevelState = QState(QState.ParallelStates)
        self.m_configState = QState(self.m_topLevelState)
        self.m_checkableState = QState(self.m_topLevelState)
        self.m_checkedState = QState(self.m_checkableState)
        self.m_uncheckedState = QState(self.m_checkableState)
        self.m_neutralState = QState(self.m_configState)
        self.m_neutralFocusedState = QState(self.m_configState)
        self.m_hoveredState = QState(self.m_configState)
        self.m_hoveredFocusedState = QState(self.m_configState)
        self.m_pressedState = QState(self.m_configState)
        self.m_haloAnimation = QSequentialAnimationGroup()
        self.m_overlayOpacity = qreal(0)
        self.m_checkedOverlayProgress = qreal(1 if parent and parent.isChecked else 0)
        self.m_haloOpacity = qreal(0)
        self.m_haloSize = qreal(0.8)
        self.m_haloScaleFactor = qreal(1)
        self.m_wasChecked = bool(false)

        if parent:
            parent.installEventFilter(self)

        self.m_configState.setInitialState(self.m_neutralState)
        self.addState(self.m_topLevelState)
        self.setInitialState(self.m_topLevelState)

        self.m_checkableState.setInitialState(
            self.m_checkedState
            if parent and parent.isChecked()
            else self.m_uncheckedState
        )

        transition = QtMaterialStateTransition(
            QtMaterialStateTransitionType.FlatButtonCheckedTransition
        )
        transition.setTargetState(self.m_checkedState)
        self.m_uncheckedState.addTransition(transition)

        animation = QPropertyAnimation(self, b"_checkedOverlayProgress")
        animation.setDuration(200)
        transition.addAnimation(animation)

        transition = QtMaterialStateTransition(
            QtMaterialStateTransitionType.FlatButtonUncheckedTransition
        )
        transition.setTargetState(self.m_uncheckedState)
        self.m_checkedState.addTransition(transition)

        animation = QPropertyAnimation(self, b"_checkedOverlayProgress", self)
        animation.setDuration(200)
        transition.addAnimation(animation)

        self.addTransition(
            self.m_button,
            QEvent.FocusIn,
            self.m_neutralState,
            self.m_neutralFocusedState,
        )
        self.addTransition(
            self.m_button,
            QEvent.FocusOut,
            self.m_neutralFocusedState,
            self.m_neutralState,
        )
        self.addTransition(
            self.m_button, QEvent.Enter, self.m_neutralState, self.m_hoveredState
        )
        self.addTransition(
            self.m_button, QEvent.Leave, self.m_hoveredState, self.m_neutralState
        )
        self.addTransition(
            self.m_button,
            QEvent.Enter,
            self.m_neutralFocusedState,
            self.m_hoveredFocusedState,
        )
        self.addTransition(
            self.m_button,
            QEvent.Leave,
            self.m_hoveredFocusedState,
            self.m_neutralFocusedState,
        )
        self.addTransition(
            self.m_button,
            QEvent.FocusIn,
            self.m_hoveredState,
            self.m_hoveredFocusedState,
        )
        self.addTransition(
            self.m_button,
            QEvent.FocusOut,
            self.m_hoveredFocusedState,
            self.m_hoveredState,
        )

        transition = QtMaterialStateTransition(
            QtMaterialStateTransitionType.FlatButtonPressedTransition
        )
        transition.setTargetState(self.m_pressedState)
        self.m_hoveredState.addTransition(transition)

        self.addTransition(
            self.m_button, QEvent.Leave, self.m_pressedState, self.m_neutralFocusedState
        )
        self.addTransition(
            self.m_button, QEvent.FocusOut, self.m_pressedState, self.m_hoveredState
        )

        self.m_neutralState.assignProperty(self, "_haloSize", 0)
        self.m_neutralFocusedState.assignProperty(self, "_haloSize", 0.7)
        self.m_hoveredState.assignProperty(self, "_haloSize", 0)
        self.m_pressedState.assignProperty(self, "_haloSize", 4)
        self.m_hoveredFocusedState.assignProperty(self, "_haloSize", 0.7)

        grow = QPropertyAnimation(self)
        shrink = QPropertyAnimation(self)

        grow.setTargetObject(self)
        grow.setPropertyName(b"_haloScaleFactor")
        grow.setStartValue(0.56)
        grow.setEndValue(0.63)
        grow.setEasingCurve(QEasingCurve.InOutSine)
        grow.setDuration(840)

        shrink.setTargetObject(self)
        shrink.setPropertyName(b"_haloScaleFactor")
        shrink.setStartValue(0.63)
        shrink.setEndValue(0.56)
        shrink.setEasingCurve(QEasingCurve.InOutSine)
        shrink.setDuration(840)

        self.m_haloAnimation.addAnimation(grow)
        self.m_haloAnimation.addAnimation(shrink)
        self.m_haloAnimation.setLoopCount(-1)

    def setOverlayOpacity(self, opacity: qreal) -> void:
        self.m_overlayOpacity = opacity
        self.m_button.update()

    def overlayOpacity(self) -> qreal:
        return self.m_overlayOpacity

    def setCheckedOverlayProgress(self, progress: qreal) -> void:
        self.m_checkedOverlayProgress = progress
        self.m_button.update()

    def checkedOverlayProgress(self) -> qreal:
        return self.m_checkedOverlayProgress

    def setHaloOpacity(self, opacity: qreal) -> void:
        self.m_haloOpacity = opacity
        self.m_button.update()

    def haloOpacity(self) -> qreal:
        return self.m_haloOpacity

    def setHaloSize(self, size: qreal) -> void:
        self.m_haloSize = size
        self.m_button.update()

    def haloSize(self) -> qreal:
        return self.m_haloSize

    def setHaloScaleFactor(self, factor: qreal) -> void:
        self.m_haloScaleFactor = factor
        self.m_button.update()

    def haloScaleFactor(self) -> qreal:
        return self.m_haloScaleFactor

    def startAnimations(self) -> void:
        self.m_haloAnimation.start()
        self.start()

    def setupProperties(self) -> void:
        # if Qt.TransparentMode == self.m_button.backgroundMode():
        #     overlayColor = self.m_button.backgroundColor()
        # else:
        #     overlayColor = self.m_button.foregroundColor()

        baseOpacity: qreal = self.m_button.baseOpacity()

        self.m_neutralState.assignProperty(self, "_overlayOpacity", 0)
        self.m_neutralState.assignProperty(self, "_haloOpacity", 0)
        self.m_neutralFocusedState.assignProperty(self, "_overlayOpacity", 0)
        self.m_neutralFocusedState.assignProperty(self, "_haloOpacity", baseOpacity)
        self.m_hoveredState.assignProperty(self, "_overlayOpacity", baseOpacity)
        self.m_hoveredState.assignProperty(self, "_haloOpacity", 0)
        self.m_hoveredFocusedState.assignProperty(self, "_overlayOpacity", baseOpacity)
        self.m_hoveredFocusedState.assignProperty(self, "_haloOpacity", baseOpacity)
        self.m_pressedState.assignProperty(self, "_overlayOpacity", baseOpacity)
        self.m_pressedState.assignProperty(self, "_haloOpacity", 0)
        self.m_checkedState.assignProperty(self, "_checkedOverlayProgress", 1)
        self.m_uncheckedState.assignProperty(self, "_checkedOverlayProgress", 0)

        self.m_button.update()

    def updateCheckedStatus(self) -> void:
        checked: bool = self.m_button.isChecked()
        if self.m_wasChecked != checked:
            self.m_wasChecked = checked
            if checked:
                # this causes the main thread to suddenly exit,
                # I dont know the reason yet..
                self.postEvent(
                    QtMaterialStateTransitionEvent(
                        QtMaterialStateTransitionType.FlatButtonCheckedTransition
                    )
                )
            else:
                # this causes the main thread to suddenly exit,
                # I dont know the reason yet..
                self.postEvent(
                    QtMaterialStateTransitionEvent(
                        QtMaterialStateTransitionType.FlatButtonUncheckedTransition
                    )
                )

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if QEvent.FocusIn == event.type():
            focusEvent: QFocusEvent = event
            if Qt.MouseFocusReason == focusEvent.reason():
                ev = QtMaterialStateTransitionEvent(
                    QtMaterialStateTransitionType.FlatButtonPressedTransition
                )
                # this causes the main thread to suddenly exit,
                # I dont know the reason yet..
                # self.postDelayedEvent(ev, 2)
                ...
            return true
        return QStateMachine.eventFilter(self, watched, event)

    def addTransition(
        self,
        object: QObject = None,
        eventType: QEvent.Type = None,
        fromState: QState = None,
        toState: QState = None,
        # transition: QAbstractTransition = None,
    ) -> void:
        # reordering

        transition = (
            object
            if isinstance(object, QAbstractTransition)
            else QEventTransition(object, eventType)
        )
        if transition == object:
            toState = fromState
            fromState = eventType

        transition.setTargetState(toState)

        animation = QPropertyAnimation(self, b"_overlayOpacity", self)
        animation.setDuration(150)
        transition.addAnimation(animation)

        animation = QPropertyAnimation(self, b"_haloOpacity", self)
        animation.setDuration(170)
        transition.addAnimation(animation)

        animation = QPropertyAnimation(self, b"_haloSize", self)
        animation.setDuration(350)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        transition.addAnimation(animation)

        fromState.addTransition(transition)

    _overlayOpacity = Q_PROPERTY(qreal, fset=setOverlayOpacity, fget=overlayOpacity)
    _checkedOverlayProgress = Q_PROPERTY(
        qreal, fset=setCheckedOverlayProgress, fget=checkedOverlayProgress
    )
    _haloOpacity = Q_PROPERTY(qreal, fset=setHaloOpacity, fget=haloOpacity)
    _haloSize = Q_PROPERTY(qreal, fset=setHaloSize, fget=haloSize)
    _haloScaleFactor = Q_PROPERTY(qreal, fset=setHaloScaleFactor, fget=haloScaleFactor)


class QtMaterialFlatButtonPrivate:
    def __init__(self, q):
        self.q: QtMaterialFlatButton = q
        self.backgroundColor = QColor()
        self.foregroundColor = QColor()
        self.overlayColor = QColor()
        self.disabledColor = QColor()
        self.disabledBackgroundColor = QColor()
        self.fixedRippleRadius: qreal = None
        self.cornerRadius: qreal = None
        self.baseOpacity: qreal = None
        self.fontSize: qreal = None
        self.useThemeColors: bool = None
        self.useFixedRippleRadius: bool = None
        self.haloVisible: bool = None

    def init(self) -> void:
        self.stateMachine = QtMaterialFlatButtonStateMachine(self.q)
        self.rippleOverlay = QtMaterialRippleOverlay(self.q)
        self.role = Material.Default
        self.rippleStyle = Material.PositionedRipple
        self.iconPlacement = Material.LeftIcon
        self.overlayStyle = Material.GrayOverlay
        self.bgMode = Qt.TransparentMode
        self.textAlignment = Qt.AlignHCenter
        self.fixedRippleRadius = 64
        self.cornerRadius = 3
        self.baseOpacity = 0.13
        self.fontSize = 10  # 10.5
        self.useThemeColors = true
        self.useFixedRippleRadius = false
        self.haloVisible = true

        self.q.setStyle(QtMaterialStyle.instance())
        self.q.setAttribute(Qt.WA_Hover)
        self.q.setMouseTracking(true)

        font = QFont("Roboto", self.fontSize, QFont.Medium)
        font.setCapitalization(QFont.AllUppercase)
        self.q.setFont(font)

        path = QPainterPath()
        path.addRoundedRect(self.q.rect(), self.cornerRadius, self.cornerRadius)
        self.rippleOverlay.setClipPath(path)
        self.rippleOverlay.setClipping(true)

        self.stateMachine.setupProperties()
        self.stateMachine.startAnimations()


class QtMaterialFlatButton(QPushButton):
    IconPadding = 12

    def __init__(
        self,
        text: QString = None,
        role: Material.Role = None,
        parent: QWidget = None,
        preset: Material.ButtonPreset = Material.FlatPreset,
        d: QtMaterialFlatButtonPrivate = None,
    ):

        QPushButton.__init__(self, text, parent)

        self.d = d or QtMaterialFlatButtonPrivate(self)
        self.d.init()
        self.applyPreset(preset)
        self.setRole(role)

    def applyPreset(self, preset: Material.ButtonPreset) -> void:
        if preset == Material.FlatPreset:
            self.setOverlayStyle(Material.NoOverlay)
        elif preset == Material.CheckablePreset:
            self.setOverlayStyle(Material.NoOverlay)
            self.setCheckable(true)
            self.setHaloVisible(false)

    def setUseThemeColors(self, value: bool) -> void:
        if self.d.useThemeColors == value:
            return
        self.d.useThemeColors = value
        self.d.stateMachine.setupProperties()

    def useThemeColors(self) -> bool:
        return self.d.useThemeColors

    def setRole(self, role: Material.Role) -> void:
        self.d.role = role
        self.d.stateMachine.setupProperties()

    def role(self) -> Material.Role:
        return self.d.role

    def setForegroundColor(self, color: QColor) -> void:
        self.d.foregroundColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.update()

    def foregroundColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.foregroundColor.isValid():
            if Qt.OpaqueMode == self.d.bgMode:
                return QtMaterialStyle.instance().themeColor("canvas")

            role = self.d.role
            if role == Material.Primary:
                return QtMaterialStyle.instance().themeColor("primary1")
            elif role == Material.Secondary:
                return QtMaterialStyle.instance().themeColor("accent1")
            else:  # role == Material.Default:...
                return QtMaterialStyle.instance().themeColor("text")

        return self.d.foregroundColor

    def setBackgroundColor(self, color: QColor) -> void:
        self.d.backgroundColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.update()

    def backgroundColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.backgroundColor.isValid():
            role = self.d.role
            if role == Material.Primary:
                return QtMaterialStyle.instance().themeColor("primary1")
            elif role == Material.Secondary:
                return QtMaterialStyle.instance().themeColor("accent1")
            else:  # role == Material.Default:
                return QtMaterialStyle.instance().themeColor("text")
        return self.d.backgroundColor

    def setOverlayColor(self, color: QColor) -> void:
        self.d.overlayColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)

        self.setOverlayStyle(Material.TintedOverlay)
        self.update()

    def overlayColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.overlayColor.isValid():
            return self.foregroundColor()
        return self.d.overlayColor

    def setDisabledForegroundColor(self, color: QColor) -> void:
        self.d.disabledColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.update()

    def disabledForegroundColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.disabledColor.isValid():
            return QtMaterialStyle.instance().themeColor("disabled")
        else:
            return self.d.disabledColor

    def setDisabledBackgroundColor(self, color: QColor) -> void:
        self.d.disabledBackgroundColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.update()

    def disabledBackgroundColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.disabledBackgroundColor.isValid():
            return QtMaterialStyle.instance().themeColor("disabled3")
        else:
            return self.d.disabledBackgroundColor

    def setFontSize(self, size: qreal) -> void:
        self.d.fontSize = size

        f = QFont(self.font())
        f.setPointSizeF(size)
        self.setFont(f)

        self.update()

    def fontSize(self) -> qreal:
        return self.d.fontSize

    def setHaloVisible(self, visible: bool) -> void:
        self.d.haloVisible = visible
        self.update()

    def isHaloVisible(self) -> bool:
        return self.d.haloVisible

    def setOverlayStyle(self, style: Material.OverlayStyle) -> void:
        self.d.overlayStyle = style
        self.update()

    def overlayStyle(self) -> Material.OverlayStyle:
        return self.d.overlayStyle

    def setRippleStyle(self, style: Material.RippleStyle) -> void:
        self.d.rippleStyle = style

    def rippleStyle(self) -> Material.RippleStyle:
        return self.d.rippleStyle

    def setIconPlacement(self, placement: Material.ButtonIconPlacement) -> void:
        self.d.iconPlacement = placement
        self.update()

    def iconPlacement(self) -> Material.ButtonIconPlacement:
        return self.d.iconPlacement

    def setCornerRadius(self, radius: qreal) -> void:
        self.d.cornerRadius = radius
        self.updateClipPath()
        self.update()

    def cornerRadius(self) -> qreal:
        return self.d.cornerRadius

    def setBackgroundMode(self, mode: Qt.BGMode) -> void:
        self.d.bgMode = mode
        self.d.stateMachine.setupProperties()

    def backgroundMode(self) -> Qt.BGMode:
        return self.d.bgMode

    def setBaseOpacity(self, opacity: qreal) -> void:
        self.d.baseOpacity = opacity
        self.d.stateMachine.setupProperties()

    def baseOpacity(self) -> qreal:
        return self.d.baseOpacity

    def setCheckable(self, value: bool) -> void:
        self.d.stateMachine.updateCheckedStatus()

        QPushButton.setCheckable(value)

    def setHasFixedRippleRadius(self, value: bool) -> void:
        self.d.useFixedRippleRadius = value

    def hasFixedRippleRadius(self) -> bool:
        return self.d.useFixedRippleRadius

    def setFixedRippleRadius(self, radius: qreal) -> void:
        self.d.fixedRippleRadius = radius
        self.setHasFixedRippleRadius(true)

    def setTextAlignment(self, alignment: Qt.Alignment) -> void:
        self.d.textAlignment = alignment

    def textAlignment(self) -> Qt.Alignment:
        return self.d.textAlignment

    def sizeHint(self) -> QSize:
        self.ensurePolished()

        label = QSize(self.fontMetrics().size(Qt.TextSingleLine, self.text()))

        w: int = 20 + label.width()
        h: int = label.height()
        if not self.icon().isNull():
            w += self.iconSize().width() + QtMaterialFlatButton.IconPadding
            h = max(h, self.iconSize().height())

        return QSize(w, 20 + h)

    def checkStateSet(self) -> void:
        self.d.stateMachine.updateCheckedStatus()

        QPushButton.checkStateSet()

    def mousePressEvent(self, event: QMouseEvent) -> void:
        if Material.NoRipple != self.d.rippleStyle:

            if Material.CenteredRipple == self.d.rippleStyle:
                pos = self.rect().center()
            else:
                pos = event.pos()

            if self.d.useFixedRippleRadius:
                radiusEndValue = self.d.fixedRippleRadius
            else:
                radiusEndValue = self.width() / 2

            ripple = QtMaterialRipple(pos)

            ripple.setRadiusEndValue(radiusEndValue)
            ripple.setOpacityStartValue(0.35)
            ripple.setColor(self.foregroundColor())
            ripple.radiusAnimation().setDuration(600)
            ripple.opacityAnimation().setDuration(1300)
            self.d.rippleOverlay.addRipple(ripple)

        QPushButton.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> void:
        QPushButton.mouseReleaseEvent(self, event)

        self.d.stateMachine.updateCheckedStatus()

    def resizeEvent(self, event: QResizeEvent) -> void:
        QPushButton.resizeEvent(self, event)

        self.updateClipPath()

    def paintEvent(self, event: QPaintEvent) -> void:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cr: qreal = self.d.cornerRadius

        if cr > 0:
            path = QPainterPath()
            path.addRoundedRect(self.rect(), cr, cr)

            painter.setClipPath(path)
            painter.setClipping(true)

        self.paintBackground(painter)
        self.paintHalo(painter)

        painter.setOpacity(1)
        painter.setClipping(false)

        self.paintForeground(painter)

    def paintBackground(self, painter: QPainter) -> void:
        overlayOpacity: qreal = self.d.stateMachine.overlayOpacity()
        checkedProgress: qreal = self.d.stateMachine.checkedOverlayProgress()

        if Qt.OpaqueMode == self.d.bgMode:
            brush = QBrush()
            brush.setStyle(Qt.SolidPattern)
            if self.isEnabled():
                brush.setColor(self.backgroundColor())
            else:
                brush.setColor(self.disabledBackgroundColor())
            painter.setOpacity(1)
            painter.setBrush(brush)
            painter.setPen(Qt.NoPen)
            painter.drawRect(self.rect())

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        painter.setPen(Qt.NoPen)

        if not self.isEnabled():
            return

        if (Material.NoOverlay != self.d.overlayStyle) and (overlayOpacity > 0):
            if Material.TintedOverlay == self.d.overlayStyle:
                brush.setColor(self.overlayColor())
            else:
                brush.setColor(Qt.gray)

            painter.setOpacity(overlayOpacity)
            painter.setBrush(brush)
            painter.drawRect(self.rect())

        if self.isCheckable() and checkedProgress > 0:
            q: qreal = 0.45 if Qt.TransparentMode == self.d.bgMode else 0.7
            brush.setColor(self.foregroundColor())
            painter.setOpacity(q * checkedProgress)
            painter.setBrush(brush)
            r = QRect(self.rect())
            r.setHeight(r.height() * checkedProgress)
            painter.drawRect(r)

    def paintHalo(self, painter: QPainter) -> void:
        if not self.d.haloVisible:
            return

        opacity: qreal = self.d.stateMachine.haloOpacity()
        s: qreal = (
            self.d.stateMachine.haloScaleFactor() * self.d.stateMachine.haloSize()
        )
        radius: qreal = self.width() * s

        if self.isEnabled() and opacity > 0:
            brush = QBrush()
            brush.setStyle(Qt.SolidPattern)
            brush.setColor(self.foregroundColor())
            painter.setOpacity(opacity)
            painter.setBrush(brush)
            painter.setPen(Qt.NoPen)
            center = self.rect().center()
            painter.drawEllipse(center, radius, radius)

    def paintForeground(self, painter: QPainter) -> void:
        if self.isEnabled():
            painter.setPen(self.foregroundColor())
            progress: qreal = self.d.stateMachine.checkedOverlayProgress()
            if self.isCheckable() and progress > 0:
                source: QColor = self.foregroundColor()
                dest: QColor = (
                    Qt.white
                    if Qt.TransparentMode == self.d.bgMode
                    else self.backgroundColor()
                )

                def COLOR_INTERPOLATE(CH):
                    _source = getattr(source, CH)
                    _dest = getattr(dest, CH)
                    return (1 - progress) * _source() + progress * _dest()

                if qFuzzyCompare(1, progress):
                    painter.setPen(dest)
                else:
                    painter.setPen(
                        QColor(
                            COLOR_INTERPOLATE("red"),
                            COLOR_INTERPOLATE("green"),
                            COLOR_INTERPOLATE("blue"),
                            COLOR_INTERPOLATE("alpha"),
                        )
                    )

        else:
            painter.setPen(self.disabledForegroundColor())

        if self.icon().isNull():
            if Qt.AlignLeft == self.d.textAlignment:
                painter.drawText(
                    self.rect().adjusted(12, 0, 0, 0),
                    Qt.AlignLeft | Qt.AlignVCenter,
                    self.text(),
                )
            else:
                painter.drawText(self.rect(), Qt.AlignCenter, self.text())

            return

        textSize = QSize(self.fontMetrics().size(Qt.TextSingleLine, self.text()))
        base = QSize(self.size() - textSize)

        iw: int = self.iconSize().width() + self.IconPadding
        pos = QPoint(
            12 if Qt.AlignLeft == self.d.textAlignment else (base.width() - iw) / 2, 0
        )

        textGeometry = QRect(pos + QPoint(0, base.height() / 2), textSize)
        iconGeometry = QRect(
            pos + QPoint(0, (self.height() - self.iconSize().height()) / 2),
            self.iconSize(),
        )

        if Material.LeftIcon == self.d.iconPlacement:
            textGeometry.translate(iw, 0)
        else:
            iconGeometry.translate(textSize.width() + self.IconPadding, 0)

        painter.drawText(textGeometry, Qt.AlignCenter, self.text())

        pixmap: QPixmap = self.icon().pixmap(self.iconSize())
        icon = QPainter(pixmap)
        icon.setCompositionMode(QPainter.CompositionMode_SourceIn)
        icon.fillRect(pixmap.rect(), painter.pen().color())
        painter.drawPixmap(iconGeometry, pixmap)

    def updateClipPath(self) -> void:
        radius: qreal = self.d.cornerRadius

        path = QPainterPath()
        path.addRoundedRect(self.rect(), radius, radius)
        self.d.rippleOverlay.setClipPath(path)

    _foregroundColor = Q_PROPERTY(QColor, fset=setForegroundColor, fget=foregroundColor)
    _backgroundColor = Q_PROPERTY(QColor, fset=setBackgroundColor, fget=backgroundColor)
    _overlayColor = Q_PROPERTY(QColor, fset=setOverlayColor, fget=overlayColor)
    _disabledForegroundColor = Q_PROPERTY(
        QColor, fset=setDisabledForegroundColor, fget=disabledForegroundColor
    )
    _disabledBackgroundColor = Q_PROPERTY(
        QColor, fset=setDisabledBackgroundColor, fget=disabledBackgroundColor
    )
    _fontSize = Q_PROPERTY(qreal, fset=setFontSize, fget=fontSize)
