from .raisedbutton import *


class QtMaterialFloatingActionButtonPrivate(QtMaterialRaisedButtonPrivate):

    DefaultDiameter = 56
    MiniDiameter = 40
    DefaultIconSize = 24
    MiniIconSize = 18

    def __init__(self, q: "QtMaterialFloatingActionButton"):

        self.q: QtMaterialFloatingActionButton = q
        QtMaterialRaisedButtonPrivate.__init__(self, q)

        self.corner: Qt.Corner = None
        self.mini: bool = None
        self.offsX: int = None
        self.offsY: int = None

    def init(self) -> void:
        self.corner = Qt.BottomRightCorner
        self.mini = false
        self.offsX = 34
        self.offsY = 36

        self.q.setRole(Material.Primary)
        self.q.setFixedSize(self.DefaultDiameter, self.DefaultDiameter)
        self.q.setGeometry(self.fabGeometry())

        self.setupProperties()

        if self.q.parentWidget():
            self.q.parentWidget().installEventFilter(self.q)

        self.q.setFixedRippleRadius(50)

    def fabGeometry(self) -> QRect:
        parent: QWidget = self.q.parentWidget()
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

    def setupProperties(self) -> void:
        if self.mini:
            self.effect.setColor(QColor(0, 0, 0, 80))
            self.normalState.assignProperty(self.effect, "offset", QPointF(0, 3))
            self.normalState.assignProperty(self.effect, "blurRadius", 13)
            self.pressedState.assignProperty(self.effect, "offset", QPointF(0, 7))
            self.pressedState.assignProperty(self.effect, "blurRadius", 20)
        else:
            self.effect.setColor(QColor(0, 0, 0, 105))
            self.normalState.assignProperty(self.effect, "offset", QPointF(0, 6))
            self.normalState.assignProperty(self.effect, "blurRadius", 16)
            self.pressedState.assignProperty(self.effect, "offset", QPointF(0, 11))
            self.pressedState.assignProperty(self.effect, "blurRadius", 28)

    def diameter(self) -> int:
        return self.MiniDiameter if self.mini else self.DefaultDiameter

    def iconSize(self) -> int:
        return self.MiniIconSize if self.mini else self.DefaultIconSize


class QtMaterialFloatingActionButton(QtMaterialRaisedButton):
    def __init__(self, icon: QIcon = None, parent: QWidget = None):
        self.d = QtMaterialFloatingActionButtonPrivate(self)
        QtMaterialRaisedButton.__init__(self, d=self.d, parent=parent)
        self.d.init()
        self.setIcon(icon)

    def sizeHint(self) -> QSize:
        if self.d.mini:
            return QSize(
                QtMaterialFloatingActionButtonPrivate.MiniDiameter,
                QtMaterialFloatingActionButtonPrivate.MiniDiameter,
            )
        else:
            return QSize(
                QtMaterialFloatingActionButtonPrivate.DefaultDiameter,
                QtMaterialFloatingActionButtonPrivate.DefaultDiameter,
            )

    def setMini(self, state: bool) -> void:
        if self.d.mini == state:
            return

        self.d.mini = state

        self.setFixedSize(self.d.diameter(), self.d.diameter())
        self.setFixedRippleRadius(30 if state == 30 else 50)

        self.d.setupProperties()
        self.updateClipPath()
        self.setGeometry(self.d.fabGeometry())
        self.update()

    def isMini(self) -> bool:
        return self.d.mini

    def setCorner(self, corner: Qt.Corner) -> void:
        if self.d.corner == corner:
            return

        self.d.corner = corner
        self.setGeometry(self.d.fabGeometry())
        self.update()

    def corner(self) -> Qt.Corner:
        return self.d.corner

    def setOffset(self, x: int, y: int) -> void:
        self.d.offsX = x
        self.d.offsY = y
        self.setGeometry(self.d.fabGeometry())
        self.update()

    def offset(self) -> QSize:
        return QSize(self.d.offsX, self.d.offsY)

    def setXOffset(self, x: int) -> void:
        self.d.offsX = x
        self.setGeometry(self.d.fabGeometry())
        self.update()

    def xOffset(self) -> int:
        return self.d.offsX

    def setYOffset(self, y: int) -> void:
        self.d.offsY = y
        self.setGeometry(self.d.fabGeometry())
        self.update()

    def yOffset(self) -> int:
        return self.d.offsY

    def event(self, event: QEvent) -> bool:
        if not self.parent():
            return QtMaterialRaisedButton.event(self, event)

        e = event.type()
        if e == QEvent.ParentChange:
            self.parent().installEventFilter(self)
            self.setGeometry(self.d.fabGeometry())

        elif e == QEvent.ParentAboutToChange:
            self.parent().removeEventFilter(self)

        return QtMaterialRaisedButton.event(self, event)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if QEvent.Move == type or QEvent.Resize == type:
            self.setGeometry(self.d.fabGeometry())

        return QtMaterialRaisedButton.eventFilter(obj, event)

    def paintEvent(self, event: QPaintEvent) -> void:
        square = QRect(0, 0, self.d.diameter(), self.d.diameter())
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

        iconGeometry = QRect(0, 0, self.d.iconSize(), self.d.iconSize())
        iconGeometry.moveCenter(square.center())

        pixmap: QPixmap = self.icon().pixmap(
            QSize(self.d.iconSize(), self.d.iconSize())
        )
        icon = QPainter(pixmap)
        icon.setCompositionMode(QPainter.CompositionMode_SourceIn)
        icon.fillRect(
            pixmap.rect(),
            self.foregound
            if self.isEnabled() or self.foregroundColor()
            else self.disabledForegroundColor(),
        )
        painter.drawPixmap(iconGeometry, pixmap)

    def updateClipPath(self) -> void:
        path = QPainterPath()
        path.addEllipse(0, 0, self.d.diameter(), self.d.diameter())
        self.d.rippleOverlay.setClipPath(path)
