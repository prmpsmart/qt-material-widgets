from . import resources
from ._qt import *
from typing import Union

# dummy classes


class QtMaterialRippleOverlay:
    ...


class QtMaterialStyle:
    ...


class QtMaterialCheckable:
    ...


# dummy classes


def MATERIAL_DISABLE_THEME_COLORS(self):
    if self.d.useThemeColors == true:
        self.d.useThemeColors = false


class QtMaterialOverlayWidget(QWidget):
    def __init__(self, parent=void):
        QWidget.__init__(self, parent)
        if parent:
            parent.installEventFilter(self)

    def event(self, event: QEvent) -> bool:
        if not self.parent():
            return QWidget.event(self, event)

        e = event.type()
        if e == QEvent.ParentChange:
            self.parent().installEventFilter(self)
            self.setGeometry(self.overlayGeometry())

        elif e == QEvent.ParentAboutToChange:
            self.parent().removeEventFilter(self)

        return QWidget.event(self, event)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        e = event.type()
        if e in [QEvent.Move, QEvent.Resize]:
            self.setGeometry(self.overlayGeometry())

        return QWidget.eventFilter(self, obj, event)

    def overlayGeometry(self) -> QRect:
        widget: QWidget = self.parentWidget()
        if not widget:
            return QRect()
        return widget.rect()


class QtMaterialRipple(QParallelAnimationGroup):
    def __init__(
        self,
        center: QPoint,
        overlay: QtMaterialRippleOverlay = None,
        parent: QObject = None,
    ):
        QParallelAnimationGroup.__init__(self, parent)

        self.m_overlay = overlay
        self.m_radius = qreal(0)
        self.m_opacity = qreal(0)
        self.m_center = QPoint(center)
        self.m_brush = QBrush()

        self.m_radiusAnimation = self.animate(b"_radius")
        self.m_opacityAnimation = self.animate(b"_opacity")

        self.setOpacityStartValue(0.5)
        self.setOpacityEndValue(0)
        self.setRadiusStartValue(0)
        self.setRadiusEndValue(300)

        self.m_brush.setColor(Qt.black)
        self.m_brush.setStyle(Qt.SolidPattern)

        self.finished.connect(self.destroy)

    def setOverlay(self, overlay: QtMaterialRippleOverlay) -> void:
        self.m_overlay = overlay

    def setRadius(self, radius: qreal) -> void:
        if self.m_radius == radius:
            return
        self.m_radius = radius
        self.m_overlay.update()

    def radius(self) -> qreal:
        return self.m_radius

    def setOpacity(self, opacity: qreal) -> void:
        if self.m_opacity == opacity:
            return
        self.m_opacity = opacity
        self.m_overlay.update()

    def opacity(self) -> qreal:
        return self.m_opacity

    def setColor(self, color: QColor) -> void:
        if self.m_brush.color() == color:
            return
        self.m_brush.setColor(color)

        if self.m_overlay:
            self.m_overlay.update()

    def color(self) -> QColor:
        return self.m_brush.color()

    def setBrush(self, brush: QBrush) -> void:
        self.m_brush = brush

        if self.m_overlay:
            self.m_overlay.update()

    def brush(self) -> QBrush:
        return self.m_brush

    def center(self) -> QPoint:
        return self.m_center

    def radiusAnimation(self) -> QPropertyAnimation:
        return self.m_radiusAnimation

    def opacityAnimation(self) -> QPropertyAnimation:
        return self.m_opacityAnimation

    def setOpacityStartValue(self, value: qreal) -> void:
        self.m_opacityAnimation.setStartValue(value)

    def setOpacityEndValue(self, value: qreal) -> void:
        self.m_opacityAnimation.setEndValue(value)

    def setRadiusStartValue(self, value: qreal) -> void:
        self.m_radiusAnimation.setStartValue(value)

    def setRadiusEndValue(self, value: qreal) -> void:
        self.m_radiusAnimation.setEndValue(value)

    def setDuration(self, msecs: int) -> void:
        self.m_radiusAnimation.setDuration(msecs)
        self.m_opacityAnimation.setDuration(msecs)

    def destroy(self) -> void:
        self.m_overlay.removeRipple(self)

    def animate(
        self,
        property: bytes,
        easing: QEasingCurve = QEasingCurve.OutQuad,
        duration: int = 800,
    ) -> QPropertyAnimation:

        animation = QPropertyAnimation()
        animation.setTargetObject(self)
        animation.setPropertyName(property)
        animation.setEasingCurve(easing)
        animation.setDuration(duration)
        self.addAnimation(animation)
        return animation

    _radius = Q_PROPERTY(qreal, fset=setRadius, fget=radius)
    _opacity = Q_PROPERTY(qreal, fset=setOpacity, fget=opacity)


class QtMaterialRippleOverlay(QtMaterialOverlayWidget):
    def __init__(self, parent: QWidget = void):
        QtMaterialOverlayWidget.__init__(self, parent)

        self.m_ripples: List(QtMaterialRipple) = QList()
        self.m_clipPath = QPainterPath()
        self.m_useClip = bool(false)

        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)

    def addRipple(
        self,
        ripple: QtMaterialRipple = void,
        position: QPoint = void,
        radius: qreal = 300,
    ) -> void:

        if not ripple:
            ripple = QtMaterialRipple(center=position)
            ripple.setRadiusEndValue(radius)
            self.addRipple(ripple=ripple)

        ripple.setOverlay(self)
        self.m_ripples.push_back(ripple)
        ripple.start()

        m = 30
        if len(self.m_ripples) > m:
            self.m_ripples = QList(self.m_ripples[: (m // 2)])

        self.destroyed.connect(ripple.stop)
        self.destroyed.connect(ripple.deleteLater)

    def removeRipple(self, ripple: QtMaterialRipple) -> void:
        if self.m_ripples.removeOne(ripple):
            del self.ripple
            self.update()

    def setClipping(self, enable: bool) -> void:
        self.m_useClip = enable
        self.update()

    def hasClipping(self) -> bool:
        return self.m_useClip

    def setClipPath(self, path: QPainterPath) -> void:
        self.m_clipPath = path
        self.update()

    def paintEvent(self, event: QPaintEvent) -> void:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        if self.m_useClip:
            painter.setClipPath(self.m_clipPath)

        for i in self.m_ripples:
            self.paintRipple(painter, i)

    def ripples(self) -> List[QtMaterialRipple]:
        return self.m_ripples

    def paintRipple(self, painter: QPainter, ripple: QtMaterialRipple) -> void:
        radius: qreal = ripple.radius()
        center: QPointF = ripple.center()
        painter.setOpacity(ripple.opacity())
        painter.setBrush(ripple.brush())
        painter.drawEllipse(center, radius, radius)


class Material:
    class ButtonPreset(enum.Enum):
        FlatPreset = enum.auto()
        CheckablePreset = enum.auto()

    FlatPreset = ButtonPreset.FlatPreset
    CheckablePreset = ButtonPreset.CheckablePreset

    class RippleStyle(enum.Enum):
        CenteredRipple = enum.auto()
        PositionedRipple = enum.auto()
        NoRipple = enum.auto()

    CenteredRipple = RippleStyle.CenteredRipple
    PositionedRipple = RippleStyle.PositionedRipple
    NoRipple = RippleStyle.NoRipple

    class OverlayStyle(enum.Enum):
        NoOverlay = enum.auto()
        TintedOverlay = enum.auto()
        GrayOverlay = enum.auto()

    NoOverlay = OverlayStyle.NoOverlay
    TintedOverlay = OverlayStyle.TintedOverlay
    GrayOverlay = OverlayStyle.GrayOverlay

    class Role(enum.Enum):
        Default = enum.auto()
        Primary = enum.auto()
        Secondary = enum.auto()

    Default = Role.Default
    Primary = Role.Primary
    Secondary = Role.Secondary

    class ButtonIconPlacement(enum.Enum):
        LeftIcon = enum.auto()
        RightIcon = enum.auto()

    LeftIcon = ButtonIconPlacement.LeftIcon
    RightIcon = ButtonIconPlacement.RightIcon

    class ProgressType(enum.Enum):
        DeterminateProgress = enum.auto()
        IndeterminateProgress = enum.auto()

    DeterminateProgress = ProgressType.DeterminateProgress
    IndeterminateProgress = ProgressType.IndeterminateProgress

    class AvatarType(enum.Enum):
        ImageAvatar = enum.auto()
        IconAvatar = enum.auto()
        LetterAvatar = enum.auto()

    ImageAvatar = AvatarType.ImageAvatar
    IconAvatar = AvatarType.IconAvatar
    LetterAvatar = AvatarType.LetterAvatar

    class Color(enum.Enum):
        def _generate_next_value_(name, start, count, last_values):
            return count

        red50 = enum.auto()
        red100 = enum.auto()
        red200 = enum.auto()
        red300 = enum.auto()
        red400 = enum.auto()
        red500 = enum.auto()
        red600 = enum.auto()
        red700 = enum.auto()
        red800 = enum.auto()
        red900 = enum.auto()
        redA100 = enum.auto()
        redA200 = enum.auto()
        redA400 = enum.auto()
        redA700 = enum.auto()
        pink50 = enum.auto()
        pink100 = enum.auto()
        pink200 = enum.auto()
        pink300 = enum.auto()
        pink400 = enum.auto()
        pink500 = enum.auto()
        pink600 = enum.auto()
        pink700 = enum.auto()
        pink800 = enum.auto()
        pink900 = enum.auto()
        pinkA100 = enum.auto()
        pinkA200 = enum.auto()
        pinkA400 = enum.auto()
        pinkA700 = enum.auto()
        purple50 = enum.auto()
        purple100 = enum.auto()
        purple200 = enum.auto()
        purple300 = enum.auto()
        purple400 = enum.auto()
        purple500 = enum.auto()
        purple600 = enum.auto()
        purple700 = enum.auto()
        purple800 = enum.auto()
        purple900 = enum.auto()
        purpleA100 = enum.auto()
        purpleA200 = enum.auto()
        purpleA400 = enum.auto()
        purpleA700 = enum.auto()
        deepPurple50 = enum.auto()
        deepPurple100 = enum.auto()
        deepPurple200 = enum.auto()
        deepPurple300 = enum.auto()
        deepPurple400 = enum.auto()
        deepPurple500 = enum.auto()
        deepPurple600 = enum.auto()
        deepPurple700 = enum.auto()
        deepPurple800 = enum.auto()
        deepPurple900 = enum.auto()
        deepPurpleA100 = enum.auto()
        deepPurpleA200 = enum.auto()
        deepPurpleA400 = enum.auto()
        deepPurpleA700 = enum.auto()
        indigo50 = enum.auto()
        indigo100 = enum.auto()
        indigo200 = enum.auto()
        indigo300 = enum.auto()
        indigo400 = enum.auto()
        indigo500 = enum.auto()
        indigo600 = enum.auto()
        indigo700 = enum.auto()
        indigo800 = enum.auto()
        indigo900 = enum.auto()
        indigoA100 = enum.auto()
        indigoA200 = enum.auto()
        indigoA400 = enum.auto()
        indigoA700 = enum.auto()
        blue50 = enum.auto()
        blue100 = enum.auto()
        blue200 = enum.auto()
        blue300 = enum.auto()
        blue400 = enum.auto()
        blue500 = enum.auto()
        blue600 = enum.auto()
        blue700 = enum.auto()
        blue800 = enum.auto()
        blue900 = enum.auto()
        blueA100 = enum.auto()
        blueA200 = enum.auto()
        blueA400 = enum.auto()
        blueA700 = enum.auto()
        lightBlue50 = enum.auto()
        lightBlue100 = enum.auto()
        lightBlue200 = enum.auto()
        lightBlue300 = enum.auto()
        lightBlue400 = enum.auto()
        lightBlue500 = enum.auto()
        lightBlue600 = enum.auto()
        lightBlue700 = enum.auto()
        lightBlue800 = enum.auto()
        lightBlue900 = enum.auto()
        lightBlueA100 = enum.auto()
        lightBlueA200 = enum.auto()
        lightBlueA400 = enum.auto()
        lightBlueA700 = enum.auto()
        cyan50 = enum.auto()
        cyan100 = enum.auto()
        cyan200 = enum.auto()
        cyan300 = enum.auto()
        cyan400 = enum.auto()
        cyan500 = enum.auto()
        cyan600 = enum.auto()
        cyan700 = enum.auto()
        cyan800 = enum.auto()
        cyan900 = enum.auto()
        cyanA100 = enum.auto()
        cyanA200 = enum.auto()
        cyanA400 = enum.auto()
        cyanA700 = enum.auto()
        teal50 = enum.auto()
        teal100 = enum.auto()
        teal200 = enum.auto()
        teal300 = enum.auto()
        teal400 = enum.auto()
        teal500 = enum.auto()
        teal600 = enum.auto()
        teal700 = enum.auto()
        teal800 = enum.auto()
        teal900 = enum.auto()
        tealA100 = enum.auto()
        tealA200 = enum.auto()
        tealA400 = enum.auto()
        tealA700 = enum.auto()
        green50 = enum.auto()
        green100 = enum.auto()
        green200 = enum.auto()
        green300 = enum.auto()
        green400 = enum.auto()
        green500 = enum.auto()
        green600 = enum.auto()
        green700 = enum.auto()
        green800 = enum.auto()
        green900 = enum.auto()
        greenA100 = enum.auto()
        greenA200 = enum.auto()
        greenA400 = enum.auto()
        greenA700 = enum.auto()
        lightGreen50 = enum.auto()
        lightGreen100 = enum.auto()
        lightGreen200 = enum.auto()
        lightGreen300 = enum.auto()
        lightGreen400 = enum.auto()
        lightGreen500 = enum.auto()
        lightGreen600 = enum.auto()
        lightGreen700 = enum.auto()
        lightGreen800 = enum.auto()
        lightGreen900 = enum.auto()
        lightGreenA100 = enum.auto()
        lightGreenA200 = enum.auto()
        lightGreenA400 = enum.auto()
        lightGreenA700 = enum.auto()
        lime50 = enum.auto()
        lime100 = enum.auto()
        lime200 = enum.auto()
        lime300 = enum.auto()
        lime400 = enum.auto()
        lime500 = enum.auto()
        lime600 = enum.auto()
        lime700 = enum.auto()
        lime800 = enum.auto()
        lime900 = enum.auto()
        limeA100 = enum.auto()
        limeA200 = enum.auto()
        limeA400 = enum.auto()
        limeA700 = enum.auto()
        yellow50 = enum.auto()
        yellow100 = enum.auto()
        yellow200 = enum.auto()
        yellow300 = enum.auto()
        yellow400 = enum.auto()
        yellow500 = enum.auto()
        yellow600 = enum.auto()
        yellow700 = enum.auto()
        yellow800 = enum.auto()
        yellow900 = enum.auto()
        yellowA100 = enum.auto()
        yellowA200 = enum.auto()
        yellowA400 = enum.auto()
        yellowA700 = enum.auto()
        amber50 = enum.auto()
        amber100 = enum.auto()
        amber200 = enum.auto()
        amber300 = enum.auto()
        amber400 = enum.auto()
        amber500 = enum.auto()
        amber600 = enum.auto()
        amber700 = enum.auto()
        amber800 = enum.auto()
        amber900 = enum.auto()
        amberA100 = enum.auto()
        amberA200 = enum.auto()
        amberA400 = enum.auto()
        amberA700 = enum.auto()
        orange50 = enum.auto()
        orange100 = enum.auto()
        orange200 = enum.auto()
        orange300 = enum.auto()
        orange400 = enum.auto()
        orange500 = enum.auto()
        orange600 = enum.auto()
        orange700 = enum.auto()
        orange800 = enum.auto()
        orange900 = enum.auto()
        orangeA100 = enum.auto()
        orangeA200 = enum.auto()
        orangeA400 = enum.auto()
        orangeA700 = enum.auto()
        deepOrange50 = enum.auto()
        deepOrange100 = enum.auto()
        deepOrange200 = enum.auto()
        deepOrange300 = enum.auto()
        deepOrange400 = enum.auto()
        deepOrange500 = enum.auto()
        deepOrange600 = enum.auto()
        deepOrange700 = enum.auto()
        deepOrange800 = enum.auto()
        deepOrange900 = enum.auto()
        deepOrangeA100 = enum.auto()
        deepOrangeA200 = enum.auto()
        deepOrangeA400 = enum.auto()
        deepOrangeA700 = enum.auto()
        brown50 = enum.auto()
        brown100 = enum.auto()
        brown200 = enum.auto()
        brown300 = enum.auto()
        brown400 = enum.auto()
        brown500 = enum.auto()
        brown600 = enum.auto()
        brown700 = enum.auto()
        brown800 = enum.auto()
        brown900 = enum.auto()
        blueGrey50 = enum.auto()
        blueGrey100 = enum.auto()
        blueGrey200 = enum.auto()
        blueGrey300 = enum.auto()
        blueGrey400 = enum.auto()
        blueGrey500 = enum.auto()
        blueGrey600 = enum.auto()
        blueGrey700 = enum.auto()
        blueGrey800 = enum.auto()
        blueGrey900 = enum.auto()
        grey50 = enum.auto()
        grey100 = enum.auto()
        grey200 = enum.auto()
        grey300 = enum.auto()
        grey400 = enum.auto()
        grey500 = enum.auto()
        grey600 = enum.auto()
        grey700 = enum.auto()
        grey800 = enum.auto()
        grey900 = enum.auto()
        black = enum.auto()
        white = enum.auto()
        transparent = enum.auto()
        fullBlack = enum.auto()
        darkBlack = enum.auto()
        lightBlack = enum.auto()
        minBlack = enum.auto()
        faintBlack = enum.auto()
        fullWhite = enum.auto()
        darkWhite = enum.auto()
        lightWhite = enum.auto()

    red50 = Color.red50
    red100 = Color.red100
    red200 = Color.red200
    red300 = Color.red300
    red400 = Color.red400
    red500 = Color.red500
    red600 = Color.red600
    red700 = Color.red700
    red800 = Color.red800
    red900 = Color.red900
    redA100 = Color.redA100
    redA200 = Color.redA200
    redA400 = Color.redA400
    redA700 = Color.redA700
    pink50 = Color.pink50
    pink100 = Color.pink100
    pink200 = Color.pink200
    pink300 = Color.pink300
    pink400 = Color.pink400
    pink500 = Color.pink500
    pink600 = Color.pink600
    pink700 = Color.pink700
    pink800 = Color.pink800
    pink900 = Color.pink900
    pinkA100 = Color.pinkA100
    pinkA200 = Color.pinkA200
    pinkA400 = Color.pinkA400
    pinkA700 = Color.pinkA700
    purple50 = Color.purple50
    purple100 = Color.purple100
    purple200 = Color.purple200
    purple300 = Color.purple300
    purple400 = Color.purple400
    purple500 = Color.purple500
    purple600 = Color.purple600
    purple700 = Color.purple700
    purple800 = Color.purple800
    purple900 = Color.purple900
    purpleA100 = Color.purpleA100
    purpleA200 = Color.purpleA200
    purpleA400 = Color.purpleA400
    purpleA700 = Color.purpleA700
    deepPurple50 = Color.deepPurple50
    deepPurple100 = Color.deepPurple100
    deepPurple200 = Color.deepPurple200
    deepPurple300 = Color.deepPurple300
    deepPurple400 = Color.deepPurple400
    deepPurple500 = Color.deepPurple500
    deepPurple600 = Color.deepPurple600
    deepPurple700 = Color.deepPurple700
    deepPurple800 = Color.deepPurple800
    deepPurple900 = Color.deepPurple900
    deepPurpleA100 = Color.deepPurpleA100
    deepPurpleA200 = Color.deepPurpleA200
    deepPurpleA400 = Color.deepPurpleA400
    deepPurpleA700 = Color.deepPurpleA700
    indigo50 = Color.indigo50
    indigo100 = Color.indigo100
    indigo200 = Color.indigo200
    indigo300 = Color.indigo300
    indigo400 = Color.indigo400
    indigo500 = Color.indigo500
    indigo600 = Color.indigo600
    indigo700 = Color.indigo700
    indigo800 = Color.indigo800
    indigo900 = Color.indigo900
    indigoA100 = Color.indigoA100
    indigoA200 = Color.indigoA200
    indigoA400 = Color.indigoA400
    indigoA700 = Color.indigoA700
    blue50 = Color.blue50
    blue100 = Color.blue100
    blue200 = Color.blue200
    blue300 = Color.blue300
    blue400 = Color.blue400
    blue500 = Color.blue500
    blue600 = Color.blue600
    blue700 = Color.blue700
    blue800 = Color.blue800
    blue900 = Color.blue900
    blueA100 = Color.blueA100
    blueA200 = Color.blueA200
    blueA400 = Color.blueA400
    blueA700 = Color.blueA700
    lightBlue50 = Color.lightBlue50
    lightBlue100 = Color.lightBlue100
    lightBlue200 = Color.lightBlue200
    lightBlue300 = Color.lightBlue300
    lightBlue400 = Color.lightBlue400
    lightBlue500 = Color.lightBlue500
    lightBlue600 = Color.lightBlue600
    lightBlue700 = Color.lightBlue700
    lightBlue800 = Color.lightBlue800
    lightBlue900 = Color.lightBlue900
    lightBlueA100 = Color.lightBlueA100
    lightBlueA200 = Color.lightBlueA200
    lightBlueA400 = Color.lightBlueA400
    lightBlueA700 = Color.lightBlueA700
    cyan50 = Color.cyan50
    cyan100 = Color.cyan100
    cyan200 = Color.cyan200
    cyan300 = Color.cyan300
    cyan400 = Color.cyan400
    cyan500 = Color.cyan500
    cyan600 = Color.cyan600
    cyan700 = Color.cyan700
    cyan800 = Color.cyan800
    cyan900 = Color.cyan900
    cyanA100 = Color.cyanA100
    cyanA200 = Color.cyanA200
    cyanA400 = Color.cyanA400
    cyanA700 = Color.cyanA700
    teal50 = Color.teal50
    teal100 = Color.teal100
    teal200 = Color.teal200
    teal300 = Color.teal300
    teal400 = Color.teal400
    teal500 = Color.teal500
    teal600 = Color.teal600
    teal700 = Color.teal700
    teal800 = Color.teal800
    teal900 = Color.teal900
    tealA100 = Color.tealA100
    tealA200 = Color.tealA200
    tealA400 = Color.tealA400
    tealA700 = Color.tealA700
    green50 = Color.green50
    green100 = Color.green100
    green200 = Color.green200
    green300 = Color.green300
    green400 = Color.green400
    green500 = Color.green500
    green600 = Color.green600
    green700 = Color.green700
    green800 = Color.green800
    green900 = Color.green900
    greenA100 = Color.greenA100
    greenA200 = Color.greenA200
    greenA400 = Color.greenA400
    greenA700 = Color.greenA700
    lightGreen50 = Color.lightGreen50
    lightGreen100 = Color.lightGreen100
    lightGreen200 = Color.lightGreen200
    lightGreen300 = Color.lightGreen300
    lightGreen400 = Color.lightGreen400
    lightGreen500 = Color.lightGreen500
    lightGreen600 = Color.lightGreen600
    lightGreen700 = Color.lightGreen700
    lightGreen800 = Color.lightGreen800
    lightGreen900 = Color.lightGreen900
    lightGreenA100 = Color.lightGreenA100
    lightGreenA200 = Color.lightGreenA200
    lightGreenA400 = Color.lightGreenA400
    lightGreenA700 = Color.lightGreenA700
    lime50 = Color.lime50
    lime100 = Color.lime100
    lime200 = Color.lime200
    lime300 = Color.lime300
    lime400 = Color.lime400
    lime500 = Color.lime500
    lime600 = Color.lime600
    lime700 = Color.lime700
    lime800 = Color.lime800
    lime900 = Color.lime900
    limeA100 = Color.limeA100
    limeA200 = Color.limeA200
    limeA400 = Color.limeA400
    limeA700 = Color.limeA700
    yellow50 = Color.yellow50
    yellow100 = Color.yellow100
    yellow200 = Color.yellow200
    yellow300 = Color.yellow300
    yellow400 = Color.yellow400
    yellow500 = Color.yellow500
    yellow600 = Color.yellow600
    yellow700 = Color.yellow700
    yellow800 = Color.yellow800
    yellow900 = Color.yellow900
    yellowA100 = Color.yellowA100
    yellowA200 = Color.yellowA200
    yellowA400 = Color.yellowA400
    yellowA700 = Color.yellowA700
    amber50 = Color.amber50
    amber100 = Color.amber100
    amber200 = Color.amber200
    amber300 = Color.amber300
    amber400 = Color.amber400
    amber500 = Color.amber500
    amber600 = Color.amber600
    amber700 = Color.amber700
    amber800 = Color.amber800
    amber900 = Color.amber900
    amberA100 = Color.amberA100
    amberA200 = Color.amberA200
    amberA400 = Color.amberA400
    amberA700 = Color.amberA700
    orange50 = Color.orange50
    orange100 = Color.orange100
    orange200 = Color.orange200
    orange300 = Color.orange300
    orange400 = Color.orange400
    orange500 = Color.orange500
    orange600 = Color.orange600
    orange700 = Color.orange700
    orange800 = Color.orange800
    orange900 = Color.orange900
    orangeA100 = Color.orangeA100
    orangeA200 = Color.orangeA200
    orangeA400 = Color.orangeA400
    orangeA700 = Color.orangeA700
    deepOrange50 = Color.deepOrange50
    deepOrange100 = Color.deepOrange100
    deepOrange200 = Color.deepOrange200
    deepOrange300 = Color.deepOrange300
    deepOrange400 = Color.deepOrange400
    deepOrange500 = Color.deepOrange500
    deepOrange600 = Color.deepOrange600
    deepOrange700 = Color.deepOrange700
    deepOrange800 = Color.deepOrange800
    deepOrange900 = Color.deepOrange900
    deepOrangeA100 = Color.deepOrangeA100
    deepOrangeA200 = Color.deepOrangeA200
    deepOrangeA400 = Color.deepOrangeA400
    deepOrangeA700 = Color.deepOrangeA700
    brown50 = Color.brown50
    brown100 = Color.brown100
    brown200 = Color.brown200
    brown300 = Color.brown300
    brown400 = Color.brown400
    brown500 = Color.brown500
    brown600 = Color.brown600
    brown700 = Color.brown700
    brown800 = Color.brown800
    brown900 = Color.brown900
    blueGrey50 = Color.blueGrey50
    blueGrey100 = Color.blueGrey100
    blueGrey200 = Color.blueGrey200
    blueGrey300 = Color.blueGrey300
    blueGrey400 = Color.blueGrey400
    blueGrey500 = Color.blueGrey500
    blueGrey600 = Color.blueGrey600
    blueGrey700 = Color.blueGrey700
    blueGrey800 = Color.blueGrey800
    blueGrey900 = Color.blueGrey900
    grey50 = Color.grey50
    grey100 = Color.grey100
    grey200 = Color.grey200
    grey300 = Color.grey300
    grey400 = Color.grey400
    grey500 = Color.grey500
    grey600 = Color.grey600
    grey700 = Color.grey700
    grey800 = Color.grey800
    grey900 = Color.grey900
    black = Color.black
    white = Color.white
    transparent = Color.transparent
    fullBlack = Color.fullBlack
    darkBlack = Color.darkBlack
    lightBlack = Color.lightBlack
    minBlack = Color.minBlack
    faintBlack = Color.faintBlack
    fullWhite = Color.fullWhite
    darkWhite = Color.darkWhite
    lightWhite = Color.lightWhite


class QtMaterialTheme(QObject):
    palette = [
        QColor("#ffebee"),
        QColor("#ffcdd2"),
        QColor("#ef9a9a"),
        QColor("#e57373"),
        QColor("#ef5350"),
        QColor("#f44336"),
        QColor("#e53935"),
        QColor("#d32f2f"),
        QColor("#c62828"),
        QColor("#b71c1c"),
        QColor("#ff8a80"),
        QColor("#ff5252"),
        QColor("#ff1744"),
        QColor("#d50000"),
        QColor("#fce4ec"),
        QColor("#f8bbd0"),
        QColor("#f48fb1"),
        QColor("#f06292"),
        QColor("#ec407a"),
        QColor("#e91e63"),
        QColor("#d81b60"),
        QColor("#c2185b"),
        QColor("#ad1457"),
        QColor("#880e4f"),
        QColor("#ff80ab"),
        QColor("#ff4081"),
        QColor("#f50057"),
        QColor("#c51162"),
        QColor("#f3e5f5"),
        QColor("#e1bee7"),
        QColor("#ce93d8"),
        QColor("#ba68c8"),
        QColor("#ab47bc"),
        QColor("#9c27b0"),
        QColor("#8e24aa"),
        QColor("#7b1fa2"),
        QColor("#6a1b9a"),
        QColor("#4a148c"),
        QColor("#ea80fc"),
        QColor("#e040fb"),
        QColor("#d500f9"),
        QColor("#aa00ff"),
        QColor("#ede7f6"),
        QColor("#d1c4e9"),
        QColor("#b39ddb"),
        QColor("#9575cd"),
        QColor("#7e57c2"),
        QColor("#673ab7"),
        QColor("#5e35b1"),
        QColor("#512da8"),
        QColor("#4527a0"),
        QColor("#311b92"),
        QColor("#b388ff"),
        QColor("#7c4dff"),
        QColor("#651fff"),
        QColor("#6200ea"),
        QColor("#e8eaf6"),
        QColor("#c5cae9"),
        QColor("#9fa8da"),
        QColor("#7986cb"),
        QColor("#5c6bc0"),
        QColor("#3f51b5"),
        QColor("#3949ab"),
        QColor("#303f9f"),
        QColor("#283593"),
        QColor("#1a237e"),
        QColor("#8c9eff"),
        QColor("#536dfe"),
        QColor("#3d5afe"),
        QColor("#304ffe"),
        QColor("#e3f2fd"),
        QColor("#bbdefb"),
        QColor("#90caf9"),
        QColor("#64b5f6"),
        QColor("#42a5f5"),
        QColor("#2196f3"),
        QColor("#1e88e5"),
        QColor("#1976d2"),
        QColor("#1565c0"),
        QColor("#0d47a1"),
        QColor("#82b1ff"),
        QColor("#448aff"),
        QColor("#2979ff"),
        QColor("#2962ff"),
        QColor("#e1f5fe"),
        QColor("#b3e5fc"),
        QColor("#81d4fa"),
        QColor("#4fc3f7"),
        QColor("#29b6f6"),
        QColor("#03a9f4"),
        QColor("#039be5"),
        QColor("#0288d1"),
        QColor("#0277bd"),
        QColor("#01579b"),
        QColor("#80d8ff"),
        QColor("#40c4ff"),
        QColor("#00b0ff"),
        QColor("#0091ea"),
        QColor("#e0f7fa"),
        QColor("#b2ebf2"),
        QColor("#80deea"),
        QColor("#4dd0e1"),
        QColor("#26c6da"),
        QColor("#00bcd4"),
        QColor("#00acc1"),
        QColor("#0097a7"),
        QColor("#00838f"),
        QColor("#006064"),
        QColor("#84ffff"),
        QColor("#18ffff"),
        QColor("#00e5ff"),
        QColor("#00b8d4"),
        QColor("#e0f2f1"),
        QColor("#b2dfdb"),
        QColor("#80cbc4"),
        QColor("#4db6ac"),
        QColor("#26a69a"),
        QColor("#009688"),
        QColor("#00897b"),
        QColor("#00796b"),
        QColor("#00695c"),
        QColor("#004d40"),
        QColor("#a7ffeb"),
        QColor("#64ffda"),
        QColor("#1de9b6"),
        QColor("#00bfa5"),
        QColor("#e8f5e9"),
        QColor("#c8e6c9"),
        QColor("#a5d6a7"),
        QColor("#81c784"),
        QColor("#66bb6a"),
        QColor("#4caf50"),
        QColor("#43a047"),
        QColor("#388e3c"),
        QColor("#2e7d32"),
        QColor("#1b5e20"),
        QColor("#b9f6ca"),
        QColor("#69f0ae"),
        QColor("#00e676"),
        QColor("#00c853"),
        QColor("#f1f8e9"),
        QColor("#dcedc8"),
        QColor("#c5e1a5"),
        QColor("#aed581"),
        QColor("#9ccc65"),
        QColor("#8bc34a"),
        QColor("#7cb342"),
        QColor("#689f38"),
        QColor("#558b2f"),
        QColor("#33691e"),
        QColor("#ccff90"),
        QColor("#b2ff59"),
        QColor("#76ff03"),
        QColor("#64dd17"),
        QColor("#f9fbe7"),
        QColor("#f0f4c3"),
        QColor("#e6ee9c"),
        QColor("#dce775"),
        QColor("#d4e157"),
        QColor("#cddc39"),
        QColor("#c0ca33"),
        QColor("#afb42b"),
        QColor("#9e9d24"),
        QColor("#827717"),
        QColor("#f4ff81"),
        QColor("#eeff41"),
        QColor("#c6ff00"),
        QColor("#aeea00"),
        QColor("#fffde7"),
        QColor("#fff9c4"),
        QColor("#fff59d"),
        QColor("#fff176"),
        QColor("#ffee58"),
        QColor("#ffeb3b"),
        QColor("#fdd835"),
        QColor("#fbc02d"),
        QColor("#f9a825"),
        QColor("#f57f17"),
        QColor("#ffff8d"),
        QColor("#ffff00"),
        QColor("#ffea00"),
        QColor("#ffd600"),
        QColor("#fff8e1"),
        QColor("#ffecb3"),
        QColor("#ffe082"),
        QColor("#ffd54f"),
        QColor("#ffca28"),
        QColor("#ffc107"),
        QColor("#ffb300"),
        QColor("#ffa000"),
        QColor("#ff8f00"),
        QColor("#ff6f00"),
        QColor("#ffe57f"),
        QColor("#ffd740"),
        QColor("#ffc400"),
        QColor("#ffab00"),
        QColor("#fff3e0"),
        QColor("#ffe0b2"),
        QColor("#ffcc80"),
        QColor("#ffb74d"),
        QColor("#ffa726"),
        QColor("#ff9800"),
        QColor("#fb8c00"),
        QColor("#f57c00"),
        QColor("#ef6c00"),
        QColor("#e65100"),
        QColor("#ffd180"),
        QColor("#ffab40"),
        QColor("#ff9100"),
        QColor("#ff6d00"),
        QColor("#fbe9e7"),
        QColor("#ffccbc"),
        QColor("#ffab91"),
        QColor("#ff8a65"),
        QColor("#ff7043"),
        QColor("#ff5722"),
        QColor("#f4511e"),
        QColor("#e64a19"),
        QColor("#d84315"),
        QColor("#bf360c"),
        QColor("#ff9e80"),
        QColor("#ff6e40"),
        QColor("#ff3d00"),
        QColor("#dd2c00"),
        QColor("#efebe9"),
        QColor("#d7ccc8"),
        QColor("#bcaaa4"),
        QColor("#a1887f"),
        QColor("#8d6e63"),
        QColor("#795548"),
        QColor("#6d4c41"),
        QColor("#5d4037"),
        QColor("#4e342e"),
        QColor("#3e2723"),
        QColor("#eceff1"),
        QColor("#cfd8dc"),
        QColor("#b0bec5"),
        QColor("#90a4ae"),
        QColor("#78909c"),
        QColor("#607d8b"),
        QColor("#546e7a"),
        QColor("#455a64"),
        QColor("#37474f"),
        QColor("#263238"),
        QColor("#fafafa"),
        QColor("#f5f5f5"),
        QColor("#eeeeee"),
        QColor("#e0e0e0"),
        QColor("#bdbdbd"),
        QColor("#9e9e9e"),
        QColor("#757575"),
        QColor("#616161"),
        QColor("#424242"),
        QColor("#212121"),
        QColor("#000000"),
        QColor("#ffffff"),
    ]

    added_new = False

    def __init__(self, parent: QObject = void) -> void:
        QObject.__init__(self, parent=parent)
        self.d = QtMaterialThemePrivate(self)

        if not QtMaterialTheme.added_new:
            QtMaterialTheme.palette.extend(
                [
                    self.d.rgba(0, 0, 0, 0),
                    self.d.rgba(0, 0, 0, 1),
                    self.d.rgba(0, 0, 0, 0.87),
                    self.d.rgba(0, 0, 0, 0.54),
                    self.d.rgba(0, 0, 0, 0.26),
                    self.d.rgba(0, 0, 0, 0.12),
                    self.d.rgba(255, 255, 255, 1),
                    self.d.rgba(255, 255, 255, 0.87),
                    self.d.rgba(255, 255, 255, 0.54),
                ]
            )
            QtMaterialTheme.added_new = True

        self.setColor("primary1", Material.cyan500)
        self.setColor("primary2", Material.cyan700)
        self.setColor("primary3", Material.lightBlack)
        self.setColor("accent1", Material.pinkA200)
        self.setColor("accent2", Material.grey100)
        self.setColor("accent3", Material.grey500)
        self.setColor("text", Material.darkBlack)
        self.setColor("alternateText", Material.white)
        self.setColor("canvas", Material.white)
        self.setColor("border", Material.grey300)
        self.setColor("disabled", Material.minBlack)
        self.setColor("disabled2", Material.faintBlack)
        self.setColor("disabled3", Material.grey300)

    def getColor(self, key: QString) -> QColor:
        if not key in self.d.colors:
            print("A theme color matching the key '", key, "' could not be found.")
            return QColor()
        return self.d.colors.get(key)

    def setColor(self, key: QString, color: Union[QColor, Material.Color]) -> void:
        if isinstance(color, QColor): _c = color
        else: _c = self.palette[color.value]
        self.d.colors[key] = _c

    @staticmethod
    def icon(category: QString, icon: QString) -> QIcon:
        return QIcon(f":/{category}/ic_{icon}_24px.svg")


class QtMaterialThemePrivate:
    def __init__(self, q: QtMaterialTheme) -> void:
        self.q: QtMaterialTheme = q
        self.colors: Dict[QString, QColor] = {}

    def rgba(self, r: int, g: int, b: int, a: qreal) -> QColor:
        color = QColor(r, g, b)
        color.setAlphaF(a)
        return color


class QtMaterialStylePrivate:
    def __init__(self, q: QtMaterialStyle):
        self.q: QtMaterialStyle = q
        self.theme = QtMaterialTheme()

    def init(self) -> void:
        QFontDatabase.addApplicationFont(":/fonts/roboto_regular")
        QFontDatabase.addApplicationFont(":/fonts/roboto_medium")
        QFontDatabase.addApplicationFont(":/fonts/roboto_bold")

        self.q.setTheme(QtMaterialTheme())


class QtMaterialStyle(QCommonStyle):
    def __init__(self):
        QCommonStyle.__init__(self)
        self.d = QtMaterialStylePrivate(self)
        self.d.init()

    @staticmethod
    def instance() -> QtMaterialStyle:
        instance = QtMaterialStyle()
        return instance

    def setTheme(self, theme: QtMaterialTheme) -> void:
        self.d.theme = theme
        theme.setParent(self)

    def themeColor(self, key: QString) -> QColor:
        return self.d.theme.getColor(key)

    def __eq__(self, q) -> void:
        ...


class QtMaterialStateTransitionType(enum.Enum):
    # Snackbar
    SnackbarShowTransition = 1
    SnackbarHideTransition = enum.auto()
    SnackbarWaitTransition = enum.auto()
    SnackbarNextTransition = enum.auto()
    # FlatButton
    FlatButtonPressedTransition = enum.auto()
    FlatButtonCheckedTransition = enum.auto()
    FlatButtonUncheckedTransition = enum.auto()
    # CollapsibleMenu
    CollapsibleMenuExpand = enum.auto()
    CollapsibleMenuCollapse = enum.auto()
    # Slider
    SliderChangedToMinimum = enum.auto()
    SliderChangedFromMinimum = enum.auto()
    SliderNoFocusMouseEnter = enum.auto()
    SliderNoFocusMouseLeave = enum.auto()
    # Dialog
    DialogShowTransition = enum.auto()
    DialogHideTransition = enum.auto()
    #
    MaxTransitionType = 65535


class QtMaterialStateTransitionEvent(QEvent):

    SnackbarShowTransition = QtMaterialStateTransitionType.SnackbarShowTransition
    SnackbarHideTransition = QtMaterialStateTransitionType.SnackbarHideTransition
    SnackbarWaitTransition = QtMaterialStateTransitionType.SnackbarWaitTransition
    SnackbarNextTransition = QtMaterialStateTransitionType.SnackbarNextTransition
    FlatButtonPressedTransition = (
        QtMaterialStateTransitionType.FlatButtonPressedTransition
    )
    FlatButtonCheckedTransition = (
        QtMaterialStateTransitionType.FlatButtonCheckedTransition
    )
    FlatButtonUncheckedTransition = (
        QtMaterialStateTransitionType.FlatButtonUncheckedTransition
    )
    CollapsibleMenuExpand = QtMaterialStateTransitionType.CollapsibleMenuExpand
    CollapsibleMenuCollapse = QtMaterialStateTransitionType.CollapsibleMenuCollapse
    SliderChangedToMinimum = QtMaterialStateTransitionType.SliderChangedToMinimum
    SliderChangedFromMinimum = QtMaterialStateTransitionType.SliderChangedFromMinimum
    SliderNoFocusMouseEnter = QtMaterialStateTransitionType.SliderNoFocusMouseEnter
    SliderNoFocusMouseLeave = QtMaterialStateTransitionType.SliderNoFocusMouseLeave
    DialogShowTransition = QtMaterialStateTransitionType.DialogShowTransition
    DialogHideTransition = QtMaterialStateTransitionType.DialogHideTransition
    MaxTransitionType = QtMaterialStateTransitionType.MaxTransitionType

    def __init__(self, type: QtMaterialStateTransitionType) -> void:
        QEvent.__init__(self, QEvent.Type(QEvent.User + 1))

    def type(self) -> QtMaterialStateTransitionType:
        return QEvent.type(self)


class QtMaterialStateTransition(QAbstractTransition):
    def __init__(self, type: QtMaterialStateTransitionType):
        QAbstractTransition.__init__(self)
        self.m_type = QtMaterialStateTransitionType(type)

    def eventTest(self, event: QEvent) -> bool:
        if event.type() != QEvent.Type(QEvent.User + 1):
            return false

        transition = QtMaterialStateTransitionEvent(event)
        return self.m_type == transition.type()

    def onTransition(self, event: QEvent) -> void:
        ...


class QtMaterialCheckablePrivate:
    def __init__(self, q: QtMaterialCheckable) -> void:
        self.q: QtMaterialCheckable = q
        self.rippleOverlay: QtMaterialRippleOverlay = None
        self.checkedIcon: QtMaterialCheckableIcon = None
        self.uncheckedIcon: QtMaterialCheckableIcon = None
        self.stateMachine: QStateMachine = None
        self.uncheckedState: QState = None
        self.checkedState: QState = None
        self.disabledUncheckedState: QState = None
        self.disabledCheckedState: QState = None
        self.uncheckedTransition: QSignalTransition = None
        self.checkedTransition: QSignalTransition = None
        self.labelPosition: QtMaterialCheckable.LabelPosition = None

        self.checkedColor: QColor = None
        self.uncheckedColor: QColor = None
        self.textColor: QColor = None
        self.disabledColor: QColor = None
        self.useThemeColors: bool = None

    def init(self) -> void:

        q = self.q

        self.rippleOverlay = QtMaterialRippleOverlay()
        self.checkedIcon = QtMaterialCheckableIcon(
            QIcon(":toggle/ic_check_box_24px.svg"), q
        )
        self.uncheckedIcon = QtMaterialCheckableIcon(
            QIcon(":toggle/ic_check_box_outline_blank_24px.svg"), q
        )
        self.stateMachine = QStateMachine(q)
        self.uncheckedState = QState()
        self.checkedState = QState()
        self.disabledUncheckedState = QState()
        self.disabledCheckedState = QState()
        self.uncheckedTransition = QSignalTransition(q.toggled)
        self.checkedTransition = QSignalTransition(q.toggled)
        self.labelPosition = QtMaterialCheckable.LabelPositionRight
        self.useThemeColors = true

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

        # // Transition to checked

        self.uncheckedTransition.setTargetState(self.checkedState)
        self.uncheckedState.addTransition(self.uncheckedTransition)

        # // Transition to unchecked

        self.checkedTransition.setTargetState(self.uncheckedState)
        self.checkedState.addTransition(self.checkedTransition)

        # // Transitions enabled <==> disabled

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

        transition = QSignalTransition(q.toggled)
        transition.setTargetState(self.disabledCheckedState)
        self.disabledUncheckedState.addTransition(transition)

        transition = QSignalTransition(q.toggled)
        transition.setTargetState(self.disabledUncheckedState)
        self.disabledCheckedState.addTransition(transition)

        # //

        self.checkedState.assignProperty(self.checkedIcon, "_opacity", 1)
        self.checkedState.assignProperty(self.uncheckedIcon, "_opacity", 0)

        self.uncheckedState.assignProperty(self.checkedIcon, "_opacity", 0)
        self.uncheckedState.assignProperty(self.uncheckedIcon, "_opacity", 1)

        self.disabledCheckedState.assignProperty(self.checkedIcon, "_opacity", 1)
        self.disabledCheckedState.assignProperty(self.uncheckedIcon, "_opacity", 0)

        self.disabledUncheckedState.assignProperty(self.checkedIcon, "_opacity", 0)
        self.disabledUncheckedState.assignProperty(self.uncheckedIcon, "_opacity", 1)

        self.checkedState.assignProperty(self.checkedIcon, "_color", q.checkedColor())
        self.checkedState.assignProperty(self.uncheckedIcon, "_color", q.checkedColor())

        self.uncheckedState.assignProperty(
            self.uncheckedIcon, "_color", q.uncheckedColor()
        )
        self.uncheckedState.assignProperty(
            self.uncheckedIcon, "_color", q.uncheckedColor()
        )

        self.disabledUncheckedState.assignProperty(
            self.uncheckedIcon, "_color", q.disabledColor()
        )
        self.disabledCheckedState.assignProperty(
            self.checkedIcon, "_color", q.disabledColor()
        )

        self.stateMachine.start()
        QCoreApplication.processEvents()


class QtMaterialCheckable(QAbstractButton):
    toggled = Signal(bool)

    class LabelPosition(enum.Enum):
        LabelPositionLeft = enum.auto()
        LabelPositionRight = enum.auto()

    LabelPositionLeft = LabelPosition.LabelPositionLeft
    LabelPositionRight = LabelPosition.LabelPositionRight

    def __init__(self, d: QtMaterialCheckablePrivate = None, parent: QWidget = void):
        QAbstractButton.__init__(self, parent)

        self.d = QtMaterialCheckablePrivate(self)
        self.d.init()

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
        MATERIAL_DISABLE_THEME_COLORS(self)
        self.setupProperties()

    def checkedColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.checkedColor.isValid():
            return QtMaterialStyle.instance().themeColor("primary1")
        else:
            return self.d.checkedColor

    def setUncheckedColor(self, color: QColor) -> void:
        self.d.uncheckedColor = color
        MATERIAL_DISABLE_THEME_COLORS(self)
        self.setupProperties()

    def uncheckedColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.uncheckedColor.isValid():
            return QtMaterialStyle.instance().themeColor("text")
        else:
            return self.d.uncheckedColor

    def setTextColor(self, color: QColor) -> void:
        self.d.textColor = color
        MATERIAL_DISABLE_THEME_COLORS(self)
        self.setupProperties()

    def textColor(self) -> QColor:
        if self.d.useThemeColors or not self.d.textColor.isValid():
            return QtMaterialStyle.instance().themeColor("text")
        else:
            return self.d.textColor

    def setDisabledColor(self, color: QColor) -> void:
        self.d.disabledColor = color
        MATERIAL_DISABLE_THEME_COLORS(self)
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
        if self.text():
            return QSize(40, 40)

        return QSize(
            self.fontMetrics().size(Qt.TextShowMnemonic, self.text()).width() + 52, 40
        )

    def event(self, event: QEvent) -> bool:
        e = event.type()
        if e in [QEvent.Resize, QEvent.Move]:
            self.d.checkedIcon.setGeometry(self.rect())
            self.d.uncheckedIcon.setGeometry(self.rect())
            self.d.rippleOverlay.setGeometry(self.geometry().adjusted(-8, -8, 8, 8))

        elif e == QEvent.ParentChange:
            widget = QWidget()
            if widget == self.parentWidget():
                self.d.rippleOverlay.setParent(widget)

        return QAbstractButton.event(self, event)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if QEvent.Resize == event.type():
            self.d.rippleOverlay.setGeometry(self.geometry().adjusted(-8, -8, 8, 8))
        return QAbstractButton.eventFilter(self, obj, event)

    def mousePressEvent(self, event: QMouseEvent) -> void:
        if not self.isEnabled():
            return

        ripple = QtMaterialRipple()
        if QtMaterialCheckable.LabelPositionLeft == self.d.labelPosition:
            ripple = QtMaterialRipple(QPoint(self.width() - 14, 28))
        else:
            ripple = QtMaterialRipple(QPoint(28, 28))

        ripple.setRadiusEndValue(22)
        ripple.setColor(
            self.checkedColor() if self.isChecked() else self.uncheckedColor()
        )
        if self.isChecked():
            ripple.setOpacityStartValue(1)

        self.d.rippleOverlay.addRipple(ripple)

        self.setChecked(not self.isChecked())

    def paintEvent(self, event: QPaintEvent) -> void:
        painter = QPainter(self)

        pen = QPen()
        pen.setColor(self.textColor() if self.isEnabled() else self.disabledColor())
        painter.setPen(pen)

        if QtMaterialCheckable.LabelPositionLeft == self.d.labelPosition:
            painter.drawText(4, 25, self.text())
        else:
            painter.drawText(48, 25, self.text())

    def setupProperties(self) -> void:
        self.d.checkedState.assignProperty(
            self.d.checkedIcon, "color", self.checkedColor()
        )
        self.d.checkedState.assignProperty(
            self.d.uncheckedIcon, "color", self.checkedColor()
        )
        self.d.uncheckedState.assignProperty(
            self.d.uncheckedIcon, "color", self.uncheckedColor()
        )
        self.d.disabledUncheckedState.assignProperty(
            self.d.uncheckedIcon, "color", self.disabledColor()
        )
        self.d.disabledCheckedState.assignProperty(
            self.d.checkedIcon, "color", self.disabledColor()
        )

        if self.isEnabled():
            if self.isChecked():
                self.d.checkedIcon.setColor(self.checkedColor())
            else:
                self.d.uncheckedIcon.setColor(self.uncheckedColor())

        else:
            self.d.checkedIcon.setColor(self.disabledColor())
            self.d.uncheckedIcon.setColor(self.disabledColor())

        self.update()


class QtMaterialCheckableIcon(QWidget):
    def __init__(self, icon: QIcon = None, parent: QtMaterialCheckable = None) -> void:
        QWidget.__init__(self, parent)

        self.m_checkable = parent
        self.m_color = QColor(Qt.black)
        self.m_icon = QIcon(icon)
        self.m_iconSize = qreal(24)
        self.m_opacity = qreal(1.0)

        assert parent
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def setIcon(self, icon: QIcon) -> void:
        self.m_icon = icon
        self.update()

    def icon(self) -> QIcon:
        return self.m_icon

    def setColor(self, color: QColor) -> void:
        self.m_color = color
        self.update()

    def color(self) -> QColor:
        return self.m_color

    def setIconSize(self, size: qreal) -> void:
        self.m_iconSize = size
        self.update()

    def iconSize(self) -> qreal:
        return self.m_iconSize

    def setOpacity(self, opacity: qreal) -> void:
        self.m_opacity = opacity
        self.update()

    def opacity(self) -> qreal:
        return self.m_opacity

    def sizeHint(self) -> QSize:
        return QSize(self.m_iconSize, self.m_iconSize)

    def paintEvent(self, event: QPaintEvent) -> void:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setOpacity(self.m_opacity)

        pixmap: QPixmap = self.icon().pixmap(24, 24)

        if not pixmap.isNull():
            p: qreal = ((self.height()) - self.m_iconSize) / 2
            z: qreal = self.m_iconSize / 24

            t = QTransform()
            if (
                QtMaterialCheckable.LabelPositionLeft
                == self.m_checkable.labelPosition()
            ):
                t.translate(p + self.width() - 42, p)
            else:
                t.translate(p, p)

            t.scale(z, z)
            painter.setTransform(t)

            icon = QPainter(pixmap)
            icon.setCompositionMode(QPainter.CompositionMode_SourceIn)
            icon.fillRect(pixmap.rect(), self.color())
            painter.drawPixmap(0, 0, pixmap)

        painter.end()

    _color = Q_PROPERTY(QColor, fget=color, fset=setColor)
    _iconSize = Q_PROPERTY(qreal, fget=iconSize, fset=setIconSize)
    _opacity = Q_PROPERTY(qreal, fget=opacity, fset=setOpacity)
