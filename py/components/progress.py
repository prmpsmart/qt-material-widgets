from .lib.qtmaterial import *


class QtMaterialProgress:
    ...


class QtMaterialProgressDelegate(QObject):
    def __init__(self, parent: QtMaterialProgress):
        QObject.__init__(self, parent)
        self.m_progress = parent
        self.m_offset = qreal(0)

    def setOffset(self, offset: qreal) -> void:
        self.m_offset = offset
        self.m_progress.update()

    def offset(self) -> qreal:
        return self.m_offset

    _offset = Q_PROPERTY(qreal, fset=setOffset, fget=offset)


class QtMaterialProgressPrivate:
    def __init__(self, q: QtMaterialProgress):
        self.q: QtMaterialProgress = q
        self.delegate: QtMaterialProgressDelegate = None
        self.progressType: Material = None
        self.progressColor: QColor = None
        self.backgroundColor: QColor = None
        self.useThemeColors: bool = None

    def init(self) -> void:
        self.delegate = QtMaterialProgressDelegate(self.q)
        self.progressType = Material.IndeterminateProgress
        self.useThemeColors = true

        animation = QPropertyAnimation(self.q)
        animation.setPropertyName(b"_offset")
        animation.setTargetObject(self.delegate)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.setDuration(1000)

        animation.setLoopCount(-1)

        animation.start()


class QtMaterialProgress(QProgressBar):
    def __init__(self, parent: QWidget = None):
        QProgressBar.__init__(self, parent)
        self.d = QtMaterialProgressPrivate(self)
        self.d.init()

    def setProgressType(self, type: Material.ProgressType) -> void:
        self.d.progressType = type
        self.update()

    def progressType(self) -> Material.ProgressType:
        return self.d.progressType

    def setUseThemeColors(self, state: bool) -> void:
        if self.d.useThemeColors == state:
            return

        self.d.useThemeColors = state
        self.update()

    def useThemeColors(self) -> bool:
        return self.d.useThemeColors

    def setProgressColor(self, color: QColor) -> void:
        self.d.progressColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.update()

    def progressColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.progressColor.isValid():
            return QtMaterialStyle.instance().themeColor("primary1")
        else:
            return self.d.progressColor

    def setBackgroundColor(self, color: QColor) -> void:
        self.d.backgroundColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.update()

    def backgroundColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.backgroundColor.isValid():
            return QtMaterialStyle.instance().themeColor("border")
        else:
            return self.d.backgroundColor

    def paintEvent(self, event: QPaintEvent) -> void:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(
            self.backgroundColor()
            if self.isEnabled()
            else QtMaterialStyle.instance().themeColor("disabled")
        )
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.addRoundedRect(0, self.height() / 2 - 3, self.width(), 6, 3, 3)
        painter.setClipPath(path)

        painter.drawRect(0, 0, self.width(), self.height())

        if self.isEnabled():
            brush.setColor(self.progressColor())
            painter.setBrush(brush)

            if Material.IndeterminateProgress == self.d.progressType:
                painter.drawRect(
                    self.d.delegate.offset() * self.width() * 2 - self.width(),
                    0,
                    self.width(),
                    self.height(),
                )
            else:
                p: qreal = (
                    self.width()
                    * (self.value() - self.minimum())
                    / (self.maximum() - self.minimum())
                )
                painter.drawRect(0, 0, p, self.height())

    _progressColor = Q_PROPERTY(QColor, fset=setProgressColor, fget=progressColor)
    _backgroundColor = Q_PROPERTY(QColor, fset=setProgressColor, fget=backgroundColor)
