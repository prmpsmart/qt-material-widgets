from ._core import *


class QMaterialRipple(QParallelAnimationGroup):
    def __init__(
        self,
        overlay: Type["QMaterialRippleOverlay"],
        center: QPoint,
        parent: QObject = None,
        radius: float = 300,
        opacity: float = 0.5,
        easingCurve: QEasingCurve = None,
        opacityDuration=500,
        radiusDuration=500,
        color: Union[QColor, Qt.GlobalColor] = None,
    ):
        QParallelAnimationGroup.__init__(self, parent)

        self.m_overlay = overlay
        self.m_radius = 0
        self.m_opacity = 0
        self.m_center = center
        self.m_brush = QBrush()
        self.m_easingCurve = easingCurve or QEasingCurve.OutBounce

        self.m_radiusAnimation = self.animate(b"_radius", radiusDuration)
        self.m_opacityAnimation = self.animate(b"_opacity", opacityDuration)

        self.setOpacityStartValue(opacity)
        self.setOpacityEndValue(0)

        self.setRadiusStartValue(0)
        self.setRadiusEndValue(radius)

        self.setColor(color)
        self.m_brush.setStyle(Qt.SolidPattern)

        self.finished.connect(self.destroy)

    def animate(
        self,
        property: bytes,
        duration: int = 800,
    ) -> QPropertyAnimation:

        animation = QPropertyAnimation(self, property)
        animation.setEasingCurve(self.m_easingCurve)
        animation.setDuration(duration)
        self.addAnimation(animation)
        return animation

    def setRadius(self, radius: float) -> None:
        if self.m_radius == radius:
            return
        self.m_radius = radius
        self.m_overlay.update()

    def radius(self) -> float:
        return self.m_radius

    def setOpacity(self, opacity: float) -> None:
        if self.m_opacity == opacity:
            return
        self.m_opacity = opacity
        self.m_overlay.update()

    def opacity(self) -> float:
        return self.m_opacity

    def setColor(self, color: QColor) -> None:
        if self.m_brush.color() == color:
            return
        self.m_brush.setColor(QColor(color))

        if self.m_overlay:
            self.m_overlay.update()

    def color(self) -> QColor:
        return self.m_brush.color()

    def setBrush(self, brush: QBrush) -> None:
        self.m_brush = brush

        if self.m_overlay:
            self.m_overlay.update()

    def brush(self) -> QBrush:
        return self.m_brush

    def center(self) -> QPoint:
        return self.m_center

    def radiusAnimation(self) -> QPropertyAnimation:
        return self.m_radiusAnimation

    def opacityAnimation(self) -> QPropertyAnimation:
        return self.m_opacityAnimation

    def setOpacityStartValue(self, value: float) -> None:
        self.m_opacityAnimation.setStartValue(value)

    def setOpacityEndValue(self, value: float) -> None:
        self.m_opacityAnimation.setEndValue(value)

    def setRadiusStartValue(self, value: float) -> None:
        self.m_radiusAnimation.setStartValue(value)

    def setRadiusEndValue(self, value: float) -> None:
        self.m_radiusAnimation.setEndValue(value)

    def setDuration(self, msecs: int) -> None:
        self.m_radiusAnimation.setDuration(msecs)
        self.m_opacityAnimation.setDuration(msecs)

    def setRadiusDuration(self, msecs: int):
        self.m_radiusAnimation.setDuration(msecs)

    def setOpacityDuration(self, msecs: int):
        self.m_opacityAnimation.setDuration(msecs)

    def destroy(self) -> None:
        self.m_overlay.removeRipple(self)

    _radius = Property(float, fset=setRadius, fget=radius)
    _opacity = Property(float, fset=setOpacity, fget=opacity)
