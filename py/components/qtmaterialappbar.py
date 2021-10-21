from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor

from lib.qtmaterialstyle import *


class QtMaterialAppBar:
    ...


class QtMaterialAppBarPrivate:
    q_ptr: QtMaterialAppBar = None
    useThemeColors: bool = False
    foregroundColor: QColor = None
    backgroundColor: QColor = None

    def init(self, q: QtMaterialAppBar = None) -> None:
        ...

    def __del__(self):
        ...
