from PySide6.QtCore import QStringConverter
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QCommonStyle

qreal = float
QHash = dict


class QtMaterialTheme:
    ...


class QtMaterialThemePrivate:
    def __init__(self, q: QtMaterialTheme):
        self.q_ptr: QtMaterialTheme = q
        self.colors: QHash[QStringConverter, QColor] = {}

    def __del__(self):
        ...

    def rgba(self, r: int, g: int, b: int, a: qreal) -> QColor:
        color: QColor = QColor(r, g, b)
        color.setAlphaF(a)
        return color
