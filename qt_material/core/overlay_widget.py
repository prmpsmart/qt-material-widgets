from ._core import *


class QMaterialOverlayWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        if parent:
            parent.installEventFilter(self)

    def event(self, event: QEvent) -> bool:
        if not self.parent():
            return QWidget.event(self, event)

        e = event.type()
        if e == QEvent.ParentChange:
            self.parent().installEventFilter(self)
            self.setGeometry(self.overlayGeometry())

        elif e == QEvent.ParentAboutToChange:
            self.parent().removeEventFilter(self)

        return QWidget.event(self, event)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        e = event.type()
        if e in [QEvent.Move, QEvent.Resize]:
            self.setGeometry(self.overlayGeometry())

        return QWidget.eventFilter(self, obj, event)

    def overlayGeometry(self) -> QRect:
        widget: QWidget = self.parentWidget()
        if not widget:
            return QRect()
        return widget.rect()
