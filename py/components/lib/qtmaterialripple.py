from typing import overload
from PySide6.QtCore import QByteArray, QEasingCurve, QObject, QParallelAnimationGroup, QPoint, QPropertyAnimation, Qt
from PySide6.QtGui import QBrush, QColor

qreal = float
void = None


class QtMaterialRippleOverlay:
    ...


class QtMaterialRipple(QParallelAnimationGroup):
    def __init__(
        self,
        center: QPoint,
        overlay: QtMaterialRippleOverlay = None,
        parent: QObject = None,
    ):
        QParallelAnimationGroup.__init__(self, parent)

        self.m_overlay: QtMaterialRippleOverlay = overlay
        self.m_radiusAnimation: QPropertyAnimation = self.animate("radius")
        self.m_opacityAnimation: QPropertyAnimation = self.animate("opacity")
        self.m_radius: qreal = 0
        self.m_opacity: qreal = 0
        self.m_center: QPoint = center
        self.m_brush: QBrush = None

        self.init()

    def __del__(self):
        ...

    def setOverlay(self, overlay: QtMaterialRippleOverlay) -> void:
        self.m_overlay = overlay

    def radius(self) -> qreal:
        return self.m_radius
    
    def setRadius(self, radius: qreal)->void:
    
        assert self.m_overlay

        if (self.m_radius == radius) :
            return;
        
        self.m_radius = radius
        self.m_overlay.update()
    
    
    def opacity(self) -> qreal:
        return self.m_opacity
    
    def setOpacity(self, opacity: qreal)->void:
    
        assert self.m_overlay

        if (self.m_opacity == opacity) :
            return
        
        self.m_opacity = opacity
        self.m_overlay.update()
    

    def color(self) -> QColor:
        return self.m_brush.color()

    def setColor(self, color: QColor)->void:
    
        if (self.m_brush.color() == color) :
            return
        
        self.m_brush.setColor(color)

        if (self.m_overlay) :
            self.m_overlay.update()
        
    

    def brush(self) -> QBrush:
        return self.m_brush
    
    def setBrush(self,  brush:QBrush)->void:
    
        self.m_brush = brush

        if (self.m_overlay) :
            self.m_overlay.update();

    def center(self) -> QPoint:
        return self.m_center

    def radiusAnimation(self) -> QPropertyAnimation:
        return self.m_radiusAnimation

    def opacityAnimation(self) -> QPropertyAnimation:
        return self.m_opacityAnimation

    def setOpacityStartValue(self, value: qreal) -> void:
        self.m_opacityAnimation.setStartValue(value)

    def setOpacityEndValue(self, value: qreal) -> void:
        self.m_opacityAnimation.setEndValue(value)

    def setRadiusStartValue(self, value: qreal) -> void:
        self.m_radiusAnimation.setStartValue(value)

    def setRadiusEndValue(self, value: qreal) -> void:
        self.m_radiusAnimation.setEndValue(value)

    def setDuration(self, msecs: int) -> void:
        self.m_radiusAnimation.setDuration(msecs)
        self.m_opacityAnimation.setDuration(msecs)
    
        
    def animate(self, property:QByteArray,  easing:QEasingCurve, duration:int)->QPropertyAnimation:
        animation: QPropertyAnimation = QPropertyAnimation()
        animation.setTargetObject(self)
        animation.setPropertyName(property)
        animation.setEasingCurve(easing)
        animation.setDuration(duration)
        self.addAnimation(animation)
        return animation
    

    def init(self)->    void:
    
        self.setOpacityStartValue(0.5);
        self.setOpacityEndValue(0);
        self.setRadiusStartValue(0);
        self.setRadiusEndValue(300);

        self.m_brush.setColor(Qt.black);
        self.m_brush.setStyle(Qt.SolidPattern);

        self.finished.connect(self.destroy);

