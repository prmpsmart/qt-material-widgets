from PySide6.QtCore import QEvent, QObject, QRect
from PySide6.QtWidgets import QWidget


class QtMaterialOverlayWidget(QWidget):
    def __init__(self, parent: QWidget = None):
        if parent:
            parent.installEventFilter(self)

    def __del__(self):
        ...

    def event(self, event: QEvent) -> bool:
        if not self.parent():
            return QWidget.event(event)

        type = event.type()

        if type == QEvent.ParentChange:

            self.parent().installEventFilter(self)
            self.setGeometry(self.overlayGeometry())

        elif type == QEvent.ParentAboutToChange:

            self.parent().removeEventFilter(self)
        return QWidget.event(event)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        type = event.type()

        if type in [QEvent.Move, QEvent.Resize]:
            self.setGeometry(self.overlayGeometry())
        return QWidget.eventFilter(obj, event)

    def overlayGeometry(self) -> QRect:

        widget: QWidget = self.parentWidget()
        if not widget:
            return QRect()

        return widget.rect()
