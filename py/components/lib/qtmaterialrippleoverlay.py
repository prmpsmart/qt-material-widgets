from PySide6.QtCore import QPoint, QPointF, Qt
from PySide6.QtGui import QPaintEngine, QPaintEvent, QPainter, QPainterPath
from PySide6.QtWidgets import QWidget


#include "lib/qtmaterialoverlaywidget.h"
QList = list
void = None
qreal = float
false = False
true = True

class QtMaterialRipple:...
class QtMaterialOverlayWidget:...

class QtMaterialRippleOverlay(QtMaterialOverlayWidget):

    def __init__(self, parent:QWidget = None):
        QtMaterialOverlayWidget.__init__(self, parent)

        self.m_ripples:QList[QtMaterialRipple] = None
        self.m_clipPath:QPainterPath = None
        self.m_useClip:bool = false
        
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)

    def __del__(self):
        ...

    def addRipple(self,  ripple: QtMaterialRipple=None, position: QPoint=None,  radius:qreal = 300)->void:

        if position and not ripple:
            ripple = QtMaterialRipple(position)
            ripple.setRadiusEndValue(radius)

        ripple.setOverlay(self)
        self.m_ripples.push_back(ripple)
        ripple.start()

        self.destroyed.connect(ripple.stop)
        self.destroyed.connect(ripple.deleteLater)


    def removeRipple(self, ripple: QtMaterialRipple)->void:
        if (self.m_ripples.removeOne(ripple)) :
            del ripple
            self.update()
        

    def setClipping(self, enable:bool )->void:
        self.m_useClip = enable
        self.update()
    def hasClipping(self)->bool:return self.m_useClip

    def setClipPath(self, path:QPainterPath)->void:
        self.m_clipPath = path
        self.update()

    def paintEvent(self, event:QPaintEvent) ->void:
        painter:QPainter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        if (self.m_useClip) :
            painter.setClipPath(self.m_clipPath)
        

        i: QtMaterialRipple = None
        for i in self.m_ripples:
            self.paintRipple(painter, i)
        

    def ripples(self)->QList[QtMaterialRipple]:
        return self.m_ripples

    def paintRipple(self,painter:QPaintEngine, ripple:QtMaterialRipple)->void:
        radius:qreal = ripple.radius()
        center:QPointF = ripple.center()
        painter.setOpacity(ripple.opacity())
        painter.setBrush(ripple.brush())
        painter.drawEllipse(center, radius, radius)
