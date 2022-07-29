from .lib.qtmaterial import *


class QtMaterialCheckBoxPrivate(QtMaterialCheckablePrivate):
    def __init__(self, q: "QtMaterialCheckBox") -> void:
        QtMaterialCheckablePrivate.__init__(self, q)

    def init(self) -> void:
        q = self.q
        self.checkedState.assignProperty(self.checkedIcon, "_iconSize", 24)
        self.uncheckedState.assignProperty(self.checkedIcon, "_iconSize", 0)

        animation = QPropertyAnimation(self.checkedIcon, "_iconSize", q)
        animation.setDuration(300)
        self.uncheckedTransition.addAnimation(animation)

        animation = QPropertyAnimation(self.checkedIcon, "_iconSize", q)
        animation.setDuration(1300)
        self.checkedTransition.addAnimation(animation)

        animation = QPropertyAnimation(self.checkedIcon, "_opacity", q)
        animation.setDuration(440)
        self.checkedTransition.addAnimation(animation)

        animation = QPropertyAnimation(self.checkedIcon, "_opacity", q)
        animation.setDuration(440)
        self.uncheckedTransition.addAnimation(animation)

        animation = QPropertyAnimation(self.uncheckedIcon, "_opacity", q)
        animation.setDuration(440)
        self.checkedTransition.addAnimation(animation)

        animation = QPropertyAnimation(self.uncheckedIcon, "_opacity", q)
        animation.setDuration(440)
        self.uncheckedTransition.addAnimation(animation)

        animation = QPropertyAnimation(self.uncheckedIcon, "_color", q)
        animation.setDuration(440)
        self.checkedTransition.addAnimation(animation)

        animation = QPropertyAnimation(self.uncheckedIcon, "_color", q)
        animation.setDuration(440)
        self.uncheckedTransition.addAnimation(animation)


class QtMaterialCheckBox(QtMaterialCheckable):
    def __init__(self, d: QtMaterialCheckablePrivate, parent: QWidget = void):

        self.d = QtMaterialCheckBoxPrivate(self)

        QtMaterialCheckable.__init__(self, self.d, parent=parent)

        self.d.init()
