from .core.overlay_widget import *
from .buttons import *


class QMaterialTabsInkBar(QMaterialOverlayWidget):
    def __init__(self, parent):
        QMaterialOverlayWidget.__init__(self, parent)

        self.m_tabs = parent
        self.m_animation = QPropertyAnimation()
        self.m_geometry = QRect()
        self.m_previousGeometry = QRect()
        self.m_tween = 0

        self.m_animation.setPropertyName(b"_tweenValue")
        self.m_animation.setEasingCurve(QEasingCurve.OutCirc)
        self.m_animation.setTargetObject(self)
        self.m_animation.setDuration(700)

        self.m_tabs.installEventFilter(self)

        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)

    def setTweenValue(self, value: float) -> None:
        self.m_tween = value
        self.refreshGeometry()

    def tweenValue(self) -> float:
        return self.m_tween

    def refreshGeometry(self) -> None:
        item: QLayoutItem = self.m_tabs.layout().itemAt(self.m_tabs.currentIndex())

        if item:
            r = QRect(item.geometry())
            s: float = 1 - self.m_tween

            if QAbstractAnimation.Running != self.m_animation.state():
                self.m_geometry = QRect(r.left(), r.bottom() - 1, r.width(), 2)
            else:
                left: float = (
                    self.m_previousGeometry.left() * s + r.left() * self.m_tween
                )
                width: float = (
                    self.m_previousGeometry.width() * s + r.width() * self.m_tween
                )
            self.m_geometry = QRect(left, r.bottom() - 1, width, 2)

            self.m_tabs.update()

    def animate(self) -> None:
        self.raise_()

        self.m_previousGeometry = self.m_geometry

        self.m_animation.stop()
        self.m_animation.setStartValue(0)
        self.m_animation.setEndValue(1)
        self.m_animation.start()

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if event.type() in [QEvent.Move, QEvent.Resize]:
            self.refreshGeometry()

        return QMaterialOverlayWidget.eventFilter(self, obj, event)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)

        painter.setOpacity(1)
        painter.fillRect(self.m_geometry, self.m_tabs.inkColor())

    _tweenValue = Property(float, fset=setTweenValue, fget=tweenValue)


class QMaterialTab(QMaterialFlatButton):
    def __init__(self, parent):
        QMaterialFlatButton.__init__(self, parent)

        self.m_tabs = parent
        self.m_active = bool(False)

        self.setMinimumHeight(50)

        f = QFont(self.font())
        f.setStyleName("Normal")
        self.setFont(f)

        self.setCornerRadius(0)
        self.setRole(Material.Primary)
        self.setBackgroundMode(Qt.OpaqueMode)
        self.setBaseOpacity(0.25)

        self.clicked.connect(self.activateTab)

    def setActive(self, state: bool) -> None:
        self.m_active = state
        self.update()

    def isActive(self) -> bool:
        return self.m_active

    def sizeHint(self) -> QSize:
        if self.icon().isNull():
            return QMaterialFlatButton.sizeHint(self)
        else:
            return QSize(40, self.iconSize().height() + 46)

    def activateTab(self) -> None:
        self.m_tabs.setCurrentTab(self)

    def paintForeground(self, painter: QPainter) -> None:
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


class QMaterialTabs(QWidget):
    currentChanged = Signal(int)

    def __init__(self, parent: QWidget = None):
        QWidget.__nit__(self, parent)

        self.m_inkBar = QMaterialTabsInkBar(self.q)
        self.m_tabLayout = QHBoxLayout
        self.m_rippleStyle = Material.CenteredRipple
        self.m_tab = -1
        self.m_showHalo = True
        self.m_useThemeColors = True

        self.setLayout(self.m_tabLayout)
        self.setStyle(QMaterialStyle.instance())

        self.m_tabLayout.setSpacing(0)
        self.m_tabLayout.setMargin(0)

    def setUseThemeColors(self, value: bool) -> None:
        self.m_useThemeColors = value

    def useThemeColors(self) -> bool:
        return self.m_useThemeColors

    def setHaloVisible(self, value: bool) -> None:
        self.m_showHalo = value
        self.updateTabs()

    def isHaloVisible(self) -> bool:
        return self.m_showHalo

    def setRippleStyle(self, style: Material.RippleStyle) -> None:
        self.m_rippleStyle = style
        self.updateTabs()

    def rippleStyle(self) -> Material.RippleStyle:
        return self.m_rippleStyle

    def setInkColor(self, color: QColor) -> None:
        self.m_inkColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.m_inkBar.update()
        self.update()

    def inkColor(self) -> QColor:
        if self.m_useThemeColors or not self.m_inkColor.isValid():
            return QMaterialStyle.instance().themeColor("accent1")
        else:
            return self.m_inkColor

    def setBackgroundColor(self, color: QColor) -> None:
        self.m_backgroundColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.updateTabs()
        self.update()

    def backgroundColor(self) -> QColor:
        if self.m_useThemeColors or not self.m_backgroundColor.isValid():
            return QMaterialStyle.instance().themeColor("primary1")
        else:
            return self.m_backgroundColor

    def setTextColor(self, color: QColor) -> None:
        self.m_textColor = color

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.updateTabs()
        self.update()

    def textColor(self) -> QColor:
        if self.m_useThemeColors or not self.m_textColor.isValid():
            return QMaterialStyle.instance().themeColor("canvas")
        else:
            return self.m_textColor

    def addTab(self, text: str, icon: QIcon = QIcon()) -> None:
        tab: QMaterialTab = QMaterialTab(self)
        tab.setText(text)
        tab.setHaloVisible(self.isHaloVisible())
        tab.setRippleStyle(self.rippleStyle())

        if not icon.isNull():
            tab.setIcon(icon)
            tab.setIconSize(QSize(22, 22))

        self.m_tabLayout.addWidget(tab)

        if -1 == self.m_tab:
            self.m_tab = 0
            self.m_inkBar.refreshGeometry()
            self.m_inkBar.raise_()
            tab.setActive(True)

    def setCurrentTab(self, tab: QMaterialTab = None, index: int = 0) -> None:
        if tab:
            index = self.m_tabLayout.indexOf(tab)

        self.setTabActive(self.m_tab, False)
        self.m_tab = index
        self.setTabActive(index, True)
        self.m_inkBar.animate()

        self.emit(self.currentChanged(index))

    def currentIndex(self) -> int:
        return self.m_tab

    def setTabActive(self, index: int, active: bool = True) -> None:
        if index > -1:
            tab: QMaterialTab = self.m_tabLayout.itemAt(index).widget()
            if tab:
                tab.setActive(active)

    def updateTabs(self) -> None:

        for i in range(self.m_tabLayout.count()):
            item: QLayoutItem = self.m_tabLayout.itemAt(i)

            tab: QMaterialTab = item.widget()

            if tab:
                tab.setRippleStyle(self.m_rippleStyle)
                tab.setHaloVisible(self.m_showHalo)
                tab.setBackgroundColor(self.backgroundColor())
                tab.setForegroundColor(self.textColor())
