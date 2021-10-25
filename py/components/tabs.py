from py.components.flatbutton import QtMaterialFlatButton
from .lib.qtmaterial import *


class QtMaterialTabsInkBar(QtMaterialOverlayWidget):
    def __init__(self, parent):
        QtMaterialOverlayWidget.__init__(self, parent)

        self.m_tabs = parent
        self.m_animation = QPropertyAnimation()
        self.m_geometry = QRect()
        self.m_previousGeometry = QRect()
        self.m_tween = qreal(0)

        self.m_animation.setPropertyName(b"_tweenValue")
        self.m_animation.setEasingCurve(QEasingCurve.OutCirc)
        self.m_animation.setTargetObject(self)
        self.m_animation.setDuration(700)

        self.m_tabs.installEventFilter(self)

        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)

    def setTweenValue(self, value: qreal) -> void:
        self.m_tween = value
        self.refreshGeometry()

    def tweenValue(self) -> qreal:
        return self.m_tween

    def refreshGeometry(self) -> void:
        item: QLayoutItem = self.m_tabs.layout().itemAt(self.m_tabs.currentIndex())

        if item:
            r = QRect(item.geometry())
            s: qreal = 1 - self.m_tween

            if QAbstractAnimation.Running != self.m_animation.state():
                self.m_geometry = QRect(r.left(), r.bottom() - 1, r.width(), 2)
            else:
                left: qreal = (
                    self.m_previousGeometry.left() * s + r.left() * self.m_tween
                )
                width: qreal = (
                    self.m_previousGeometry.width() * s + r.width() * self.m_tween
                )
            self.m_geometry = QRect(left, r.bottom() - 1, width, 2)

            self.m_tabs.update()

    def animate(self) -> void:
        self.raise_()

        self.m_previousGeometry = self.m_geometry

        self.m_animation.stop()
        self.m_animation.setStartValue(0)
        self.m_animation.setEndValue(1)
        self.m_animation.start()

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if event.type() in [QEvent.Move, QEvent.Resize]:
            self.refreshGeometry()

        return QtMaterialOverlayWidget.eventFilter(self, obj, event)

    def paintEvent(self, event: QPaintEvent) -> void:
        painter = QPainter(self)

        painter.setOpacity(1)
        painter.fillRect(self.m_geometry, self.m_tabs.inkColor())

    _tweenValue = Q_PROPERTY(qreal, fset=setTweenValue, fget=tweenValue)


class QtMaterialTab(QtMaterialFlatButton):
    def __init__(self, parent):
        QtMaterialFlatButton.__init__(self, parent)

        self.m_tabs = parent
        self.m_active = bool(false)

        self.setMinimumHeight(50)

        f = QFont(self.font())
        f.setStyleName("Normal")
        self.setFont(f)

        self.setCornerRadius(0)
        self.setRole(Material.Primary)
        self.setBackgroundMode(Qt.OpaqueMode)
        self.setBaseOpacity(0.25)

        self.clicked.connect(self.activateTab)

    def setActive(self, state: bool) -> void:
        self.m_active = state
        self.update()

    def isActive(self) -> bool:
        return self.m_active

    def sizeHint(self) -> QSize:
        if self.icon().isNull():
            return QtMaterialFlatButton.sizeHint(self)
        else:
            return QSize(40, self.iconSize().height() + 46)

    def activateTab(self) -> void:
        self.m_tabs.setCurrentTab(self)

    def paintForeground(self, painter: QPainter) -> void:
        painter.setPen(self.foregroundColor())

        if not self.icon().isNull():
            painter.translate(0, 12)

        textSize = QSize(self.fontMetrics().size(Qt.TextSingleLine, self.text()))
        base = QSize(self.size() - textSize)

        textGeometry = QRect(QPoint(base.width(), base.height()) / 2, textSize)

        painter.drawText(textGeometry, Qt.AlignCenter, self.text())

        if not self.icon().isNull():

            size: QSize = self.iconSize()
            iconRect = QRect(QPoint((self.width() - size.width()) / 2, 0), size)

            pixmap: QPixmap = self.icon().pixmap(self.iconSize())
            icon = QPainter(pixmap)
            icon.setCompositionMode(QPainter.CompositionMode_SourceIn)
            icon.fillRect(pixmap.rect(), painter.pen().color())
            painter.drawPixmap(iconRect, pixmap)

        if not self.m_active:
            if not icon().isNull():
                painter.translate(0, -12)

            overlay = QBrush()
            overlay.setStyle(Qt.SolidPattern)
            overlay.setColor(self.backgroundColor())
            painter.setOpacity(0.36)
            painter.fillRect(self.rect(), overlay)


class QtMaterialTabsPrivate:
    def __init__(self, q):
        self.q:QtMaterialTabs = q

        self.inkBar = QtMaterialTabsInkBar()
        self.tabLayout = QHBoxLayout()
        self.rippleStyle = Material()
        self.inkColor = QColor()
        self.backgroundColor = QColor()
        self.textColor = QColor()
        self.tab :int= None
        self.showHalo :bool= None
        self.useThemeColors :bool= None

    def init(self) -> void:
        self.inkBar = QtMaterialTabsInkBar(self.q)
        self.tabLayout = QHBoxLayout
        self.rippleStyle = Material.CenteredRipple
        self.tab = -1
        self.showHalo = true
        self.useThemeColors = true

        self.q.setLayout(self.tabLayout)
        self.q.setStyle(QtMaterialStyle.instance())

        self.tabLayout.setSpacing(0)
        self.tabLayout.setMargin(0)


class QtMaterialTabs(QWidget):
    currentChanged = Signal(int)

    def __init__(self, parent: QWidget = None):
        QWidget.__nit__(self, parent)
        self.d = QtMaterialTabsPrivate(self)
        self.d.init()

    def setUseThemeColors(self, value: bool) -> void:
        self.d.useThemeColors = value

    def useThemeColors(self) -> bool:
        return self.d.useThemeColors

    def setHaloVisible(self, value: bool) -> void:
        self.d.showHalo = value
        self.updateTabs()

    def isHaloVisible(self) -> bool:
        return self.d.showHalo

    def setRippleStyle(self, style: Material.RippleStyle) -> void:
        self.d.rippleStyle = style
        self.updateTabs()

    def rippleStyle(self) -> Material.RippleStyle:
        return self.d.rippleStyle

    def setInkColor(self, color: QColor) -> void:
        self.d.inkColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.d.inkBar.update()
        self.update()

    def inkColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.inkColor.isValid():
            return QtMaterialStyle.instance().themeColor("accent1")
        else:
            return self.d.inkColor

    def setBackgroundColor(self, color: QColor) -> void:
        self.d.backgroundColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.updateTabs()
        self.update()

    def backgroundColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.backgroundColor.isValid():
            return QtMaterialStyle.instance().themeColor("primary1")
        else:
            return self.d.backgroundColor

    def setTextColor(self, color: QColor) -> void:
        self.d.textColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.updateTabs()
        self.update()

    def textColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.textColor.isValid():
            return QtMaterialStyle.instance().themeColor("canvas")
        else:
            return self.d.textColor

    def addTab(self, text: QString, icon: QIcon = QIcon()) -> void:
        tab: QtMaterialTab = QtMaterialTab(self)
        tab.setText(text)
        tab.setHaloVisible(self.isHaloVisible())
        tab.setRippleStyle(self.rippleStyle())

        if not icon.isNull():
            tab.setIcon(icon)
            tab.setIconSize(QSize(22, 22))

        self.d.tabLayout.addWidget(tab)

        if -1 == self.d.tab:
            self.d.tab = 0
            self.d.inkBar.refreshGeometry()
            self.d.inkBar.raise_()
            tab.setActive(true)

    def setCurrentTab(self, tab: QtMaterialTab = None, index: int = 0) -> void:
        if tab:
            index = self.d.tabLayout.indexOf(tab)

        self.setTabActive(self.d.tab, false)
        self.d.tab = index
        self.setTabActive(index, true)
        self.d.inkBar.animate()

        self.emit(self.currentChanged(index))

    def currentIndex(self) -> int:
        return self.d.tab

    def setTabActive(self, index: int, active: bool = true) -> void:
        if index > -1:
            tab: QtMaterialTab = self.d.tabLayout.itemAt(index).widget()
            if tab:
                tab.setActive(active)

    def updateTabs(self) -> void:

        for i in range(self.d.tabLayout.count()):
            item: QLayoutItem = self.d.tabLayout.itemAt(i)

            tab: QtMaterialTab = item.widget()

            if tab:
                tab.setRippleStyle(self.d.rippleStyle)
                tab.setHaloVisible(self.d.showHalo)
                tab.setBackgroundColor(self.backgroundColor())
                tab.setForegroundColor(self.textColor())
