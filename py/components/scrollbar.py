from .lib.qtmaterial import *


class QtMaterialScrollBar:
    ...


class QtMaterialScrollBarStateMachine(QStateMachine):
    def __init__(self, parent: QtMaterialScrollBar) -> None:
        QStateMachine.__init__(self, parent)

        self.m_scrollBar = parent
        self.m_focusState = QState()
        self.m_blurState = QState()
        self.m_opacity = qreal(0)

        self.addState(self.m_focusState)
        self.addState(self.m_blurState)
        self.setInitialState(self.m_blurState)

        transition = QEventTransition(parent, QEvent.Enter)
        transition.setTargetState(self.m_focusState)
        self.m_blurState.addTransition(transition)

        transition = QEventTransition(parent, QEvent.Leave)
        transition.setTargetState(self.m_blurState)
        self.m_focusState.addTransition(transition)

        self.m_focusState.assignProperty(self, "opacity", 1)
        self.m_blurState.assignProperty(self, "opacity", 0)

        animation = QPropertyAnimation(self, b"opacity", self)
        animation.setDuration(340)
        self.addDefaultAnimation(animation)

    def setOpacity(self, opacity: qreal) -> void:
        self.m_opacity = opacity
        self.m_scrollBar.update()

    def opacity(self) -> qreal:
        return self.m_opacity

    _opacity = Q_PROPERTY(qreal, fset=setOpacity, fget=opacity)


class QtMaterialScrollBarPrivate:
    def __init__(self, q: QtMaterialScrollBar):
        self.q :QtMaterialScrollBar= q

        self.backgroundColor = QColor("blue")
        self.sliderColor = QColor()
        self.canvasColor = QColor()
        self.hideOnMouseOut :bool= None
        self.useThemeColors :bool= None

    def init(self) -> void:
        self.stateMachine = QtMaterialScrollBarStateMachine(self.q)
        self.hideOnMouseOut = true
        self.useThemeColors = true

        self.q.setMouseTracking(true)
        self.q.setStyle(QtMaterialStyle.instance())
        self.q.setStyleSheet(
            """
        QtMaterialScrollBar:vertical { margin: 0 }
        QtMaterialScrollBar.add-line:vertical { height: 0; margin: 0; }
        QtMaterialScrollBar.sub-line:vertical { height: 0; margin: 0 }"""
        )

        self.stateMachine.start()


class QtMaterialScrollBar(QScrollBar):
    def __init__(self, parent: QWidget = None, d: QtMaterialScrollBarPrivate = None):
        QScrollBar.__init__(self, parent)
        self.d = d or QtMaterialScrollBarPrivate(self)
        self.d.init()

    def sizeHint(self) -> QSize:
        if Qt.Horizontal == self.orientation():
            return QSize(1, 10)
        else:
            return QSize(10, 1)

    def setUseThemeColors(self, value: bool) -> void:
        if self.d.useThemeColors == value:
            return

        self.d.useThemeColors = value
        self.update()

    def useThemeColors(self) -> bool:
        return self.d.useThemeColors

    def setCanvasColor(self, color: QColor) -> void:
        self.d.canvasColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.update()

    def canvasColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.canvasColor.isValid():
            return self.parentWidget().palette().color(self.backgroundRole())
        else:
            return self.d.canvasColor

    def setBackgroundColor(self, color: QColor) -> void:
        self.d.backgroundColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.update()

    def backgroundColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.backgroundColor.isValid():
            QtMaterialStyle.instance().themeColor("border")
        else:
            return self.d.backgroundColor

    def setSliderColor(self, color: QColor) -> void:
        self.d.sliderColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.update()

    def sliderColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.sliderColor.isValid():
            return QtMaterialStyle.instance().themeColor("primary1")
        else:
            return self.d.sliderColor

    def setHideOnMouseOut(self, value: bool) -> void:
        self.d.hideOnMouseOut = value
        self.update()

    def hideOnMouseOut(self) -> bool:
        return self.d.hideOnMouseOut

    def paintEvent(self, event: QPaintEvent) -> void:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(self.rect(), self.canvasColor())

        x, y, w, h = self.rect().getRect()

        margins = QMargins(2, 2, 2, 2)

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(self.backgroundColor())
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)

        if self.d.hideOnMouseOut:
            painter.setOpacity(self.d.stateMachine.opacity)

        trimmed = QRect(self.rect().marginsRemoved(margins))

        path = QPainterPath()
        path.addRoundedRect(trimmed, 3, 3)
        painter.setClipPath(path)

        painter.drawRect(trimmed)

        q: qreal = (
            (w if Qt.Horizontal == self.orientation() else h) / self.maximum()
            - self.minimum()
            + self.pageStep()
            - 1
        )

        handle: QRect = (
            QRect(self.sliderPosition() * q, y, self.pageStep() * q, h)
            if Qt.Horizontal == self.orientation()
            else QRect(x, self.sliderPosition() * q, w, self.pageStep() * q)
        )

        brush.setColor(self.sliderColor())
        painter.setBrush(brush)

        painter.drawRoundedRect(handle, 9, 9)
        painter.end()

    _canvasColor = Q_PROPERTY(QColor, fset=setCanvasColor, fget=canvasColor)
    _backgroundColor = Q_PROPERTY(QColor, fset=setBackgroundColor, fget=backgroundColor)
    _sliderColor = Q_PROPERTY(QColor, fset=setSliderColor, fget=sliderColor)
