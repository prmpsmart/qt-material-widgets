from .checkable import *


class QMaterialRadioButton(QMaterialCheckable):
    def __init__(self, parent: QWidget = None, **kwargs):
        QMaterialCheckable.__init__(self, parent, **kwargs)
        self.setAutoExclusive(True)

        self.setCheckedIcon(QIcon(":/toggle/radio_button_checked.svg"))
        self.setUncheckedIcon(QIcon(":/toggle/radio_button_unchecked.svg"))

        self.uncheckedState.assignProperty(self.m_checkedIcon, "_iconSize", 0)
        self.uncheckedState.assignProperty(self.m_uncheckedIcon, "_iconSize", 24)

        self.disabledUncheckedState.assignProperty(self.m_checkedIcon, "_iconSize", 0)
        self.disabledUncheckedState.assignProperty(
            self.m_uncheckedIcon, "_iconSize", 24
        )

        self.checkedState.assignProperty(self.m_uncheckedIcon, "_iconSize", 0)
        self.checkedState.assignProperty(self.m_checkedIcon, "_iconSize", 24)

        self.disabledCheckedState.assignProperty(self.m_uncheckedIcon, "_iconSize", 0)
        self.disabledCheckedState.assignProperty(self.m_checkedIcon, "_iconSize", 24)

        self.uncheckedState.assignProperty(self.m_checkedIcon, "_opacity", 0)
        self.uncheckedState.assignProperty(self.m_uncheckedIcon, "_opacity", 1)

        self.checkedState.assignProperty(self.m_uncheckedIcon, "_opacity", 0)
        self.checkedState.assignProperty(self.m_checkedIcon, "_opacity", 1)

        self.m_checkedIcon.setIconSize(0)

        self.checkedState.assignProperty(
            self.m_checkedIcon, "_color", self.checkedColor()
        )
        self.checkedState.assignProperty(
            self.m_uncheckedIcon, "_color", self.uncheckedColor()
        )
        self.uncheckedState.assignProperty(
            self.m_uncheckedIcon, "_color", self.uncheckedColor()
        )

        animation = QPropertyAnimation(self.m_checkedIcon, b"_iconSize", self)
        animation.setDuration(250)
        self.stateMachine.addDefaultAnimation(animation)

        animation = QPropertyAnimation(self.m_uncheckedIcon, b"_iconSize", self)
        animation.setDuration(250)
        self.stateMachine.addDefaultAnimation(animation)

        animation = QPropertyAnimation(self.m_uncheckedIcon, b"_opacity", self)
        animation.setDuration(250)
        self.stateMachine.addDefaultAnimation(animation)

        animation = QPropertyAnimation(self.m_checkedIcon, b"_opacity", self)
        animation.setDuration(250)
        self.stateMachine.addDefaultAnimation(animation)

    def setupProperties(self) -> None:
        QMaterialCheckable.setupProperties(self)

        self.m_checkedState.assignProperty(
            self.m_checkedIcon, "_color", self.checkedColor()
        )
        self.m_checkedState.assignProperty(
            self.m_uncheckedIcon, "_color", self.uncheckedColor()
        )
        self.m_uncheckedState.assignProperty(
            self.m_uncheckedIcon, "_color", self.uncheckedColor()
        )
