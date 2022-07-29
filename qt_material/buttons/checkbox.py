from .checkable import *


class QMaterialCheckBox(QMaterialCheckable):
    def __init__(self, parent: QWidget = None, **kwargs):
        QMaterialCheckable.__init__(self, parent=parent, **kwargs)

        self.checkedState.assignProperty(self.m_checkedIcon, "_iconSize", 24)
        self.uncheckedState.assignProperty(self.m_checkedIcon, "_iconSize", 0)

        animation = QPropertyAnimation(self.m_checkedIcon, b"_iconSize", self)
        animation.setDuration(300)
        self.uncheckedTransition.addAnimation(animation)

        animation = QPropertyAnimation(self.m_checkedIcon, b"_iconSize", self)
        animation.setDuration(1300)
        self.checkedTransition.addAnimation(animation)

        animation = QPropertyAnimation(self.m_checkedIcon, b"_opacity", self)
        animation.setDuration(440)
        self.checkedTransition.addAnimation(animation)

        animation = QPropertyAnimation(self.m_checkedIcon, b"_opacity", self)
        animation.setDuration(440)
        self.uncheckedTransition.addAnimation(animation)

        animation = QPropertyAnimation(self.m_uncheckedIcon, b"_opacity", self)
        animation.setDuration(440)
        self.checkedTransition.addAnimation(animation)

        animation = QPropertyAnimation(self.m_uncheckedIcon, b"_opacity", self)
        animation.setDuration(440)
        self.uncheckedTransition.addAnimation(animation)

        animation = QPropertyAnimation(self.m_uncheckedIcon, b"_color", self)
        animation.setDuration(440)
        self.checkedTransition.addAnimation(animation)

        animation = QPropertyAnimation(self.m_uncheckedIcon, b"_color", self)
        animation.setDuration(440)
        self.uncheckedTransition.addAnimation(animation)
