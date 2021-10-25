from .lib.qtmaterial import *




class QtMaterialIconButton: ...


class QtMaterialIconButtonPrivate:

    def __init__(self, q: QtMaterialIconButton):
        self.q:QtMaterialIconButton = q
        self.rippleOverlay = QtMaterialRippleOverlay()
        self.color = QColor()
        self.disabledColor = QColor()
        self.useThemeColors:bool = None

    def init(self) -> void:
        self.rippleOverlay  = QtMaterialRippleOverlay(self.q.parentWidget())
        self.useThemeColors = true
        self.rippleOverlay.installEventFilter(self.q)

        self.q.setStyle(QtMaterialStyle.instance())

        policy = QSizePolicy()
        policy.setWidthForHeight(true)
        self.q.setSizePolicy(policy)

    def updateRipple(self) -> void:
        r = QRect(self.q.rect())
        r.setSize(QSize(self.q.width()*2, self.q.height()*2))
        r.moveCenter(self.q.geometry().center())
        self.rippleOverlay.setGeometry(r)




class QtMaterialIconButton(QAbstractButton):

    def __init__(self, icon: QIcon=None, parent: QWidget=None, d: QtMaterialIconButtonPrivate=None):
        QAbstractButton.__init__(self, parent)
        self.d = d or QtMaterialIconButtonPrivate(self)
        self.d.init()

        self.setIcon(icon)

    def sizeHint(self) -> QSize:
        return self.iconSize()

    def setUseThemeColors(self, value: bool) -> void:
        if (self.d.useThemeColors == value):
            return

        self.d.useThemeColors = value
        self.update()

    def useThemeColors(self) -> bool:
        return self.d.useThemeColors

    def setColor(self, color: QColor) -> void:
        self.d.color = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.update()

    def color(self) -> QColor:
        if (self.d.useThemeColors or not QColor(self.d.color).isValid()):
            return QtMaterialStyle.instance().themeColor("text")
        
        return self.d.color

    def setDisabledColor(self, color: QColor) -> void:
        self.d.disabledColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.update()

    def disabledColor(self) -> QColor:
        if (self.d.useThemeColors or not self.d.disabledColor.isValid()):
            return QtMaterialStyle.instance().themeColor("disabled")
        
        return self.d.disabledColor

    def event(self, event: QEvent) -> bool:
        typ = event.type()
        if typ in [QEvent.Move, QEvent.Resize]:
            self.d.updateRipple()
        elif typ == QEvent.ParentChange:
            widget = self.parentWidget()
            if (widget):
                self.d.rippleOverlay.setParent(widget)
            
        return QAbstractButton.event(self, event)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if (QEvent.Resize == event.type()):
            self.d.updateRipple()
        
        return QAbstractButton.eventFilter(self, obj, event)
    
    def mousePressEvent(self, event: QMouseEvent) -> void:
        self.d.rippleOverlay.addRipple(position=QPoint(self.d.rippleOverlay.width(), self.d.rippleOverlay.height())/2, radius=self.iconSize().width())

        self.clicked.emit()

        QAbstractButton.mousePressEvent(self, event)

    def paintEvent(self, event: QPaintEvent) -> void:
        painter = QPainter(self)

        pixmap: QPixmap = self.icon().pixmap(self.iconSize())

        icon = QPainter(pixmap)
        
        icon.setCompositionMode(QPainter.CompositionMode_SourceIn)
        icon.fillRect(pixmap.rect(), self.color() if self.isEnabled() else self.disabledColor())
        icon.end()

        r = QRect(self.rect())
        w: qreal = pixmap.width()
        h: qreal = pixmap.height()
        painter.drawPixmap(QRect((r.width()-w)/2, (r.height()-h)/2, w, h), pixmap)
        
        painter.end()







