from ..core.overlay_widget import *



class QMaterialDrawerWidget(QMaterialOverlayWidget):
    def __init__(self, parent: QWidget = None):
        QMaterialOverlayWidget.__init__(self, parent)

        self.m_offset = int(0)

    def setOffset(self, offset: int) -> None:
        self.m_offset = offset

        widget: QWidget = self.parentWidget()
        if widget:
            self.setGeometry(widget.rect().translated(offset, 0))
        self.update()

    def offset(self) -> int:
        return self.m_offset

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(Qt.white)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)

        painter.drawRect(self.rect().adjusted(0, 0, -16, 0))

        gradient = QLinearGradient(
            QPointF(self.width() - 16, 0), QPointF(self.width(), 0)
        )
        gradient.setColorAt(0, QColor(0, 0, 0, 80))
        gradient.setColorAt(0.5, QColor(0, 0, 0, 20))
        gradient.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(gradient))

        painter.drawRect(self.width() - 16, 0, 16, self.height())

    def overlayGeometry(self) -> QRect:
        return QMaterialOverlayWidget.overlayGeometry(self).translated(self.m_offset, 0)

    _offset = Property(int, fset=setOffset, fget=offset)

