from .core._core import *


class QMaterialCircularProgressDelegate(QObject):
    def __init__(self, parent: "QMaterialCircularProgress") -> None:
        QObject.__init__(self, parent)

        self.m_progress = parent
        self.m_dashOffset = float(0)
        self.m_dashLength = float(89)
        self.m_angle = int(0)

    def setDashOffset(self, offset: float) -> None:
        self.m_dashOffset = offset
        self.m_progress.update()

    def dashOffset(self) -> float:
        return self.m_dashOffset

    def setDashLength(self, length: float) -> None:
        self.m_dashLength = length
        self.m_progress.update()

    def dashLength(self) -> float:
        return self.m_dashLength

    def setAngle(self, angle: int) -> None:
        self.m_angle = angle
        self.m_progress.update()

    def angle(self) -> int:
        return self.m_angle

    _dashOffset = Property(float, fset=setDashOffset, fget=dashOffset)
    _dashLength = Property(float, fset=setDashLength, fget=dashLength)
    _angle = Property(int, fset=setAngle, fget=angle)


class QMaterialCircularProgress(QProgressBar):
    def __init__(self, parent: QWidget = None):
        QProgressBar.__init__(self, parent)

        self.m_delegate = QMaterialCircularProgressDelegate(self)
        self.m_progressType = Material.IndeterminateProgress
        self.m_penWidth = 6.25
        self.m_size = 64
        self.m_useThemeColors = True

        self.setSizePolicy(
            QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        )

        group = QParallelAnimationGroup(self)
        group.setLoopCount(-1)

        animation = QPropertyAnimation(self)
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

        animation = QPropertyAnimation(self)
        animation.setPropertyName(b"_dashOffset")
        animation.setTargetObject(self.m_delegate)
        animation.setEasingCurve(QEasingCurve.InOutSine)
        animation.setStartValue(0)
        animation.setKeyValueAt(0.15, 0)
        animation.setKeyValueAt(0.6, -7)
        animation.setKeyValueAt(0.7, -7)
        animation.setEndValue(-25)
        animation.setDuration(2050)

        group.addAnimation(animation)

        animation = QPropertyAnimation(self)
        animation.setPropertyName(b"_angle")
        animation.setTargetObject(self.m_delegate)
        animation.setStartValue(0)
        animation.setEndValue(719)
        animation.setDuration(2050)

        group.addAnimation(animation)

        group.start()

    def setProgressType(self, type: Material.ProgressType) -> None:
        self.m_progressType = type
        self.update()

    def progressType(self) -> Material.ProgressType:
        return self.m_progressType

    def setUseThemeColors(self, value: bool) -> None:
        if self.m_useThemeColors == value:
            return

        self.m_useThemeColors = value
        self.update()

    def useThemeColors(self) -> bool:
        return self.m_useThemeColors

    def setLineWidth(self, width: float) -> None:
        self.m_penWidth = width
        self.update()
        self.updateGeometry()

    def lineWidth(self) -> float:
        return self.m_penWidth

    def setSize(self, size: int) -> None:
        self.m_size = size
        self.update()
        self.updateGeometry()

    def size(self) -> int:
        return self.m_size

    def setColor(self, color: QColor) -> None:
        self.m_color = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.update()

    def color(self) -> QColor:
        if self.m_useThemeColors or not self.m_color.isValid():
            return QMaterialStyle.instance().themeColor("primary1")
        else:
            return self.m_color

    def sizeHint(self) -> QSize:
        s: float = self.m_size + self.m_penWidth + 8
        return QSize(s, s)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen()

        if not self.isEnabled():
            pen.setCapStyle(Qt.RoundCap)
            pen.setWidthF(self.m_penWidth)
            pen.setColor(QMaterialStyle.instance().themeColor("border"))
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

        if Material.IndeterminateProgress == self.m_progressType:
            painter.translate(self.width() / 2, self.height() / 2)
            painter.rotate(self.m_delegate.angle())

        pen.setCapStyle(Qt.RoundCap)
        pen.setWidthF(self.m_penWidth)
        pen.setColor(self.color())

        if Material.IndeterminateProgress == self.m_progressType:
            pattern: List[float] = [
                self.m_delegate.dashLength() * self.m_size / 50,
                30 * self.m_size / 50,
            ]

            pen.setDashOffset(self.m_delegate.dashOffset() * self.m_size / 50)
            pen.setDashPattern(pattern)

            painter.setPen(pen)

            painter.drawEllipse(QPoint(0, 0), self.m_size / 2, self.m_size / 2)

        else:
            painter.setPen(pen)

            x: float = (self.width() - self.m_size) / 2
            y: float = (self.height() - self.m_size) / 2

            a: float = (
                360
                * (self.value() - self.minimum())
                / (self.maximum() - self.minimum())
            )

            path = QPainterPath()
            path.arcMoveTo(x, y, self.m_size, self.m_size, 0)
            path.arcTo(x, y, self.m_size, self.m_size, 0, a)

            painter.drawPath(path)

    _lineWidth = Property(float, fset=setLineWidth, fget=lineWidth)
    _size = Property(float, fset=setSize, fget=size)
    _color = Property(QColor, fset=setColor, fget=color)
