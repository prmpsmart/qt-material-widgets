from ._core import *
from .ripple_overlay import QMaterialRippleOverlay


class QMaterialWidget:
    def __init__(
        self,
        easingCurve: QEasingCurve = QEasingCurve.OutBounce,
        useThemeColors: bool = True,
        foregroundColor: Union[QColor, Qt.GlobalColor] = None,
        backgroundColor: Union[QColor, Qt.GlobalColor] = None,
        disabledForegroundColor: Union[QColor, Qt.GlobalColor] = None,
        disabledBackgroundColor: Union[QColor, Qt.GlobalColor] = None,
        overlayColor: Union[QColor, Qt.GlobalColor] = None,
        overlayStyle: Material.OverlayStyle = Material.GrayOverlay,
        rippleColor: Union[QColor, Qt.GlobalColor] = None,
        overlayOpacity: float = 0.13,
        role: Material.Role = Material.Default,
        rippleStyle=Material.PositionedRipple,
        bgMode: Qt.BGMode = Qt.TransparentMode,
        **kwargs
    ):
        self.m_useThemeColors = useThemeColors
        self.m_baseOpacity = overlayOpacity

        self.m_role = role
        self.m_bgMode = bgMode
        self.m_rippleStyle = rippleStyle

        self.m_foregroundColor = QColor(foregroundColor)
        self.m_backgroundColor = QColor(backgroundColor)
        self.m_disabledForegroundColor = QColor(disabledForegroundColor)
        self.m_disabledBackgroundColor = QColor(disabledBackgroundColor)
        self.m_overlayColor = QColor(overlayColor)
        self.m_overlayStyle = overlayStyle

        self.m_rippleOverlay = QMaterialRippleOverlay(
            self, easingCurve=easingCurve, **kwargs
        )

        self.m_rippleColor: QColor = None
        self.setRippleColor(rippleColor)

    def rippleOverlay(self):
        return self.m_rippleOverlay

    def role(self) -> Material.Role:
        return self.m_role

    def setBackgroundMode(self, mode: Qt.BGMode) -> None:
        self.m_bgMode = mode
        self.m_stateMachine.setupProperties()

    def backgroundMode(self) -> Qt.BGMode:
        return self.m_bgMode

    def setRole(self, role: Material.Role) -> None:
        self.m_role = role

    def setEasingCurve(self, easingCurve: QEasingCurve = QEasingCurve.OutBounce):
        self.m_rippleOverlay.setEasingCurve(easingCurve)

    def setUseThemeColors(self, value: bool) -> None:
        if self.m_useThemeColors == value:
            return
        self.m_useThemeColors = value

    def useThemeColors(self) -> bool:
        return self.m_useThemeColors

    def setForegroundColor(self, color: Union[QColor, Qt.GlobalColor]) -> None:
        self.m_foregroundColor = QColor(color)

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.update()

    def foregroundColor(self) -> QColor:
        if (not self.m_foregroundColor.isValid()) and self.m_useThemeColors:
            materialStyle = QMaterialStyle()
            color = "text"  # role == Material.Default:...
            if Qt.OpaqueMode == self.m_bgMode:
                color = "canvas"

            if self.m_role == Material.Primary:
                color = "primary1"
            elif self.m_role == Material.Secondary:
                color = "accent1"

            return materialStyle.themeColor(color)

        return self.m_foregroundColor

    def setBackgroundColor(self, color: Union[QColor, Qt.GlobalColor]) -> None:
        self.m_backgroundColor = QColor(color)

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.update()

    def backgroundColor(self) -> QColor:
        if (not self.m_backgroundColor.isValid()) and self.m_useThemeColors:
            role = self.m_role
            materialStyle = QMaterialStyle()
            color = "text"  # role == Material.Default:

            if role == Material.Primary:
                color = "primary1"
            elif role == Material.Secondary:
                color = "accent1"
            return materialStyle.themeColor(color)

        return self.m_backgroundColor

    def setOverlayColor(self, color: Union[QColor, Qt.GlobalColor]) -> None:
        self.m_overlayColor = QColor(color)

        MATERIAL_DISABLE_THEME_COLORS(self)

        self.setOverlayStyle(Material.TintedOverlay)
        self.update()

    def overlayColor(self) -> QColor:
        return (
            self.m_overlayColor
            if self.m_overlayColor.isValid()
            else self.foregroundColor()
        )

    def setRippleColor(self, color: Union[QColor, Qt.GlobalColor]) -> None:
        self.m_rippleColor = QColor(color)
        self.m_rippleOverlay.setColor(self.rippleColor())

    def rippleColor(self) -> QColor:
        return (
            self.m_rippleColor
            if self.m_rippleColor.isValid()
            else self.foregroundColor()
        )

    def setDisabledForegroundColor(self, color: Union[QColor, Qt.GlobalColor]) -> None:
        self.m_disabledForegroundColor = QColor(color)

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.update()

    def disabledForegroundColor(self) -> QColor:
        if (not self.m_disabledColor.isValid()) and self.m_useThemeColors:
            return QMaterialStyle().themeColor("disabled")
        else:
            return self.m_disabledColor

    def setDisabledBackgroundColor(self, color: Union[QColor, Qt.GlobalColor]) -> None:
        self.m_disabledBackgroundColor = QColor(color)

        MATERIAL_DISABLE_THEME_COLORS(self)
        self.update()

    def disabledBackgroundColor(self) -> QColor:
        if (not self.m_disabledBackgroundColor.isValid()) and self.m_useThemeColors:
            return QMaterialStyle().themeColor("disabled3")
        else:
            return self.m_disabledBackgroundColor

    def setFontSize(self, size: float) -> None:
        self.m_fontSize = size

        f = QFont(self.font())
        f.setPointSizeF(size)
        self.setFont(f)

        self.update()

    def fontSize(self) -> float:
        return self.m_fontSize

    _foregroundColor = Property(QColor, fset=setForegroundColor, fget=foregroundColor)
    _backgroundColor = Property(QColor, fset=setBackgroundColor, fget=backgroundColor)
    _overlayColor = Property(QColor, fset=setOverlayColor, fget=overlayColor)
    _disabledForegroundColor = Property(
        QColor, fset=setDisabledForegroundColor, fget=disabledForegroundColor
    )
    _disabledBackgroundColor = Property(
        QColor, fset=setDisabledBackgroundColor, fget=disabledBackgroundColor
    )
    _fontSize = Property(float, fset=setFontSize, fget=fontSize)

    def setBaseOpacity(self, opacity: float) -> None:
        self.m_baseOpacity = opacity
        self.m_stateMachine.setupProperties()

    def baseOpacity(self) -> float:
        return self.m_baseOpacity

    def setHasFixedRippleRadius(self, value: bool) -> None:
        self.m_useFixedRippleRadius = value

    def hasFixedRippleRadius(self) -> bool:
        return self.m_useFixedRippleRadius

    def setFixedRippleRadius(self, radius: float) -> None:
        self.m_fixedRippleRadius = radius
        self.setHasFixedRippleRadius(True)

    def update(self):
        ...
