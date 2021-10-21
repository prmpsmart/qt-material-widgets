from PySide6.QtGui import QPaintEvent, QPainter, QPixmap, QTransform, QIcon, QColor
from PySide6.QtWidgets import *
from PySide6.QtCore import QSize, Qt

void = None
qreal = float


class QtMaterialCheckable:
    ...


class QtMaterialCheckableIcon(QWidget):
    def __init__(self, icon: QIcon, parent: QtMaterialCheckable = None):
        QWidget.__init__(self, parent)

        self.m_checkable: QtMaterialCheckable = parent
        self.m_color: QColor = Qt.black
        self.m_icon: QIcon = icon
        self.m_iconSize: qreal = 24
        self.m_opacity: qreal = 1.0

        assert parent

        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def __del__(self):
        ...

    def sizeHint(self) -> QSize:
        return QSize(self.m_iconSize, self.m_iconSize)

    def setIcon(self, icon: QIcon) -> void:

        self.m_icon = icon
        self.self.update()

    def icon(self) -> QIcon:
        return self.m_icon

    def setColor(self, color: QColor) -> void:
        self.m_color = color
        self.update()

    def color(self) -> QColor:
        return self.m_color

    def setIconSize(self, size: qreal) -> void:
        self.m_iconSize = size
        self.update()

    def iconSize(self) -> qreal:
        return self.m_iconSize

    def setOpacity(self, opacity: qreal) -> void:
        self.m_opacity = opacity
        self.update()

    def opacity(self) -> qreal:
        return self.m_opacity

    def paintEvent(self, event: QPaintEvent) -> void:
        
        painter:QPainter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setOpacity(self.m_opacity)

        pixmap: QPixmap = self.icon().pixmap(24, 24)

        if pixmap.isNull():
        
            p: qreal = ((self.height())-self.m_iconSize)/2
            z: qreal = self.m_iconSize/24

            t: QTransform= None
            if QtMaterialCheckable.LabelPositionLeft == self.m_checkable.labelPosition():
                
                t.translate(p+self.width()-42, p)
            else: 
                t.translate(p, p)
            
            t.scale(z, z)
            painter.setTransform(t)

            icon: QPainter = QPainter(pixmap)
            icon.setCompositionMode(QPainter.CompositionMode_SourceIn)
            icon.fillRect(pixmap.rect(), self.color())
            painter.drawPixmap(0, 0, pixmap)
        
