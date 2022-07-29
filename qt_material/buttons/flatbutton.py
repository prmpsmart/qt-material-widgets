from ..core.material_widget import QMaterialWidget
from .flatbutton_statemachine import *


class QMaterialFlatButton(QPushButton, QMaterialWidget):
    IconPadding = 12

    def __init__(
        self,
        text: str = None,
        parent: QWidget = None,
        preset: Material.ButtonPreset = Material.FlatPreset,
        haloVisible: bool = True,
        **kwargs
    ):
        QPushButton.__init__(self, text, parent)
        QMaterialWidget.__init__(self, **kwargs)

        self.m_haloVisible = haloVisible

        self.m_iconPlacement = Material.LeftIcon
        self.m_textAlignment = Qt.AlignHCenter
        self.m_fixedRippleRadius = 64
        self.m_cornerRadius = 3
        self.m_fontSize = 10  # 10.5
        self.m_useFixedRippleRadius = False

        self.setAttribute(Qt.WA_Hover)
        self.setMouseTracking(True)

        font = QFont("Roboto", self.m_fontSize, QFont.Medium)
        font.setCapitalization(QFont.AllUppercase)
        self.setFont(font)

        path = QPainterPath()
        path.addRoundedRect(self.rect(), self.m_cornerRadius, self.m_cornerRadius)
        self.m_rippleOverlay.setClipPath(path)
        self.m_rippleOverlay.setClipping(True)

        self.m_stateMachine = QMaterialFlatButtonStateMachine(self)

        self.m_stateMachine.setupProperties()
        self.m_stateMachine.startAnimations()

        self.applyPreset(preset)

    def applyPreset(self, preset: Material.ButtonPreset) -> None:
        if preset == Material.FlatPreset:
            self.setOverlayStyle(Material.NoOverlay)
        elif preset == Material.CheckablePreset:
            self.setOverlayStyle(Material.NoOverlay)
            self.setCheckable(True)
            self.setHaloVisible(False)

    def setUseThemeColors(self, value: bool) -> None:
        QMaterialWidget.setUseThemeColors(self, value)
        self.m_stateMachine.setupProperties()

    def setRole(self, role: Material.Role) -> None:
        QMaterialWidget.setRole(self, role)
        self.m_stateMachine.setupProperties()

    def setHaloVisible(self, visible: bool) -> None:
        self.m_haloVisible = visible
        self.update()

    def isHaloVisible(self) -> bool:
        return self.m_haloVisible

    def setOverlayStyle(self, style: Material.OverlayStyle) -> None:
        self.m_overlayStyle = style
        self.update()

    def overlayStyle(self) -> Material.OverlayStyle:
        return self.m_overlayStyle

    def setRippleStyle(self, style: Material.RippleStyle) -> None:
        self.m_rippleStyle = style

    def rippleStyle(self) -> Material.RippleStyle:
        return self.m_rippleStyle

    def setIconPlacement(self, placement: Material.ButtonIconPlacement) -> None:
        self.m_iconPlacement = placement
        self.update()

    def iconPlacement(self) -> Material.ButtonIconPlacement:
        return self.m_iconPlacement

    def setCornerRadius(self, radius: float) -> None:
        self.m_cornerRadius = radius
        self.updateClipPath()
        self.update()

    def cornerRadius(self) -> float:
        return self.m_cornerRadius

    def setCheckable(self, value: bool) -> None:
        self.m_stateMachine.updateCheckedStatus()

        QPushButton.setCheckable(value)

    def setTextAlignment(self, alignment: Qt.Alignment) -> None:
        self.m_textAlignment = alignment

    def textAlignment(self) -> Qt.Alignment:
        return self.m_textAlignment

    def sizeHint(self) -> QSize:
        self.ensurePolished()

        label = QSize(self.fontMetrics().size(Qt.TextSingleLine, self.text()))

        w: int = 20 + label.width()
        h: int = label.height()
        if not self.icon().isNull():
            w += self.iconSize().width() + QMaterialFlatButton.IconPadding
            h = max(h, self.iconSize().height())

        return QSize(w, 20 + h)

    def checkStateSet(self) -> None:
        self.m_stateMachine.updateCheckedStatus()

        QPushButton.checkStateSet()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if Material.NoRipple != self.m_rippleStyle:

            if Material.CenteredRipple == self.m_rippleStyle:
                pos = self.rect().center()
            else:
                pos = event.pos()

            if self.m_useFixedRippleRadius:
                radiusEndValue = self.m_fixedRippleRadius
            else:
                radiusEndValue = self.width() / 2

            ripple = self.m_rippleOverlay.addRipple(
                center=pos,
                radius=radiusEndValue,
                radiusDuration=600,
                opacityDuration=1300,
            )
            ripple.setOpacityStartValue(0.35)

        QPushButton.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        QPushButton.mouseReleaseEvent(self, event)

        self.m_stateMachine.updateCheckedStatus()

    def resizeEvent(self, event: QResizeEvent) -> None:
        QPushButton.resizeEvent(self, event)

        self.updateClipPath()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cr: float = self.m_cornerRadius

        if cr > 0:
            path = QPainterPath()
            path.addRoundedRect(self.rect(), cr, cr)

            painter.setClipPath(path)
            painter.setClipping(True)

        self.paintBackground(painter)
        self.paintHalo(painter)

        painter.setOpacity(1)
        painter.setClipping(False)

        self.paintForeground(painter)

    def paintBackground(self, painter: QPainter) -> None:
        overlayOpacity: float = self.m_stateMachine.overlayOpacity()
        checkedProgress: float = self.m_stateMachine.checkedOverlayProgress()

        if Qt.OpaqueMode == self.m_bgMode:
            brush = QBrush()
            brush.setStyle(Qt.SolidPattern)
            if self.isEnabled():
                brush.setColor(self.backgroundColor())
            else:
                brush.setColor(self.disabledBackgroundColor())

            painter.setOpacity(1)
            painter.setBrush(brush)
            painter.setPen(Qt.NoPen)
            painter.drawRect(self.rect())

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        painter.setPen(Qt.NoPen)

        if not self.isEnabled():
            return

        if (Material.NoOverlay != self.m_overlayStyle) and (overlayOpacity > 0):
            if Material.TintedOverlay == self.m_overlayStyle:
                brush.setColor(self.overlayColor())
            else:
                brush.setColor(Qt.gray)

            painter.setOpacity(overlayOpacity)
            painter.setBrush(brush)
            painter.drawRect(self.rect())

        if self.isCheckable() and checkedProgress > 0:
            q: float = 0.45 if Qt.TransparentMode == self.m_bgMode else 0.7
            brush.setColor(self.foregroundColor())
            painter.setOpacity(q * checkedProgress)
            painter.setBrush(brush)
            r = QRect(self.rect())
            r.setHeight(r.height() * checkedProgress)
            painter.drawRect(r)

    def paintHalo(self, painter: QPainter) -> None:
        if not self.m_haloVisible:
            return

        opacity: float = self.m_stateMachine.haloOpacity()
        s: float = (
            self.m_stateMachine.haloScaleFactor() * self.m_stateMachine.haloSize()
        )
        radius: float = self.width() * s

        if self.isEnabled() and opacity > 0:
            brush = QBrush()
            brush.setStyle(Qt.SolidPattern)
            brush.setColor(self.foregroundColor())
            painter.setOpacity(opacity)
            painter.setBrush(brush)
            painter.setPen(Qt.NoPen)
            center = self.rect().center()
            painter.drawEllipse(center, radius, radius)

    def paintForeground(self, painter: QPainter) -> None:
        if self.isEnabled():
            painter.setPen(self.foregroundColor())
            progress: float = self.m_stateMachine.checkedOverlayProgress()
            if self.isCheckable() and progress > 0:
                source: QColor = self.foregroundColor()
                dest: QColor = (
                    Qt.white
                    if Qt.TransparentMode == self.m_bgMode
                    else self.backgroundColor()
                )

                def COLOR_INTERPOLATE(CH):
                    _source = getattr(source, CH)
                    _dest = getattr(dest, CH)
                    return (1 - progress) * _source() + progress * _dest()

                if qFuzzyCompare(1, progress):
                    painter.setPen(dest)
                else:
                    painter.setPen(
                        QColor(
                            COLOR_INTERPOLATE("red"),
                            COLOR_INTERPOLATE("green"),
                            COLOR_INTERPOLATE("blue"),
                            COLOR_INTERPOLATE("alpha"),
                        )
                    )

        else:
            painter.setPen(self.disabledForegroundColor())

        if self.icon().isNull():
            if Qt.AlignLeft == self.m_textAlignment:
                painter.drawText(
                    self.rect().adjusted(12, 0, 0, 0),
                    Qt.AlignLeft | Qt.AlignVCenter,
                    self.text(),
                )
            else:
                painter.drawText(self.rect(), Qt.AlignCenter, self.text())

            return

        textSize = QSize(self.fontMetrics().size(Qt.TextSingleLine, self.text()))
        base = QSize(self.size() - textSize)

        iw: int = self.iconSize().width() + self.IconPadding
        pos = QPoint(
            12 if Qt.AlignLeft == self.m_textAlignment else (base.width() - iw) / 2, 0
        )

        textGeometry = QRect(pos + QPoint(0, base.height() / 2), textSize)
        iconGeometry = QRect(
            pos + QPoint(0, (self.height() - self.iconSize().height()) / 2),
            self.iconSize(),
        )

        if Material.LeftIcon == self.m_iconPlacement:
            textGeometry.translate(iw, 0)
        else:
            iconGeometry.translate(textSize.width() + self.IconPadding, 0)

        painter.drawText(textGeometry, Qt.AlignCenter, self.text() + "000")

        pixmap: QPixmap = self.icon().pixmap(self.iconSize())
        icon = QPainter(pixmap)
        icon.setCompositionMode(QPainter.CompositionMode_SourceIn)
        icon.fillRect(pixmap.rect(), painter.pen().color())
        painter.drawPixmap(iconGeometry, pixmap)

    def updateClipPath(self) -> None:
        radius: float = self.m_cornerRadius

        path = QPainterPath()
        path.addRoundedRect(self.rect(), radius, radius)
        self.m_rippleOverlay.setClipPath(path)
