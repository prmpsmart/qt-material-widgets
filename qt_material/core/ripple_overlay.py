from .ripple import *
from .overlay_widget import *


class QMaterialRippleOverlay(QMaterialOverlayWidget):
    def __init__(
        self,
        parent: QWidget = None,
        easingCurve: QEasingCurve = None,
        color: Union[QColor, Qt.GlobalColor] = None,
        radius: float = 300,
        opacity: float = 0.5,
    ):
        QMaterialOverlayWidget.__init__(self, parent)

        self.m_ripples: List[QMaterialRipple] = list()
        self.m_color = QColor(color)
        self.m_clipPath = QPainterPath()
        self.m_useClip = False
        self.m_easingCurve = easingCurve

        self.m_radius = radius
        self.m_opacity = opacity

        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)

    def setColor(self, color: QColor) -> None:
        self.m_color = QColor(color)

    def color(self) -> QColor:
        return self.m_color

    def setRadius(self, radius: float) -> None:
        self.m_radius = radius

    def radius(self) -> float:
        return self.m_radius

    def setOpacity(self, opacity: float) -> None:
        if self.m_opacity == opacity:
            return
        self.m_opacity = opacity
        self.m_overlay.update()

    def opacity(self) -> float:
        return self.m_opacity

    def addRipple(
        self, ripple: QMaterialRipple = None, color=None, radius: float = None, **kwargs
    ) -> QMaterialRipple:
        if not ripple:
            ripple = QMaterialRipple(
                overlay=self,
                easingCurve=self.m_easingCurve,
                color=color or self.m_color,
                radius=radius or self.m_radius,
                opacity=self.m_opacity,
                **kwargs
            )

        self.m_ripples.append(ripple)
        ripple.start()

        m = 30
        if len(self.m_ripples) >= m:
            self.m_ripples = self.m_ripples[: (m // 2)]

        self.destroyed.connect(ripple.stop)
        self.destroyed.connect(ripple.deleteLater)

        return ripple

    def removeRipple(self, ripple: QMaterialRipple) -> None:
        if self.m_ripples.remove(ripple):
            del ripple
            self.update()

    def setEasingCurve(self, easingCurve: QEasingCurve) -> None:
        self.m_easingCurve = easingCurve
        self.update()

    def setClipping(self, enable: bool) -> None:
        self.m_useClip = enable
        self.update()

    def hasClipping(self) -> bool:
        return self.m_useClip

    def setClipPath(self, path: QPainterPath) -> None:
        self.m_clipPath = path
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        if self.m_useClip:
            painter.setClipPath(self.m_clipPath)

        for i in self.m_ripples:
            self.paintRipple(painter, i)

    def ripples(self) -> List[QMaterialRipple]:
        return self.m_ripples

    def paintRipple(self, painter: QPainter, ripple: QMaterialRipple) -> None:
        radius: float = ripple.radius()
        center: QPointF = ripple.center()
        painter.setOpacity(ripple.opacity())
        painter.setBrush(ripple.brush())
        painter.drawEllipse(center, radius, radius)
