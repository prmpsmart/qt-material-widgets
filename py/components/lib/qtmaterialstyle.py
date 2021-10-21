from PySide6.QtGui import QColor
from PySide6.QtWidgets import QCommonStyle

true = True
false = False
void = None
QString = str


def MATERIAL_DISABLE_THEME_COLORS(d):
    if d.useThemeColors == true:
        d.useThemeColors = false


class QtMaterialTheme:
    ...


class QtMaterialStyle:
    ...


class QtMaterialStylePrivate:
    ...


class QtMaterialStyle(QCommonStyle):
    def __init__(self):
        QCommonStyle.__init__(self)
        self.d: QtMaterialStylePrivate = QtMaterialStylePrivate(self)
        self.d.init()

    @staticmethod
    def instance() -> QtMaterialStyle:
        return QtMaterialStyle()

    def setTheme(self, theme: QtMaterialTheme) -> void:
        self.d.theme = theme
        theme.setParent(self)

    def themeColor(self, key: QString) -> QColor:
        assert self.d.theme
        return self.d.theme.getColor(key)

    # def __eq__(self, other):
