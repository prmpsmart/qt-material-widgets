from ..core.material_widget import *


class QMaterialIconButton(QAbstractButton, QMaterialWidget):
    def __init__(
        self,
        icon: Union[QIcon, QPixmap, str] = None,
        parent: QWidget = None,
        size: QSize = None,
        **kwargs
    ):
        QAbstractButton.__init__(self, parent)
        QMaterialWidget.__init__(self, self.parentWidget(), **kwargs)

        self.setIcon(QIcon(icon))

        if size:
            self.setIconSize(size)

        self.m_rippleOverlay.installEventFilter(self)

        policy = QSizePolicy()
        policy.setWidthForHeight(True)
        self.setSizePolicy(policy)

    def updateRipple(self) -> None:
        r = self.rect()
        r.setSize(QSize(self.width() * 2, self.height() * 2))
        r.moveCenter(self.geometry().center())
        self.m_rippleOverlay.setGeometry(r)

    def sizeHint(self) -> QSize:
        return self.iconSize()

    def color(self) -> QColor:
        if (not self.m_color.isValid()) and self.m_useThemeColors:
            return QMaterialStyle().themeColor("text")

        return self.m_color

    def setDisabledColor(self, color: Union[QColor, Qt.GlobalColor]) -> None:
        self.m_disabledColor = QColor(color)

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.update()

    def disabledColor(self) -> QColor:
        if (not self.m_disabledColor.isValid()) and self.m_useThemeColors:
            return QMaterialStyle().themeColor("disabled")

        return self.m_disabledColor

    def event(self, event: QEvent) -> bool:
        typ = event.type()
        if typ in [QEvent.Move, QEvent.Resize]:
            self.updateRipple()
        elif typ == QEvent.ParentChange:
            widget = self.parentWidget()
            if widget:
                self.m_rippleOverlay.setParent(widget)

        return QAbstractButton.event(self, event)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if QEvent.Resize == event.type():
            self.updateRipple()

        return QAbstractButton.eventFilter(self, obj, event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.m_rippleOverlay.addRipple(
            center=QPoint(self.m_rippleOverlay.width(), self.m_rippleOverlay.height())
            / 2,
            radius=self.iconSize().width(),
        )

        self.clicked.emit()

        QAbstractButton.mousePressEvent(self, event)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        pixmap: QPixmap = self.icon().pixmap(self.iconSize())

        r = QRect(self.rect())
        w: float = pixmap.width()
        h: float = pixmap.height()
        painter.drawPixmap(
            QRect((r.width() - w) / 2, (r.height() - h) / 2, w, h), pixmap
        )

        painter.end()
