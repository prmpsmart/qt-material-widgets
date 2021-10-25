from .lib.qtmaterial import *


class QtMaterialTextField:
    ...


class QtMaterialTextFieldLabel:
    ...


class QtMaterialTextFieldStateMachine(QStateMachine):
    def __init__(self, parent: QtMaterialTextField):
        QStateMachine.__init__(self, parent)

        self.m_textField = parent
        self.m_normalState = QState()
        self.m_focusedState = QState()
        self.m_label = QtMaterialTextFieldLabel(parent)
        self.m_offsetAnimation = QPropertyAnimation(self)
        self.m_colorAnimation = QPropertyAnimation(self)
        self.m_progress = qreal(0.0)

        self.addState(self.m_normalState)
        self.addState(self.m_focusedState)

        self.setInitialState(self.m_normalState)

        transition = QEventTransition(parent, QEvent.FocusIn)
        transition.setTargetState(self.m_focusedState)
        self.m_normalState.addTransition(transition)

        animation = QPropertyAnimation(self, b"progress", self)
        animation.setEasingCurve(QEasingCurve.InCubic)
        animation.setDuration(310)
        transition.addAnimation(animation)

        transition = QEventTransition(parent, QEvent.FocusOut)
        transition.setTargetState(self.m_normalState)
        self.m_focusedState.addTransition(transition)

        animation = QPropertyAnimation(self, b"progress", self)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        animation.setDuration(310)
        transition.addAnimation(animation)

        self.m_normalState.assignProperty(self, "progress", 0)
        self.m_focusedState.assignProperty(self, "progress", 1)

        self.setupProperties()

        self.m_textField.textChanged.connect(self.setupProperties)

    def setLabel(self, label: QtMaterialTextFieldLabel) -> void:
        if self.m_label:
            del self.m_label

        if self.m_offsetAnimation:
            self.removeDefaultAnimation(self.m_offsetAnimation)
            del self.m_offsetAnimation

        if self.m_colorAnimation:
            self.removeDefaultAnimation(self.m_colorAnimation)
            del self.m_colorAnimation

        self.m_label = label

        if self.m_label:
            self.m_offsetAnimation = QPropertyAnimation(self.m_label, "offset", self)
            self.m_offsetAnimation.setDuration(210)
            self.m_offsetAnimation.setEasingCurve(QEasingCurve.OutCubic)
            self.addDefaultAnimation(self.m_offsetAnimation)

            self.m_colorAnimation = QPropertyAnimation(self.m_label, "color", self)
            self.m_colorAnimation.setDuration(210)
            self.addDefaultAnimation(self.m_colorAnimation)

        self.setupProperties()

    def setProgress(self, progress: qreal) -> void:
        self.m_progress = progress
        self.m_textField.update()

    def progress(self) -> qreal:
        return self.m_progress

    def setupProperties(self) -> void:
        if self.m_label:
            m: int = self.m_textField.textMargins().top()

            if self.m_textField.text():
                self.m_normalState.assignProperty(
                    self.m_label, "offset", QPointF(0, 26)
                )
            else:
                self.m_normalState.assignProperty(
                    self.m_label, "offset", QPointF(0, 0 - m)
                )

            self.m_focusedState.assignProperty(
                self.m_label, "offset", QPointF(0, 0 - m)
            )
            self.m_focusedState.assignProperty(
                self.m_label, "color", self.m_textField.inkColor()
            )
            self.m_normalState.assignProperty(
                self.m_label, "color", self.m_textField.labelColor()
            )

            if 0 != self.m_label.offset().y() and not self.m_textField.text():
                self.m_label.setOffset(QPointF(0, 0 - m))
            elif (
                not self.m_textField.hasFocus()
                and self.m_label.offset().y() <= 0
                and self.m_textField.text()
            ):
                self.m_label.setOffset(QPointF(0, 26))

        self.m_textField.update()

    _progress = Q_PROPERTY(qreal, fset=setProgress, fget=progress)


class QtMaterialTextFieldPrivate:
    def __init__(self, q: QtMaterialTextField):
        self.q: QtMaterialTextField = q
        self.textColor = QColor()
        self.labelColor = QColor()
        self.inkColor = QColor()
        self.inputLineColor = QColor()
        self.labelString = QString()
        self.labelFontSize: qreal = 9.5
        self.showLabel: bool = false
        self.showInputLine: bool = true
        self.useThemeColors: bool = true
        self.label: QtMaterialTextFieldLabel = None
        self.stateMachine: QtMaterialTextFieldStateMachine = None

    def init(self):
        self.label = QtMaterialTextFieldLabel(self.q)
        self.stateMachine = QtMaterialTextFieldStateMachine(self.q)

        self.q.setFrame(false)
        self.q.setStyle(QtMaterialStyle.instance())
        self.q.setAttribute(Qt.WA_Hover)
        self.q.setMouseTracking(true)
        self.q.setTextMargins(0, 2, 0, 4)

        self.q.setFont(QFont("Roboto", 11, QFont.Normal))

        self.stateMachine.start()
        QCoreApplication.processEvents()


class QtMaterialTextField(QLineEdit):
    def __init__(self, parent: QWidget = None, p: bool = 1):
        QLineEdit.__init__(self, parent)

        if p:
            self.d = QtMaterialTextFieldPrivate(self)
            self.d.init()

    def setUseThemeColors(self, value: bool) -> void:
        if self.d.useThemeColors == value:
            return

        self.d.useThemeColors = value
        self.d.stateMachine.setupProperties()

    def useThemeColors(self) -> bool:
        return self.d.useThemeColors

    def setShowLabel(self, value: bool) -> void:
        if self.d.showLabel == value:
            return

        self.d.showLabel = value

        if not self.d.label and value:
            self.d.label = QtMaterialTextFieldLabel(self)
            self.d.stateMachine.setLabel(self.d.label)

        if value:
            self.setContentsMargins(0, 23, 0, 0)
        else:
            self.setContentsMargins(0, 0, 0, 0)

    def hasLabel(self) -> bool:
        return self.d.showLabel

    def setLabelFontSize(self, size: qreal) -> void:
        self.d.labelFontSize = size

        if self.d.label:
            font = QFont(self.d.label.font())
            font.setPointSizeF(size)
            self.d.label.setFont(font)
            self.d.label.update()

    def labelFontSize(self) -> qreal:
        return self.d.labelFontSize

    def setLabel(self, label: QString) -> void:
        self.d.labelString = label
        self.setShowLabel(true)
        self.d.label.update()

    def label(self) -> QString:
        return self.d.labelString

    def setTextColor(self, color: QColor) -> void:
        self.d.textColor = color
        self.setStyleSheet(QString("QLineEdit { color: %s }").arg(color.name()))
        MATERIAL_DISABLE_THEME_COLORS(self)
        self.d.stateMachine.setupProperties()

    def textColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.textColor.isValid():
            return QtMaterialStyle.instance().themeColor("text")
        else:
            return self.d.textColor

    def setLabelColor(self, color: QColor) -> void:
        self.d.labelColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.d.stateMachine.setupProperties()

    def labelColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.labelColor.isValid():
            return QtMaterialStyle.instance().themeColor("accent3")
        else:
            return self.d.labelColor

    def setInkColor(self, color: QColor) -> void:
        self.d.inkColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.d.stateMachine.setupProperties()

    def inkColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.inkColor.isValid():
            return QtMaterialStyle.instance().themeColor("primary1")
        else:
            return self.d.inkColor

    def setInputLineColor(self, color: QColor) -> void:
        self.d.inputLineColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.d.stateMachine.setupProperties()

    def inputLineColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.inputLineColor.isValid():
            return QtMaterialStyle.instance().themeColor("border")
        else:
            return self.d.inputLineColor

    def setShowInputLine(self, value: bool) -> void:
        if self.d.showInputLine == value:
            return

        self.d.showInputLine = value
        self.update()

    def hasInputLine(self) -> bool:
        return self.d.showInputLine

    def event(self, event: QEvent) -> bool:
        if event.type() in [QEvent.Resize, QEvent.Move]:
            if self.d.label:
                self.d.label.setGeometry(self.rect())

        return QLineEdit.event(self, event)

    def paintEvent(self, event: QPaintEvent) -> void:
        QLineEdit.paintEvent(self, event)
        try:
            progress: qreal = self.d.stateMachine.progress()
        except:
            return

        painter = QPainter(self)

        if self.text().isEmpty() and progress < 1:
            painter.setOpacity(1 - progress)
            painter.fillRect(
                self.rect(), self.parentWidget().palette().color(self.backgroundRole())
            )

        y: int = self.height() - 1
        wd: int = self.width() - 5

        if self.d.showInputLine:
            pen = QPen()
            pen.setWidth(1)
            pen.setColor(self.inputLineColor())

            if not self.isEnabled():
                pen.setStyle(Qt.DashLine)

            painter.setPen(pen)
            painter.setOpacity(1)
            painter.drawLine(QLineF(2.5, y, wd, y))

            brush = QBrush()
            brush.setStyle(Qt.SolidPattern)
            brush.setColor(self.inkColor())

            if progress > 0:
                painter.setPen(Qt.NoPen)
                painter.setBrush(brush)
                w: int = (1 - progress) * (wd / 2)
                painter.drawRect(w + 2.5, self.height() - 2, wd - w * 2, 2)

    _textColor = Q_PROPERTY(QColor, fset=setTextColor, fget=textColor)
    _inkColor = Q_PROPERTY(QColor, fset=setInkColor, fget=inkColor)
    _inputLineColor = Q_PROPERTY(QColor, fset=setInputLineColor, fget=inputLineColor)


class QtMaterialTextFieldLabel(QWidget):
    def __init__(self, parent: QtMaterialTextField):
        QWidget.__init__(self, parent)

        self.m_textField = parent
        self.m_scale = qreal(1)
        self.m_posX = qreal(0)
        self.m_posY = qreal(26)
        self.m_color = QColor(parent.labelColor())

        font = QFont("Roboto", parent.labelFontSize(), QFont.Medium)
        font.setLetterSpacing(QFont.PercentageSpacing, 102)
        self.setFont(font)

    def setScale(self, scale: qreal) -> void:
        self.m_scale = scale
        self.update()

    def scale(self) -> qreal:
        return self.m_scale

    def setOffset(self, pos: QPointF) -> void:
        self.m_posX = pos.x()
        self.m_posY = pos.y()
        self.update()

    def offset(self) -> QPointF:
        return QPointF(self.m_posX, self.m_posY)

    def setColor(self, color: QColor) -> void:
        self.m_color = color
        self.update()

    def color(self) -> QColor:
        return self.m_color

    def paintEvent(self, event: QPaintEvent) -> void:

        if not self.m_textField.hasLabel():
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.scale(self.m_scale, self.m_scale)
        painter.setPen(self.m_color)
        painter.setOpacity(1)

        pos = QPointF(2 + self.m_posX, self.height() - 36 + self.m_posY)
        painter.drawText(pos.x(), pos.y(), self.m_textField.label())

    _scale = Q_PROPERTY(qreal, fset=setScale, fget=scale)
    _offset = Q_PROPERTY(QPointF, fset=setOffset, fget=offset)
    _color = Q_PROPERTY(QColor, fset=setColor, fget=color)
