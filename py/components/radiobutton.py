from .lib.qtmaterial import *


class QtMaterialRadioButton:
    ...


class QtMaterialRadioButtonPrivate(QtMaterialCheckablePrivate):
    def __init__(self, q: QtMaterialRadioButton):
        QtMaterialCheckablePrivate.__init__(self)

        self.q = q

    def init(self) -> void:
        self.q.setAutoExclusive(true)

        self.q.setCheckedIcon(QIcon(":/icons/toggle/ic_radio_button_checked_24px.svg"))
        self.q.setUncheckedIcon(
            QIcon(":/icons/toggle/ic_radio_button_unchecked_24px.svg")
        )

        self.uncheckedState.assignProperty(self.checkedIcon, "iconSize", 0)
        self.uncheckedState.assignProperty(self.uncheckedIcon, "iconSize", 24)

        self.disabledUncheckedState.assignProperty(self.checkedIcon, "iconSize", 0)
        self.disabledUncheckedState.assignProperty(self.uncheckedIcon, "iconSize", 24)

        self.checkedState.assignProperty(self.uncheckedIcon, "iconSize", 0)
        self.checkedState.assignProperty(self.checkedIcon, "iconSize", 24)

        self.disabledCheckedState.assignProperty(self.uncheckedIcon, "iconSize", 0)
        self.disabledCheckedState.assignProperty(self.checkedIcon, "iconSize", 24)

        self.uncheckedState.assignProperty(self.checkedIcon, "opacity", 0)
        self.uncheckedState.assignProperty(self.uncheckedIcon, "opacity", 1)

        self.checkedState.assignProperty(self.uncheckedIcon, "opacity", 0)
        self.checkedState.assignProperty(self.checkedIcon, "opacity", 1)

        self.checkedIcon.setIconSize(0)

        self.checkedState.assignProperty(
            self.checkedIcon, "color", self.q.checkedColor()
        )
        self.checkedState.assignProperty(
            self.uncheckedIcon, "color", self.q.uncheckedColor()
        )
        self.uncheckedState.assignProperty(
            self.uncheckedIcon, "color", self.q.uncheckedColor()
        )

        q = self.q
        animation = QPropertyAnimation(self.checkedIcon, "iconSize", q)
        animation.setDuration(250)
        self.stateMachine.addDefaultAnimation(animation)

        animation = QPropertyAnimation(self.uncheckedIcon, "iconSize", q)
        animation.setDuration(250)
        self.stateMachine.addDefaultAnimation(animation)

        animation = QPropertyAnimation(self.uncheckedIcon, "opacity", q)
        animation.setDuration(250)
        self.stateMachine.addDefaultAnimation(animation)

        animation = QPropertyAnimation(self.checkedIcon, "opacity", q)
        animation.setDuration(250)
        self.stateMachine.addDefaultAnimation(animation)


class QtMaterialRadioButton(QtMaterialCheckable):
    def __init__(self, parent: QWidget = None):
        QtMaterialCheckable.__init__(self, parent)
        self.d = QtMaterialRadioButtonPrivate(self)
        self.d.init()

    def setupProperties(self) -> void:
        QtMaterialCheckable.setupProperties(self)

        self.d.checkedState.assignProperty(
            self.d.checkedIcon, "color", self.checkedColor()
        )
        self.d.checkedState.assignProperty(
            self.d.uncheckedIcon, "color", self.uncheckedColor()
        )
        self.d.uncheckedState.assignProperty(
            self.d.uncheckedIcon, "color", self.uncheckedColor()
        )
