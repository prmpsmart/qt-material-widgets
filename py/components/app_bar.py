from .lib.qtmaterial import *


class QtMaterialAppBar:
    ...


class QtMaterialAppBarPrivate:
    def __init__(self, q: QtMaterialAppBar):
        self.q = q
        self.useThemeColors = bool()
        self.foregroundColor = QColor()
        self.backgroundColor = QColor()

    def init(self) -> None:
        self.useThemeColors = True

        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(11)
        effect.setColor(QColor(0, 0, 0, 50))
        effect.setOffset(0, 3)

        self.q.setGraphicsEffect(effect)

        layout = QHBoxLayout()
        self.q.setLayout(layout)


class QtMaterialAppBar(QWidget):
    def __init__(self, parent: QWidget = None):
        QWidget.__init__(self, parent)

        self.d = QtMaterialAppBarPrivate(self)
        self.d.init()

    def sizeHint(self) -> QSize:
        return QSize(-1, 64)

    def setUseThemeColors(self, value: bool) -> None:
        if self.d.useThemeColors == value:
            return

        self.d.useThemeColors = value
        self.update()

    def useThemeColors(self) -> bool:
        return self.d.useThemeColors

    def setForegroundColor(self, color: QColor) -> None:
        self.d.foregroundColor = color

        if self.d.useThemeColors == True:
            self.d.useThemeColors = False
        self.update()

    def foregroundColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.foregroundColor.isValid():
            return QtMaterialStyle.instance().themeColor("primary1")
        else:
            return self.d.foregroundColor

    def setBackgroundColor(self, color: QColor) -> None:
        self.d.backgroundColor = color

        if self.d.useThemeColors == True:
            self.d.useThemeColors = False
        self.update()

    def backgroundColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.backgroundColor.isValid():
            return QtMaterialStyle.instance().themeColor("primary1")
        else:
            return self.d.backgroundColor

    def appBarLayout(self) -> QHBoxLayout:
        return self.layout()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)

        painter.fillRect(self.rect(), self.backgroundColor())
        painter.end()

    foregroundColor = Q_PROPERTY(QColor, fset=setForegroundColor, fget=foregroundColor)
    backgroundColor = Q_PROPERTY(QColor, fset=setBackgroundColor, fget=backgroundColor)
