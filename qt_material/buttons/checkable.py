from ..core.material_widget import *
from .checkable_icon import QMaterialCheckableIcon


class QMaterialCheckable(QAbstractButton, QMaterialWidget):
    class LabelPosition(enum.Enum):
        LabelPositionLeft = enum.auto()
        LabelPositionRight = enum.auto()

    LabelPositionLeft = LabelPosition.LabelPositionLeft
    LabelPositionRight = LabelPosition.LabelPositionRight

    def __init__(
        self,
        parent: QWidget = None,
        text: str = "",
        disabledColor: Union[QColor, Qt.GlobalColor] = None,
        checkedColor: Union[QColor, Qt.GlobalColor] = None,
        uncheckedColor: Union[QColor, Qt.GlobalColor] = None,
        textColor: Union[QColor, Qt.GlobalColor] = None,
        flipToggle: bool = False,
        **kwargs
    ):
        QAbstractButton.__init__(self, parent)

        self.m_disabledColor = QColor(disabledColor)
        self.m_checkedColor = QColor(checkedColor)
        self.m_uncheckedColor = QColor(uncheckedColor)
        self.m_textColor = QColor(textColor)
        self.flipToggle = flipToggle

        QMaterialWidget.__init__(self, **kwargs)

        self.m_rippleOverlay.installEventFilter(self)

        self.setText(text)

        self.m_checkedIcon = QMaterialCheckableIcon(
            self,
            QIcon(":toggle/check_box.svg"),
        )
        self.m_uncheckedIcon = QMaterialCheckableIcon(
            self,
            QIcon(":toggle/check_box_outline_blank.svg"),
        )
        self.stateMachine = QStateMachine(self)
        self.uncheckedState = QState()
        self.checkedState = QState()
        self.disabledUncheckedState = QState()
        self.disabledCheckedState = QState()
        self.uncheckedTransition = QSignalTransition(self.toggled)
        self.checkedTransition = QSignalTransition(self.toggled)
        self.m_labelPosition = QMaterialCheckable.LabelPositionRight

        self.setCheckable(True)
        self.setStyle(QMaterialStyle())
        self.setFont(QFont("Roboto", 11, QFont.Normal))

        self.stateMachine.addState(self.uncheckedState)
        self.stateMachine.addState(self.checkedState)
        self.stateMachine.addState(self.disabledUncheckedState)
        self.stateMachine.addState(self.disabledCheckedState)
        self.stateMachine.setInitialState(self.uncheckedState)

        # // Transition to checked

        self.uncheckedTransition.setTargetState(self.checkedState)
        self.uncheckedState.addTransition(self.uncheckedTransition)

        # // Transition to unchecked

        self.checkedTransition.setTargetState(self.uncheckedState)
        self.checkedState.addTransition(self.checkedTransition)

        # // Transitions enabled <==> disabled

        transition = QEventTransition(self, QEvent.EnabledChange)
        transition.setTargetState(self.disabledUncheckedState)
        self.uncheckedState.addTransition(transition)

        transition = QEventTransition(self, QEvent.EnabledChange)
        transition.setTargetState(self.uncheckedState)
        self.disabledUncheckedState.addTransition(transition)

        transition = QEventTransition(self, QEvent.EnabledChange)
        transition.setTargetState(self.disabledCheckedState)
        self.checkedState.addTransition(transition)

        transition = QEventTransition(self, QEvent.EnabledChange)
        transition.setTargetState(self.checkedState)
        self.disabledCheckedState.addTransition(transition)

        transition = QSignalTransition(self.toggled)
        transition.setTargetState(self.disabledCheckedState)
        self.disabledUncheckedState.addTransition(transition)

        transition = QSignalTransition(self.toggled)
        transition.setTargetState(self.disabledUncheckedState)
        self.disabledCheckedState.addTransition(transition)

        # //

        self.checkedState.assignProperty(self.m_checkedIcon, "_opacity", 1)
        self.checkedState.assignProperty(self.m_uncheckedIcon, "_opacity", 0)

        self.uncheckedState.assignProperty(self.m_checkedIcon, "_opacity", 0)
        self.uncheckedState.assignProperty(self.m_uncheckedIcon, "_opacity", 1)

        self.disabledCheckedState.assignProperty(self.m_checkedIcon, "_opacity", 1)
        self.disabledCheckedState.assignProperty(self.m_uncheckedIcon, "_opacity", 0)

        self.disabledUncheckedState.assignProperty(self.m_checkedIcon, "_opacity", 0)
        self.disabledUncheckedState.assignProperty(self.m_uncheckedIcon, "_opacity", 1)

        self.checkedState.assignProperty(
            self.m_checkedIcon, "_color", self.checkedColor()
        )
        self.checkedState.assignProperty(
            self.m_uncheckedIcon, "_color", self.checkedColor()
        )

        self.uncheckedState.assignProperty(
            self.m_uncheckedIcon, "_color", self.uncheckedColor()
        )
        self.uncheckedState.assignProperty(
            self.m_uncheckedIcon, "_color", self.uncheckedColor()
        )

        self.disabledUncheckedState.assignProperty(
            self.m_uncheckedIcon, "_color", self.disabledColor()
        )
        self.disabledCheckedState.assignProperty(
            self.m_checkedIcon, "_color", self.disabledColor()
        )

        self.stateMachine.start()
        QCoreApplication.processEvents()

    def setRippleColor(self, color: Union[QColor, Qt.GlobalColor]) -> None:
        self.m_rippleColor = QColor(color)
        self.m_rippleOverlay.setColor(self.rippleColor())

    def rippleColor(self) -> QColor:
        return self.checkedColor() if self.isChecked() else self.uncheckedColor()

    def setLabelPosition(self, placement: LabelPosition) -> None:
        self.m_labelPosition = placement
        self.update()

    def labelPosition(self) -> LabelPosition:
        return self.m_labelPosition

    def setCheckedColor(self, color: QColor) -> None:
        self.m_checkedColor = color
        MATERIAL_DISABLE_THEME_COLORS(self)
        self.setupProperties()

    def checkedColor(self) -> QColor:
        if (not self.m_checkedColor.isValid()) and self.m_useThemeColors:
            return QMaterialStyle().themeColor("primary1")
        else:
            return self.m_checkedColor

    def setUncheckedColor(self, color: QColor) -> None:
        self.m_uncheckedColor = color
        MATERIAL_DISABLE_THEME_COLORS(self)
        self.setupProperties()

    def uncheckedColor(self) -> QColor:
        if (not self.m_uncheckedColor.isValid()) and self.m_useThemeColors:
            return QMaterialStyle().themeColor("text")
        else:
            return self.m_uncheckedColor

    def setTextColor(self, color: QColor) -> None:
        self.m_textColor = QColor(color)
        MATERIAL_DISABLE_THEME_COLORS(self)
        self.setupProperties()

    def textColor(self) -> QColor:
        if (not self.m_textColor.isValid()) and self.m_useThemeColors:
            return QMaterialStyle().themeColor("text")
        else:
            return self.m_textColor

    def setDisabledColor(self, color: QColor) -> None:
        self.m_disabledColor = QColor(color)
        MATERIAL_DISABLE_THEME_COLORS(self)
        self.setupProperties()

    def disabledColor(self) -> QColor:
        if (not self.m_disabledColor.isValid()) and self.m_useThemeColors:
            return QMaterialStyle().themeColor("accent3")
        else:
            return self.m_disabledColor

    def setCheckedIcon(self, icon: QIcon) -> None:
        self.m_checkedIcon.setIcon(icon)
        self.update()

    def checkedIcon(self) -> QIcon:
        return self.m_checkedIcon.icon()

    def setUncheckedIcon(self, icon: QIcon) -> None:
        self.m_uncheckedIcon.setIcon(icon)
        self.update()

    def uncheckedIcon(self) -> QIcon:
        return self.m_uncheckedIcon.icon()

    def sizeHint(self) -> QSize:
        if self.text():
            return QSize(40, 40)

        return QSize(
            self.fontMetrics().size(Qt.TextShowMnemonic, self.text()).width() + 52, 40
        )

    def event(self, event: QEvent) -> bool:
        e = event.type()
        if e in [QEvent.Resize, QEvent.Move]:
            rect = self.rect()
            self.m_checkedIcon.setGeometry(rect)
            self.m_uncheckedIcon.setGeometry(rect)

        elif e == QEvent.ParentChange:
            widget = QWidget()
            if widget == self.parentWidget():
                self.m_rippleOverlay.setParent(widget)

        return QAbstractButton.event(self, event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if not self.isEnabled():
            return

        self.rippleOverlay().addRipple(center=event.pos(), color=self.rippleColor())

        self.setChecked(not self.isChecked())

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setPen(
            QPen(self.textColor() if self.isEnabled() else self.disabledColor())
        )

        if QMaterialCheckable.LabelPositionLeft == self.m_labelPosition:
            painter.drawText(4, 25, self.text())
        else:
            painter.drawText(48, 25, self.text())

        painter.end()

    def setupProperties(self) -> None:
        self.m_checkedState.assignProperty(
            self.m_checkedIcon, "_color", self.checkedColor()
        )
        self.m_checkedState.assignProperty(
            self.m_uncheckedIcon, "_color", self.checkedColor()
        )
        self.m_uncheckedState.assignProperty(
            self.m_uncheckedIcon, "_color", self.uncheckedColor()
        )
        self.m_disabledUncheckedState.assignProperty(
            self.m_uncheckedIcon, "_color", self.disabledColor()
        )
        self.m_disabledCheckedState.assignProperty(
            self.m_checkedIcon, "_color", self.disabledColor()
        )

        if self.isEnabled():
            if self.isChecked():
                self.m_checkedIcon.setColor(self.checkedColor())
            else:
                self.m_uncheckedIcon.setColor(self.uncheckedColor())

        else:
            self.m_checkedIcon.setColor(self.disabledColor())
            self.m_uncheckedIcon.setColor(self.disabledColor())

        self.update()
