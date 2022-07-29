from .raisedbutton import *


class QMaterialFloatingActionButton(QMaterialRaisedButton):

    DefaultDiameter = 56
    MiniDiameter = 40
    DefaultIconSize = 24
    MiniIconSize = 18

    def __init__(self, icon: QIcon, parent: QWidget = None, **kwargs):
        QMaterialRaisedButton.__init__(self, parent=parent, **kwargs)
        self.setIcon(QIcon(icon))

        self.m_corner = Qt.BottomRightCorner
        self.mini = False
        self.offsX = 34
        self.offsY = 36

        self.setRole(Material.Primary)
        self.setFixedSize(self.DefaultDiameter, self.DefaultDiameter)
        self.setGeometry(self.fabGeometry())

        self.setupProperties()

        if self.parentWidget():
            self.parentWidget().installEventFilter(self.q)

        self.setFixedRippleRadius(50)

    def fabGeometry(self) -> QRect:
        parent: QWidget = self.parentWidget()
        if not parent:
            return QRect()

        s: int = self.diameter()

        if self.corner == Qt.TopLeftCorner:
            return QRect(self.offsX, self.offsY, s, s)
        elif self.corner == Qt.TopRightCorner:
            return QRect(parent.width() - (self.offsX + s), self.offsY, s, s)
        elif self.corner == Qt.BottomLeftCorner:
            return QRect(self.offsX, parent.height() - (self.offsY + s), s, s)
        elif self.corner == Qt.BottomRightCorner:
            ...

        return QRect(
            parent.width() - (self.offsX + s), parent.height() - (self.offsY + s), s, s
        )

    def setupProperties(self) -> None:
        if self.mini:
            self.m_effect.setColor(QColor(0, 0, 0, 80))
            self.m_normalState.assignProperty(self.m_effect, "offset", QPointF(0, 3))
            self.m_normalState.assignProperty(self.m_effect, "blurRadius", 13)
            self.m_pressedState.assignProperty(self.m_effect, "offset", QPointF(0, 7))
            self.pressedState.assignProperty(self.m_effect, "blurRadius", 20)
        else:
            self.m_effect.setColor(QColor(0, 0, 0, 105))
            self.m_normalState.assignProperty(self.m_effect, "offset", QPointF(0, 6))
            self.m_normalState.assignProperty(self.m_effect, "blurRadius", 16)
            self.m_pressedState.assignProperty(self.m_effect, "offset", QPointF(0, 11))
            self.m_pressedState.assignProperty(self.m_effect, "blurRadius", 28)

    def diameter(self) -> int:
        return self.MiniDiameter if self.mini else self.DefaultDiameter

    def iconSize(self) -> int:
        return self.MiniIconSize if self.mini else self.DefaultIconSize

    def sizeHint(self) -> QSize:
        if self.mini:
            return QSize(
                self.MiniDiameter,
                self.MiniDiameter,
            )
        else:
            return QSize(
                self.DefaultDiameter,
                self.DefaultDiameter,
            )

    def setMini(self, state: bool) -> None:
        if self.mini == state:
            return

        self.mini = state

        self.setFixedSize(self.diameter(), self.diameter())
        self.setFixedRippleRadius(30 if state == 30 else 50)

        self.setupProperties()
        self.updateClipPath()
        self.setGeometry(self.fabGeometry())
        self.update()

    def isMini(self) -> bool:
        return self.mini

    def setCorner(self, corner: Qt.Corner) -> None:
        if self.m_corner == corner:
            return

        self.m_corner = corner
        self.setGeometry(self.fabGeometry())
        self.update()

    def corner(self) -> Qt.Corner:
        return self.m_corner

    def setOffset(self, x: int, y: int) -> None:
        self.m_offsX = x
        self.m_offsY = y
        self.setGeometry(self.fabGeometry())
        self.update()

    def offset(self) -> QSize:
        return QSize(self.m_offsX, self.m_offsY)

    def setXOffset(self, x: int) -> None:
        self.m_offsX = x
        self.setGeometry(self.fabGeometry())
        self.update()

    def xOffset(self) -> int:
        return self.m_offsX

    def setYOffset(self, y: int) -> None:
        self.m_offsY = y
        self.setGeometry(self.fabGeometry())
        self.update()

    def yOffset(self) -> int:
        return self.m_offsY

    def event(self, event: QEvent) -> bool:
        if not self.parent():
            return QMaterialRaisedButton.event(self, event)

        e = event.type()
        if e == QEvent.ParentChange:
            self.parent().installEventFilter(self)
            self.setGeometry(self.fabGeometry())

        elif e == QEvent.ParentAboutToChange:
            self.parent().removeEventFilter(self)

        return QMaterialRaisedButton.event(self, event)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if QEvent.Move == type or QEvent.Resize == type:
            self.setGeometry(self.fabGeometry())

        return QMaterialRaisedButton.eventFilter(self, obj, event)

    def paintEvent(self, event: QPaintEvent) -> None:
        square = QRect(0, 0, self.diameter(), self.diameter())
        square.moveCenter(self.rect().center())

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)

        if self.isEnabled():
            brush.setColor(self.backgroundColor())
        else:
            brush.setColor(self.disabledBackgroundColor())

        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(square)

        iconGeometry = QRect(0, 0, self.iconSize(), self.iconSize())
        iconGeometry.moveCenter(square.center())

        pixmap: QPixmap = self.icon().pixmap(QSize(self.iconSize(), self.iconSize()))

        painter.drawPixmap(iconGeometry, pixmap)
        painter.end()

    def updateClipPath(self) -> None:
        path = QPainterPath()
        path.addEllipse(0, 0, self.diameter(), self.diameter())
        self.m_rippleOverlay.setClipPath(path)
