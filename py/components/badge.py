from .lib.qtmaterial import *


class QtMaterialBadge:
    ...


class QtMaterialBadgePrivate:
    def __init__(self, q: QtMaterialBadge):

        self.q = q

        self.text = QString()
        self.textColor = QColor()
        self.backgroundColor = QColor()
        self.size = QSize()
        self.icon = QIcon()
        self.x = qreal()
        self.y = qreal()
        self.padding = int()
        self.useThemeColors = bool()

    def init(self) -> None:
        self.x = 0
        self.y = 0
        self.padding = 10
        self.useThemeColors = true

        self.q.setAttribute(Qt.WA_TransparentForMouseEvents)

        font = QFont(self.q.font())
        font.setPointSizeF(10)
        font.setStyleName("Bold")
        self.q.setFont(font)

        self.q.setText("+1")


class QtMaterialBadge(QtMaterialOverlayWidget):
    def __init__(
        self, icon: QIcon = None, text: QString = None, parent: QWidget = None
    ):
        QtMaterialOverlayWidget.__init__(self, parent)

        self.d = QtMaterialBadgePrivate(self)
        self.d.init()

        if icon:
            self.setIcon(icon)
        if text:
            self.setText(text)

    def setUseThemeColors(self, value: bool) -> void:
        if self.d.useThemeColors == value:
            return
        self.d.useThemeColors = value
        self.update()

    def useThemeColors(self) -> bool:
        return self.d.useThemeColors

    def setTextColor(self, color: QColor) -> void:
        self.d.textColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.update()

    def textColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.textColor.isValid():
            return QtMaterialStyle.instance().themeColor("canvas")
        else:
            return self.d.textColor

    def setBackgroundColor(self, color: QColor) -> void:
        self.d.backgroundColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.update()

    def backgroundColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.backgroundColor.isValid():
            return QtMaterialStyle.instance().themeColor("accent1")
        else:
            return self.d.backgroundColor

    def setRelativePosition(self, pos: QPointF) -> void:
        self.setRelativePosition(pos.x(), pos.y())

    def setRelativePosition(self, x: qreal, y: qreal) -> void:
        self.d.x = x
        self.d.y = y
        self.update()

    def relativePosition(self) -> QPointF:
        return QPointF(self.d.x, self.d.y)

    def setRelativeXPosition(self, x: qreal) -> void:
        self.d.x = x
        self.update()

    def relativeXPosition(self) -> qreal:
        return self.d.x

    def setRelativeYPosition(self, y: qreal) -> void:
        self.d.y = y
        self.update()

    def relativeYPosition(self) -> qreal:
        return self.d.y

    def sizeHint(self) -> QSize:
        s: int = self.getDiameter()
        return QSize(s + 4, s + 4)

    def setIcon(self, icon: QIcon) -> void:
        self.d.icon = icon
        self.update()

    def icon(self) -> QIcon:
        return self.d.icon

    def setText(self, text: QString) -> void:
        self.d.text = text

        if not self.d.icon.isNull():
            self.d.icon = QIcon()

        self.d.size = self.fontMetrics().size(Qt.TextShowMnemonic, text)

        self.update()

    def text(self) -> QString:
        return self.d.text

    def paintEvent(self, event: QPaintEvent) -> void:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.d.x, self.d.y)

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(
            self.backgroundColor()
            if self.isEnabled()
            else QtMaterialStyle.instance().themeColor("disabled")
        )
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)

        s: int = self.getDiameter()

        r = QRectF(0, 0, s, s)
        r.translate(QPointF((self.width() - s), (self.height() - s)) / 2)

        if self.d.icon.isNull():
            painter.drawEllipse(r)
            painter.setPen(self.textColor())
            painter.setBrush(Qt.NoBrush)
            painter.drawText(r.translated(0, -0.5), Qt.AlignCenter, self.d.text)
        else:
            painter.drawEllipse(r)
            q = QRectF(0, 0, 16, 16)
            q.moveCenter(r.center())
            pixmap: QPixmap = self.icon().pixmap(16, 16)
            icon = QPainter(pixmap)
            icon.setCompositionMode(QPainter.CompositionMode_SourceIn)
            icon.fillRect(pixmap.rect(), self.textColor())
            icon.end()
            painter.drawPixmap(q.toRect(), pixmap)
        painter.end()

    def getDiameter(self) -> int:
        if self.d.icon.isNull():
            return max(self.d.size.width(), self.d.size.height()) + self.d.padding
        else:
            return 24
