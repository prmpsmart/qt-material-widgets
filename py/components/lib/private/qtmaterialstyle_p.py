from PySide6.QtGui import QFontDatabase


void = None


class QtMaterialStyle:
    ...


class QtMaterialTheme:
    ...


class QtMaterialStylePrivate:
    def __init__(self, q: QtMaterialStyle):
        self.q_ptr: QtMaterialStyle = q
        self.theme: QtMaterialTheme = None

    def __del__(self):
        ...

    def init(self) -> void:
        QFontDatabase.addApplicationFont(":/fonts/roboto_regular")
        QFontDatabase.addApplicationFont(":/fonts/roboto_medium")
        QFontDatabase.addApplicationFont(":/fonts/roboto_bold")

        self.q.setTheme(QtMaterialTheme())
