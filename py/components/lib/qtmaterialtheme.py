from typing import List
from PySide6.QtGui import QColor, QIcon
from PySide6.QtCore import QObject
from enum import Enum

QString = str
void = None


class Material:
    class ButtonPreset(Enum):
        FlatPreset = "FlatPreset"
        CheckablePreset = "CheckablePreset"

    class RippleStyle(Enum):
        CenteredRipple = "CenteredRipple"
        PositionedRipple = "PositionedRipple"
        NoRipple = "NoRipple"

    class OverlayStyle(Enum):
        NoOverlay = "NoOverlay"
        TintedOverlay = "TintedOverlay"
        GrayOverlay = "GrayOverlay"

    class Role(Enum):
        Default = "Default"
        Primary = "Primary"
        Secondary = "Secondary"

    class ButtonIconPlacement(Enum):
        LeftIcon = "LeftIcon"
        RightIcon = "RightIcon"

    class ProgressType(Enum):
        DeterminateProgress = "DeterminateProgress"
        IndeterminateProgress = "IndeterminateProgress"

    class AvatarType(Enum):
        ImageAvatar = "ImageAvatar"
        IconAvatar = "IconAvatar"
        LetterAvatar = "LetterAvatar"

    class Color(Enum):
        red50 = "red50"
        red100 = "red100"
        red200 = "red200"
        red300 = "red300"
        red400 = "red400"
        red500 = "red500"
        red600 = "red600"
        red700 = "red700"
        red800 = "red800"
        red900 = "red900"
        redA100 = "redA100"
        redA200 = "redA200"
        redA400 = "redA400"
        redA700 = "redA700"
        pink50 = "pink50"
        pink100 = "pink100"
        pink200 = "pink200"
        pink300 = "pink300"
        pink400 = "pink400"
        pink500 = "pink500"
        pink600 = "pink600"
        pink700 = "pink700"
        pink800 = "pink800"
        pink900 = "pink900"
        pinkA100 = "pinkA100"
        pinkA200 = "pinkA200"
        pinkA400 = "pinkA400"
        pinkA700 = "pinkA700"
        purple50 = "purple50"
        purple100 = "purple100"
        purple200 = "purple200"
        purple300 = "purple300"
        purple400 = "purple400"
        purple500 = "purple500"
        purple600 = "purple600"
        purple700 = "purple700"
        purple800 = "purple800"
        purple900 = "purple900"
        purpleA100 = "purpleA100"
        purpleA200 = "purpleA200"
        purpleA400 = "purpleA400"
        purpleA700 = "purpleA700"
        deepPurple50 = "deepPurple50"
        deepPurple100 = "deepPurple100"
        deepPurple200 = "deepPurple200"
        deepPurple300 = "deepPurple300"
        deepPurple400 = "deepPurple400"
        deepPurple500 = "deepPurple500"
        deepPurple600 = "deepPurple600"
        deepPurple700 = "deepPurple700"
        deepPurple800 = "deepPurple800"
        deepPurple900 = "deepPurple900"
        deepPurpleA100 = "deepPurpleA100"
        deepPurpleA200 = "deepPurpleA200"
        deepPurpleA400 = "deepPurpleA400"
        deepPurpleA700 = "deepPurpleA700"
        indigo50 = "indigo50"
        indigo100 = "indigo100"
        indigo200 = "indigo200"
        indigo300 = "indigo300"
        indigo400 = "indigo400"
        indigo500 = "indigo500"
        indigo600 = "indigo600"
        indigo700 = "indigo700"
        indigo800 = "indigo800"
        indigo900 = "indigo900"
        indigoA100 = "indigoA100"
        indigoA200 = "indigoA200"
        indigoA400 = "indigoA400"
        indigoA700 = "indigoA700"
        blue50 = "blue50"
        blue100 = "blue100"
        blue200 = "blue200"
        blue300 = "blue300"
        blue400 = "blue400"
        blue500 = "blue500"
        blue600 = "blue600"
        blue700 = "blue700"
        blue800 = "blue800"
        blue900 = "blue900"
        blueA100 = "blueA100"
        blueA200 = "blueA200"
        blueA400 = "blueA400"
        blueA700 = "blueA700"
        lightBlue50 = "lightBlue50"
        lightBlue100 = "lightBlue100"
        lightBlue200 = "lightBlue200"
        lightBlue300 = "lightBlue300"
        lightBlue400 = "lightBlue400"
        lightBlue500 = "lightBlue500"
        lightBlue600 = "lightBlue600"
        lightBlue700 = "lightBlue700"
        lightBlue800 = "lightBlue800"
        lightBlue900 = "lightBlue900"
        lightBlueA100 = "lightBlueA100"
        lightBlueA200 = "lightBlueA200"
        lightBlueA400 = "lightBlueA400"
        lightBlueA700 = "lightBlueA700"
        cyan50 = "cyan50"
        cyan100 = "cyan100"
        cyan200 = "cyan200"
        cyan300 = "cyan300"
        cyan400 = "cyan400"
        cyan500 = "cyan500"
        cyan600 = "cyan600"
        cyan700 = "cyan700"
        cyan800 = "cyan800"
        cyan900 = "cyan900"
        cyanA100 = "cyanA100"
        cyanA200 = "cyanA200"
        cyanA400 = "cyanA400"
        cyanA700 = "cyanA700"
        teal50 = "teal50"
        teal100 = "teal100"
        teal200 = "teal200"
        teal300 = "teal300"
        teal400 = "teal400"
        teal500 = "teal500"
        teal600 = "teal600"
        teal700 = "teal700"
        teal800 = "teal800"
        teal900 = "teal900"
        tealA100 = "tealA100"
        tealA200 = "tealA200"
        tealA400 = "tealA400"
        tealA700 = "tealA700"
        green50 = "green50"
        green100 = "green100"
        green200 = "green200"
        green300 = "green300"
        green400 = "green400"
        green500 = "green500"
        green600 = "green600"
        green700 = "green700"
        green800 = "green800"
        green900 = "green900"
        greenA100 = "greenA100"
        greenA200 = "greenA200"
        greenA400 = "greenA400"
        greenA700 = "greenA700"
        lightGreen50 = "lightGreen50"
        lightGreen100 = "lightGreen100"
        lightGreen200 = "lightGreen200"
        lightGreen300 = "lightGreen300"
        lightGreen400 = "lightGreen400"
        lightGreen500 = "lightGreen500"
        lightGreen600 = "lightGreen600"
        lightGreen700 = "lightGreen700"
        lightGreen800 = "lightGreen800"
        lightGreen900 = "lightGreen900"
        lightGreenA100 = "lightGreenA100"
        lightGreenA200 = "lightGreenA200"
        lightGreenA400 = "lightGreenA400"
        lightGreenA700 = "lightGreenA700"
        lime50 = "lime50"
        lime100 = "lime100"
        lime200 = "lime200"
        lime300 = "lime300"
        lime400 = "lime400"
        lime500 = "lime500"
        lime600 = "lime600"
        lime700 = "lime700"
        lime800 = "lime800"
        lime900 = "lime900"
        limeA100 = "limeA100"
        limeA200 = "limeA200"
        limeA400 = "limeA400"
        limeA700 = "limeA700"
        yellow50 = "yellow50"
        yellow100 = "yellow100"
        yellow200 = "yellow200"
        yellow300 = "yellow300"
        yellow400 = "yellow400"
        yellow500 = "yellow500"
        yellow600 = "yellow600"
        yellow700 = "yellow700"
        yellow800 = "yellow800"
        yellow900 = "yellow900"
        yellowA100 = "yellowA100"
        yellowA200 = "yellowA200"
        yellowA400 = "yellowA400"
        yellowA700 = "yellowA700"
        amber50 = "amber50"
        amber100 = "amber100"
        amber200 = "amber200"
        amber300 = "amber300"
        amber400 = "amber400"
        amber500 = "amber500"
        amber600 = "amber600"
        amber700 = "amber700"
        amber800 = "amber800"
        amber900 = "amber900"
        amberA100 = "amberA100"
        amberA200 = "amberA200"
        amberA400 = "amberA400"
        amberA700 = "amberA700"
        orange50 = "orange50"
        orange100 = "orange100"
        orange200 = "orange200"
        orange300 = "orange300"
        orange400 = "orange400"
        orange500 = "orange500"
        orange600 = "orange600"
        orange700 = "orange700"
        orange800 = "orange800"
        orange900 = "orange900"
        orangeA100 = "orangeA100"
        orangeA200 = "orangeA200"
        orangeA400 = "orangeA400"
        orangeA700 = "orangeA700"
        deepOrange50 = "deepOrange50"
        deepOrange100 = "deepOrange100"
        deepOrange200 = "deepOrange200"
        deepOrange300 = "deepOrange300"
        deepOrange400 = "deepOrange400"
        deepOrange500 = "deepOrange500"
        deepOrange600 = "deepOrange600"
        deepOrange700 = "deepOrange700"
        deepOrange800 = "deepOrange800"
        deepOrange900 = "deepOrange900"
        deepOrangeA100 = "deepOrangeA100"
        deepOrangeA200 = "deepOrangeA200"
        deepOrangeA400 = "deepOrangeA400"
        deepOrangeA700 = "deepOrangeA700"
        brown50 = "brown50"
        brown100 = "brown100"
        brown200 = "brown200"
        brown300 = "brown300"
        brown400 = "brown400"
        brown500 = "brown500"
        brown600 = "brown600"
        brown700 = "brown700"
        brown800 = "brown800"
        brown900 = "brown900"
        blueGrey50 = "blueGrey50"
        blueGrey100 = "blueGrey100"
        blueGrey200 = "blueGrey200"
        blueGrey300 = "blueGrey300"
        blueGrey400 = "blueGrey400"
        blueGrey500 = "blueGrey500"
        blueGrey600 = "blueGrey600"
        blueGrey700 = "blueGrey700"
        blueGrey800 = "blueGrey800"
        blueGrey900 = "blueGrey900"
        grey50 = "grey50"
        grey100 = "grey100"
        grey200 = "grey200"
        grey300 = "grey300"
        grey400 = "grey400"
        grey500 = "grey500"
        grey600 = "grey600"
        grey700 = "grey700"
        grey800 = "grey800"
        grey900 = "grey900"
        black = "black"
        white = "white"
        transparent = "transparent"
        fullBlack = "fullBlack"
        darkBlack = "darkBlack"
        lightBlack = "lightBlack"
        minBlack = "minBlack"
        faintBlack = "faintBlack"
        fullWhite = "fullWhite"
        darkWhite = "darkWhite"
        lightWhite = "lightWhite"


class QtMaterialThemePrivate:
    ...


class QtMaterialTheme(QObject):
    def __init__(self, parent: QObject = None):
        self.d = QtMaterialThemePrivate(self)

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

    def __del__(self):
        ...

    def getColor(self, key: QString) -> QColor:
        if not self.d.colors.contains(key):
            print("A theme color matching the key '", key, "' could not be found.")
            return QColor()

        return self.d.colors.value(key)

    # color2 is just to show that possible colors are of two type types, color2 is never used in this method. Because python does not support function & method overloading.
    def setColor(
        self, key: QString, color: QColor, color2: Material.Color = None
    ) -> void:
        _color = None
        if isinstance(color, QColor):
            _color = color
        else:
            palette: List[QColor] = [
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
            _color = palette[color]

        self.d.colors.insert(key, _color)

    @staticmethod
    def icon(self, category: QString, icon: QString) -> QIcon:
        return QIcon(
            ":/icons/icons/" % category % "/svg/production/ic_" % icon % "_24px.svg"
        )
