from .lib.qtmaterial import *


class QtMaterialCircularProgressDelegate(QObject):
    def __init__(self, parent: "QtMaterialCircularProgress") -> None:
        QObject.__init__(self, parent)

        self.m_progress = parent
        self.m_dashOffset = qreal(0)
        self.m_dashLength = qreal(89)
        self.m_angle = int(0)

    def setDashOffset(self, offset: qreal) -> void:
        self.m_dashOffset = offset
        self.m_progress.update()

    def dashOffset(self) -> qreal:
        return self.m_dashOffset

    def setDashLength(self, length: qreal) -> void:
        self.m_dashLength = length
        self.m_progress.update()

    def dashLength(self) -> qreal:
        return self.m_dashLength

    def setAngle(self, angle: int) -> void:
        self.m_angle = angle
        self.m_progress.update()

    def angle(self) -> int:
        return self.m_angle

    _dashOffset = Q_PROPERTY(qreal, fset=setDashOffset, fget=dashOffset)
    _dashLength = Q_PROPERTY(qreal, fset=setDashLength, fget=dashLength)
    _angle = Q_PROPERTY(int, fset=setAngle, fget=angle)


class QtMaterialCircularProgressPrivate:
    def __init__(self, q: "QtMaterialCircularProgress"):
        self.q: QtMaterialCircularProgress = q
        self.delegate: QtMaterialCircularProgressDelegate = None
        self.progressType: Material = None
        self.color: QColor = None
        self.penWidth: qreal = None
        self.size: int = None
        self.useThemeColors: bool = None

    def init(self) -> void:
        q = self.q

        self.delegate = QtMaterialCircularProgressDelegate(q)
        self.progressType = Material.IndeterminateProgress
        self.penWidth = 6.25
        self.size = 64
        self.useThemeColors = true

        self.q.setSizePolicy(
            QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        )

        group = QParallelAnimationGroup(q)
        group.setLoopCount(-1)

        animation = QPropertyAnimation(q)
        animation.setPropertyName(b"_dashLength")
        animation.setTargetObject(self.delegate)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.setStartValue(0.1)
        animation.setKeyValueAt(0.15, 0.2)
        animation.setKeyValueAt(0.6, 20)
        animation.setKeyValueAt(0.7, 20)
        animation.setEndValue(20)
        animation.setDuration(2050)

        group.addAnimation(animation)

        animation = QPropertyAnimation(q)
        animation.setPropertyName(b"_dashOffset")
        animation.setTargetObject(self.delegate)
        animation.setEasingCurve(QEasingCurve.InOutSine)
        animation.setStartValue(0)
        animation.setKeyValueAt(0.15, 0)
        animation.setKeyValueAt(0.6, -7)
        animation.setKeyValueAt(0.7, -7)
        animation.setEndValue(-25)
        animation.setDuration(2050)

        group.addAnimation(animation)

        animation = QPropertyAnimation(q)
        animation.setPropertyName(b"_angle")
        animation.setTargetObject(self.delegate)
        animation.setStartValue(0)
        animation.setEndValue(719)
        animation.setDuration(2050)

        group.addAnimation(animation)

        group.start()


class QtMaterialCircularProgress(QProgressBar):
    def __init__(self, parent: QWidget = None):
        QProgressBar.__init__(self, parent)
        self.d = QtMaterialCircularProgressPrivate(self)
        self.d.init()

    def setProgressType(self, type: Material.ProgressType) -> void:
        self.d.progressType = type
        self.update()

    def progressType(self) -> Material.ProgressType:
        return self.d.progressType

    def setUseThemeColors(self, value: bool) -> void:
        if self.d.useThemeColors == value:
            return

        self.d.useThemeColors = value
        self.update()

    def useThemeColors(self) -> bool:
        return self.d.useThemeColors

    def setLineWidth(self, width: qreal) -> void:
        self.d.penWidth = width
        self.update()
        self.updateGeometry()

    def lineWidth(self) -> qreal:
        return self.d.penWidth

    def setSize(self, size: int) -> void:
        self.d.size = size
        self.update()
        self.updateGeometry()

    def size(self) -> int:
        return self.d.size

    def setColor(self, color: QColor) -> void:
        self.d.color = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.update()

    def color(self) -> QColor:
        if self.d.useThemeColors or not self.d.color.isValid():
            return QtMaterialStyle.instance().themeColor("primary1")
        else:
            return self.d.color

    def sizeHint(self) -> QSize:
        s: qreal = self.d.size + self.d.penWidth + 8
        return QSize(s, s)

    def paintEvent(self, event: QPaintEvent) -> void:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen()

        if not self.isEnabled():
            pen.setCapStyle(Qt.RoundCap)
            pen.setWidthF(self.d.penWidth)
            pen.setColor(QtMaterialStyle.instance().themeColor("border"))
            painter.setPen(pen)
            painter.drawLine(
                self.rect().center() - QPointF(20, 20),
                self.rect().center() + QPointF(20, 20),
            )
            painter.drawLine(
                self.rect().center() + QPointF(20, -20),
                self.rect().center() - QPointF(20, -20),
            )
            return

        if Material.IndeterminateProgress == self.d.progressType:
            painter.translate(self.width() / 2, self.height() / 2)
            painter.rotate(self.d.delegate.angle())

        pen.setCapStyle(Qt.RoundCap)
        pen.setWidthF(self.d.penWidth)
        pen.setColor(self.color())

        if Material.IndeterminateProgress == self.d.progressType:
            pattern: List[qreal] = [
                self.d.delegate.dashLength() * self.d.size / 50,
                30 * self.d.size / 50,
            ]

            pen.setDashOffset(self.d.delegate.dashOffset() * self.d.size / 50)
            pen.setDashPattern(pattern)

            painter.setPen(pen)

            painter.drawEllipse(QPoint(0, 0), self.d.size / 2, self.d.size / 2)

        else:
            painter.setPen(pen)

            x: qreal = (self.width() - self.d.size) / 2
            y: qreal = (self.height() - self.d.size) / 2

            a: qreal = (
                360
                * (self.value() - self.minimum())
                / (self.maximum() - self.minimum())
            )

            path = QPainterPath()
            path.arcMoveTo(x, y, self.d.size, self.d.size, 0)
            path.arcTo(x, y, self.d.size, self.d.size, 0, a)

            painter.drawPath(path)

    _lineWidth = Q_PROPERTY(qreal, fset=setLineWidth, fget=lineWidth)
    _size = Q_PROPERTY(qreal, fset=setSize, fget=size)
    _color = Q_PROPERTY(QColor, fset=setColor, fget=color)
