from .lib.qtmaterial import *


class QtMaterialCheckBox:
    ...


class QtMaterialCheckBoxPrivate(QtMaterialCheckablePrivate):
    def __init__(self, q: QtMaterialCheckBox) -> void:
        QtMaterialCheckablePrivate.__init__(self, q)

    def init(self) -> void:
        q = self.q
        self.checkedState.assignProperty(self.checkedIcon, "iconSize", 24)
        self.uncheckedState.assignProperty(self.checkedIcon, "iconSize", 0)

        animation = QPropertyAnimation()

        animation = QPropertyAnimation(self.checkedIcon, "iconSize", q)
        animation.setDuration(300)
        self.uncheckedTransition.addAnimation(animation)

        animation = QPropertyAnimation(self.checkedIcon, "iconSize", q)
        animation.setDuration(1300)
        self.checkedTransition.addAnimation(animation)

        animation = QPropertyAnimation(self.checkedIcon, "opacity", q)
        animation.setDuration(440)
        self.checkedTransition.addAnimation(animation)

        animation = QPropertyAnimation(self.checkedIcon, "opacity", q)
        animation.setDuration(440)
        self.uncheckedTransition.addAnimation(animation)

        animation = QPropertyAnimation(self.uncheckedIcon, "opacity", q)
        animation.setDuration(440)
        self.checkedTransition.addAnimation(animation)

        animation = QPropertyAnimation(self.uncheckedIcon, "opacity", q)
        animation.setDuration(440)
        self.uncheckedTransition.addAnimation(animation)

        animation = QPropertyAnimation(self.uncheckedIcon, "color", q)
        animation.setDuration(440)
        self.checkedTransition.addAnimation(animation)

        animation = QPropertyAnimation(self.uncheckedIcon, "color", q)
        animation.setDuration(440)
        self.uncheckedTransition.addAnimation(animation)


class QtMaterialCheckBox(QtMaterialCheckable):
    def __init__(self, d: QtMaterialCheckablePrivate, parent: QWidget = void):

        self.d = QtMaterialCheckBoxPrivate(self)

        QtMaterialCheckable.__init__(self, self.d, parent=parent)

        self.d.init()
