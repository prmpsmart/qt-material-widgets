from ..core._core import *


class QMaterialDialogProxy(QWidget):
    class TransparencyMode(enum.Enum):
        Transparent = enum.auto()
        SemiTransparent = enum.auto()
        Opaque = enum.auto()

    Transparent = TransparencyMode.Transparent
    SemiTransparent = TransparencyMode.SemiTransparent
    Opaque = TransparencyMode.Opaque

    def __init__(
        self,
        source,
        layout: QStackedLayout,
        dialog,
        parent: QWidget = None,
    ):
        QWidget.__init__(self, parent)

        # from .dialog import QMaterialDialog, QMaterialDialogWindow

        self.m_source: 'QMaterialDialogWindow' = source
        self.m_layout = layout
        self.m_dialog: QMaterialDialog = dialog
        self.m_opacity = float()
        self.m_mode = self.Transparent

    def setOpacity(self, opacity: float) -> None:
        self.m_opacity = opacity
        self.m_mode = self.SemiTransparent
        self.update()
        self.m_dialog.update()

    def opacity(self) -> float:
        return self.m_opacity

    def makeOpaque(self) -> None:
        self.m_dialog.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.m_layout.setCurrentIndex(0)
        self.m_opacity = 1.0
        self.m_mode = self.Opaque
        self.update()

    def makeTransparent(self) -> None:
        self.m_opacity = 0.0
        self.m_mode = self.Transparent
        self.update()

    def sizeHint(self) -> QSize:
        return self.m_source.sizeHint()

    def event(self, event: QEvent) -> bool:
        type: QEvent.Type = event.type()

        if QEvent.Move == type or QEvent.Resize == type:
            self.m_source.setGeometry(self.geometry())

        return QWidget.event(self, event)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)

        if self.Transparent == self.m_mode:
            return
        elif self.Opaque != self.m_mode:
            painter.setOpacity(self.m_opacity)

        pm: QPixmap = self.m_source.grab(self.m_source.rect())
        painter.drawPixmap(0, 0, pm)

    _opacity = Property(float, fset=setOpacity, fget=opacity)
