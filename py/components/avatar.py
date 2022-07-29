from .lib.qtmaterial import *


class QtMaterialAvatarPrivate:
    def __init__(self, q: "QtMaterialAvatar"):

        self.q: QtMaterialAvatar = q
        self.size = int(40)
        self.type = Material.LetterAvatar
        self.letter = QChar()
        self.image = QImage()
        self.icon = QIcon()
        self.pixmap = QPixmap()
        self.useThemeColors = bool(true)
        self.textColor = QColor()
        self.backgroundColor = QColor()

        font = QFont(self.q.font())
        font.setPointSizeF(16)
        self.q.setFont(font)

        policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.q.setSizePolicy(policy)


class QtMaterialAvatar(QWidget):
    def __init__(
        self,
        icon: QIcon = void,
        letter: QChar = "",
        image: QImage = void,
        parent: QWidget = void,
    ):
        QWidget.__init__(self, parent)

        self.d = QtMaterialAvatarPrivate(self)
        if icon:
            self.setIcon(icon)
        elif letter:
            self.setLetter(letter)
        elif image:
            self.setImage(image)

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
            return QtMaterialStyle.instance().themeColor("primary1")
        else:
            return self.d.backgroundColor

    def sizeHint(self) -> QSize:
        return QSize(self.d.size + 2, self.d.size + 2)

    def setSize(self, size: int) -> void:
        self.d.size = size

        if not self.d.image.isNull():
            self.d.pixmap = QPixmap.fromImage(
                self.d.image.scaled(
                    self.d.size,
                    self.d.size,
                    Qt.IgnoreAspectRatio,
                    Qt.SmoothTransformation,
                )
            )

        f = QFont(self.font())
        f.setPointSizeF(size * 16 / 40)
        self.setFont(f)

        self.update()

    def size(self) -> int:
        return self.d.size

    def setLetter(self, letter: QChar) -> void:
        self.d.letter = letter
        self.d.type = Material.LetterAvatar
        self.update()

    def setImage(self, image: QImage) -> void:
        self.d.image = image
        self.d.type = Material.ImageAvatar

        self.d.pixmap = QPixmap.fromImage(
            image.scaled(
                self.d.size, self.d.size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation
            )
        )
        self.update()

    def setIcon(self, icon: QIcon) -> void:
        self.d.icon = icon
        self.d.type = Material.IconAvatar
        self.update()

    def type(self) -> Material.AvatarType:
        return self.d.type

    def paintEvent(self, event: QPaintEvent) -> void:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        r: QRect = self.rect()
        hs: qreal = self.d.size / 2

        if not self.isEnabled():
            brush = QBrush()
            brush.setStyle(Qt.SolidPattern)
            brush.setColor(QtMaterialStyle.instance().themeColor("disabled"))
            painter.setPen(Qt.NoPen)
            painter.setBrush(brush)
            painter.drawEllipse(
                QRectF(
                    (self.width() - self.d.size) / 2,
                    (self.height() - self.d.size) / 2,
                    self.d.size,
                    self.d.size,
                )
            )
            return

        if Material.ImageAvatar != self.d.type:
            brush = QBrush()
            brush.setStyle(Qt.SolidPattern)
            brush.setColor(self.backgroundColor())
            painter.setPen(Qt.NoPen)
            painter.setBrush(brush)
            painter.drawEllipse(
                QRectF(
                    (self.width() - self.d.size) / 2,
                    (self.height() - self.d.size) / 2,
                    self.d.size,
                    self.d.size,
                )
            )

        d_type = self.d.type
        if d_type == Material.ImageAvatar:
            path = QPainterPath()
            path.addEllipse(
                self.width() / 2 - hs, self.height() / 2 - hs, self.d.size, self.d.size
            )
            painter.setClipPath(path)

            painter.drawPixmap(
                QRect(
                    self.width() / 2 - hs,
                    self.height() / 2 - hs,
                    self.d.size,
                    self.d.size,
                ),
                self.d.pixmap,
            )

        elif d_type == Material.IconAvatar:
            iconGeometry = QRect(
                (self.width() - hs) / 2, (self.height() - hs) / 2, hs, hs
            )

            pixmap: QPixmap = self.d.icon.pixmap(hs, hs)
            icon = QPainter(pixmap)
            icon.setCompositionMode(QPainter.CompositionMode_SourceIn)
            icon.fillRect(pixmap.rect(), self.textColor())
            icon.end()
            painter.drawPixmap(iconGeometry, pixmap)

        elif d_type == Material.LetterAvatar:
            painter.setPen(self.textColor())
            painter.setBrush(Qt.NoBrush)
            painter.drawText(r, Qt.AlignCenter, QString(self.d.letter))
        painter.end()
