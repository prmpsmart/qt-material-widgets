from ..core._core import *


class QMaterialCheckableIcon(QWidget):
    SIZE = 24

    def __init__(
        self,
        parent: "QMaterialCheckable",
        icon: Union[QIcon, QPixmap, str] = None,
        size: float = 24,
        opacity: float = 1,
        color: Union[QColor, Qt.GlobalColor] = Qt.black,
    ) -> None:
        QWidget.__init__(self, parent)

        self.m_checkable = parent
        self.m_color = QColor(color)
        self.m_icon = QIcon(icon)
        self.m_iconSize = size
        self.m_opacity = opacity

        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def setIcon(self, icon: QIcon) -> None:
        self.m_icon = QIcon(icon)
        self.update()

    def icon(self) -> QIcon:
        return self.m_icon

    def setColor(self, color: QColor) -> None:
        self.m_color = color
        self.update()

    def color(self) -> QColor:
        return self.m_color

    def setIconSize(self, size: float) -> None:
        self.m_iconSize = size
        self.update()

    def iconSize(self) -> float:
        return self.m_iconSize

    def setOpacity(self, opacity: float) -> None:
        self.m_opacity = opacity
        self.update()

    def opacity(self) -> float:
        return self.m_opacity

    def sizeHint(self) -> QSize:
        return QSize(self.m_iconSize, self.m_iconSize)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setOpacity(self.m_opacity)

        pixmap: QPixmap = self.icon().pixmap(24, 24)

        if not pixmap.isNull():
            p: float = ((self.height()) - self.m_iconSize) / 2
            z: float = self.m_iconSize / 24

            t = QTransform()
            dx = self.m_iconSize

            if self.m_checkable.LabelPositionLeft == self.m_checkable.labelPosition():
                dx = p + self.width() - 42

            painter.setTransform(
                t.translate(dx if self.m_checkable.flipToggle else p, p).scale(z, z)
            )

            painter.setBrush(QBrush(self.color()))
            painter.setPen(QPen(self.color()))
            painter.drawPixmap(0, 0, pixmap)

        painter.end()

    _color = Property(QColor, fget=color, fset=setColor)
    _iconSize = Property(float, fget=iconSize, fset=setIconSize)
    _opacity = Property(float, fget=opacity, fset=setOpacity)
