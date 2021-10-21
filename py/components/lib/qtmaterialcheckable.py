from PySide6.QtCore import QEvent, QObject, QPoint, QSize, Qt
from PySide6.QtGui import (
    QColor,
    QIcon,
    QMouseEvent,
    QPaintEngine,
    QPaintEvent,
    QPainter,
    QPen,
)
from PySide6.QtWidgets import QAbstractButton, QWidget
from enum import Enum


class QtMaterialStyle:
    ...


class QtMaterialCheckablePrivate:
    ...


class QtMaterialRipple:
    ...


void = None
qreal = float


class QtMaterialCheckable(QAbstractButton):
    class LabelPosition(Enum):
        LabelPositionLeft = 1
        LabelPositionRight = 2

    def __init__(self, d: QtMaterialCheckablePrivate, parent: QWidget = None):
        QAbstractButton.__init__(self, d, parent)
        #  QScopedPointer<QtMaterialCheckablePrivate>
        self.d: QtMaterialCheckablePrivate = d

    def setLabelPosition(self, placement: LabelPosition) -> void:
        self.d.labelPosition = placement
        self.update()

    def labelPosition(self) -> LabelPosition:
        return self.d.labelPosition

    def setUseThemeColors(self, value: bool) -> void:
        if self.d.useThemeColors == value:
            return

        self.d.useThemeColors = value
        self.setupProperties()

    def useThemeColors(self) -> bool:
        return self.d.useThemeColors

    def setCheckedColor(self, color: QColor) -> void:

        self.d.checkedColor = color

        # MATERIAL_DISABLE_THEME_COLORS
        self.setupProperties()

    def checkedColor(self) -> QColor:
        if self.d.useThemeColors or not self.dcheckedColor.isValid():
            return QtMaterialStyle.instance().themeColor("primary1")
        else:
            return self.d.checkedColor

    def setUncheckedColor(self, color: QColor) -> void:
        self.d.uncheckedColor = color

        # MATERIAL_DISABLE_THEME_COLORS
        self.setupProperties()

    def uncheckedColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.uncheckedColor.isValid():
            return QtMaterialStyle.instance().themeColor("text")
        else:
            return self.d.uncheckedColor

    def setTextColor(self, color: QColor) -> void:
        self.d.textColor = color

        # MATERIAL_DISABLE_THEME_COLORS
        self.setupProperties()

    def textColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.textColor.isValid():
            return QtMaterialStyle.instance().themeColor("text")
        else:
            return self.d.textColor

    def setDisabledColor(self, color: QColor) -> void:
        self.d.disabledColor = color

        # MATERIAL_DISABLE_THEME_COLORS
        self.setupProperties()

    def disabledColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.disabledColor.isValid():
            return QtMaterialStyle.instance().themeColor("accent3")
        else:
            return self.d.disabledColor

    def setCheckedIcon(self, icon: QIcon) -> void:
        self.d.checkedIcon.setIcon(icon)
        self.update()

    def checkedIcon(self) -> QIcon:
        return self.d.checkedIcon.icon()

    def setUncheckedIcon(self, icon: QIcon) -> void:
        self.d.uncheckedIcon.setIcon(icon)
        self.update()

    def uncheckedIcon(self) -> QIcon:
        return self.d.uncheckedIcon.icon()

    def sizeHint(self) -> QSize:
        if self.text().isEmpty():
            return QSize(40, 40)

        return QSize(
            self.fontMetrics().size(Qt.TextShowMnemonic, self.text()).width() + 52, 40
        )

    def event(self, event: QEvent) -> bool:
        typee = event.type()
        if typee in [QEvent.Resize, QEvent.Move]:

            self.d.checkedIcon.setGeometry(self.rect())
            self.d.uncheckedIcon.setGeometry(self.rect())
            self.d.rippleOverlay.setGeometry(self.geometry().adjusted(-8, -8, 8, 8))

        elif typee == QEvent.ParentChange:

            widget: QWidget = None
            if widget == self.parentWidget():
                self.d.rippleOverlay.setParent(widget)

        return QAbstractButton.event(event)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if QEvent.Resize == event.type():

            # Q_D(QtMaterialCheckable)

            self.d.rippleOverlay.setGeometry(self.geometry().adjusted(-8, -8, 8, 8))

        return QAbstractButton.eventFilter(obj, event)

    def mousePressEvent(self, event: QMouseEvent) -> void:
        if not self.isEnabled():
            return

        ripple: QtMaterialRipple = None
        if QtMaterialCheckable.LabelPositionLeft == self.d.labelPosition:
            ripple = QtMaterialRipple(QPoint(self.width() - 14, 28))
        else:
            ripple = QtMaterialRipple(QPoint(28, 28))

        self.ripple.setRadiusEndValue(22)
        self.ripple.setColor(
            self.checkedColor if self.isChecked() else self.uncheckedColor()
        )

        if self.isChecked():
            self.selfle.setOpacityStartValue(1)

        self.rippleOverlay.addRipple(ripple)

        self.setChecked(not self.isChecked())

    def paintEvent(self, event: QPaintEvent) -> void:

        painter: QPaintEngine = QPainter(self)

        pen: QPen = QPen(self.parent())
        pen.setColor(self.textColor() if self.isEnabled() else self.disabledColor())
        painter.setPen(pen)

        if QtMaterialCheckable.LabelPositionLeft == self.d.labelPosition:
            painter.drawText(4, 25, self.text())
        else:
            painter.drawText(48, 25, self.text())

    def setupProperties(self) -> void:
        self.selfeckedState.assignProperty(
            self.d.checkedIcon, "color", self.checkedColor()
        )
        self.selfeckedState.assignProperty(
            self.d.uncheckedIcon, "color", self.checkedColor()
        )
        self.selfcheckedState.assignProperty(
            self.d.uncheckedIcon, "color", self.uncheckedColor()
        )
        self.selfsabledUncheckedState.assignProperty(
            self.d.uncheckedIcon, "color", self.disabledColor()
        )
        self.selfsabledCheckedState.assignProperty(
            self.d.checkedIcon, "color", self.disabledColor()
        )

        if self.isEnabled():
            if self.isChecked():
                self.selfeckedIcon.setColor(self.checkedColor())
            else:
                self.selfcheckedIcon.setColor(self.uncheckedColor())

        else:
            self.selfeckedIcon.setColor(self.disabledColor())
            self.selfcheckedIcon.setColor(self.disabledColor())

        self.update()
