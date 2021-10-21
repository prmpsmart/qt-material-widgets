from PySide6.QtCore import QEvent
from PySide6.QtGui import QColor, QFont, QIcon
from PySide6.QtStateMachine import QSignalTransition, QState, QStateMachine, QAbstractTransition, QEventTransition



# include <QtGlobal>
class QtMaterialCheckable:  
    ...


class QtMaterialRippleOverlay:
    ...


class QtMaterialStyle:
    ...


class QtMaterialCheckableIcon:
    ...




true = True
false = False


class QtMaterialCheckablePrivate:
    def __init__(self, q: QtMaterialCheckable):

        self.q_ptr: QtMaterialCheckable = q

        self.rippleOverlay: QtMaterialRippleOverlay = QtMaterialRippleOverlay()
        self.checkedIcon: QtMaterialCheckableIcon = QtMaterialCheckableIcon(
            QIcon(":/icons/icons/toggle/svg/production/ic_check_box_24px.svg"), q
        )
        self.uncheckedIcon: QtMaterialCheckableIcon = QtMaterialCheckableIcon(
            QIcon(
                ":/icons/icons/toggle/svg/production/ic_check_box_outline_blank_24px.svg"
            ),
            q,
        )
        self.stateMachine: QStateMachine = QStateMachine(q)
        self.uncheckedState: QState = QState()
        self.checkedState: QState = QState()
        self.disabledUncheckedState: QState = QState()
        self.disabledCheckedState: QState = QState()
        self.uncheckedTransition: QSignalTransition = QSignalTransition(q, self.toggled)
        self.checkedTransition: QSignalTransition = QSignalTransition(q, self.toggled)
        self.labelPosition: QtMaterialCheckable.LabelPosition = (
            QtMaterialCheckable.LabelPositionRight
        )

        self.checkedColor: QColor = None
        self.uncheckedColor: QColor = None
        self.textColor: QColor = None
        self.disabledColor: QColor = None

        self.useThemeColors: bool = True

        self.rippleOverlay.setParent(q.parentWidget())
        self.rippleOverlay.installEventFilter(q)

        q.setCheckable(true)
        q.setStyle(QtMaterialStyle.instance())
        q.setFont(QFont("Roboto", 11, QFont.Normal))

        self.stateMachine.addState(self.uncheckedState)
        self.stateMachine.addState(self.checkedState)
        self.stateMachine.addState(self.disabledUncheckedState)
        self.stateMachine.addState(self.disabledCheckedState)
        self.stateMachine.setInitialState(self.uncheckedState)

        # Transition to checked

        self.uncheckedTransition.setTargetState(self.checkedState)
        self.uncheckedState.addTransition(self.uncheckedTransition)

        # Transition to unchecked

        self.checkedTransition.setTargetState(self.uncheckedState)
        self.checkedState.addTransition(self.checkedTransition)

        transition: QAbstractTransition = None

        # Transitions enabled <==> disabled

        transition = QEventTransition(q, QEvent.EnabledChange)
        transition.setTargetState(self.disabledUncheckedState)
        self.uncheckedState.addTransition(transition)

        transition = QEventTransition(q, QEvent.EnabledChange)
        transition.setTargetState(self.uncheckedState)
        self.disabledUncheckedState.addTransition(transition)

        transition = QEventTransition(q, QEvent.EnabledChange)
        transition.setTargetState(self.disabledCheckedState)
        self.checkedState.addTransition(transition)

        transition = QEventTransition(q, QEvent.EnabledChange)
        transition.setTargetState(self.checkedState)
        self.disabledCheckedState.addTransition(transition)

        transition = QSignalTransition(q, self.toggled)
        transition.setTargetState(self.disabledCheckedState)
        self.disabledUncheckedState.addTransition(transition)

        transition = QSignalTransition(q, self.toggled)
        transition.setTargetState(self.disabledUncheckedState)
        self.disabledCheckedState.addTransition(transition)

        #

        self.checkedState.assignProperty(self.checkedIcon, "opacity", 1)
        self.checkedState.assignProperty(self.uncheckedIcon, "opacity", 0)

        self.uncheckedState.assignProperty(self.checkedIcon, "opacity", 0)
        self.uncheckedState.assignProperty(self.uncheckedIcon, "opacity", 1)

        self.disabledCheckedState.assignProperty(self.checkedIcon, "opacity", 1)
        self.disabledCheckedState.assignProperty(self.uncheckedIcon, "opacity", 0)

        self.disabledUncheckedState.assignProperty(self.checkedIcon, "opacity", 0)
        self.disabledUncheckedState.assignProperty(self.uncheckedIcon, "opacity", 1)

        self.checkedState.assignProperty(self.checkedIcon, "color", q.checkedColor())
        self.checkedState.assignProperty(self.uncheckedIcon, "color", q.checkedColor())

        self.uncheckedState.assignProperty(
            self.uncheckedIcon, "color", q.uncheckedColor()
        )
        self.uncheckedState.assignProperty(
            self.uncheckedIcon, "color", q.uncheckedColor()
        )

        self.disabledUncheckedState.assignProperty(
            self.uncheckedIcon, "color", q.disabledColor()
        )
        self.disabledCheckedState.assignProperty(
            self.checkedIcon, "color", q.disabledColor()
        )

        self.stateMachine.start()
        self.QCoreApplication.processEvents()
