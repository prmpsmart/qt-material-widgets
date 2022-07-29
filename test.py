from qt_material import *


class StateTest(QWidget):
    def __init__(self) -> None:
        super().__init__(f=Qt.WindowStaysOnTopHint)

        self.lay = QVBoxLayout(self)
        # self.setMinimumWidth(200)

        self.testEasingCurves()
        self.testFlatButton()
        self.testRaisedButton()
        self.testIconButton()
        self.testRadioButton()
        self.testFABButton()
        self.testCheckButton()

        self.testDrawer()
        self.testDialog()

        self.show()

    def testEasingCurves(self):
        easings = [
            QEasingCurve.Linear,
            QEasingCurve.InQuad,
            QEasingCurve.OutQuad,
            QEasingCurve.InOutQuad,
            QEasingCurve.OutInQuad,
            QEasingCurve.InCubic,
            QEasingCurve.OutCubic,
            QEasingCurve.InOutCubic,
            QEasingCurve.OutInCubic,
            QEasingCurve.InQuart,
            QEasingCurve.OutQuart,
            QEasingCurve.InOutQuart,
            QEasingCurve.OutInQuart,
            QEasingCurve.InQuint,
            QEasingCurve.OutQuint,
            QEasingCurve.InOutQuint,
            QEasingCurve.OutInQuint,
            QEasingCurve.InSine,
            QEasingCurve.OutSine,
            QEasingCurve.InOutSine,
            QEasingCurve.OutInSine,
            QEasingCurve.InExpo,
            QEasingCurve.OutExpo,
            QEasingCurve.InOutExpo,
            QEasingCurve.OutInExpo,
            QEasingCurve.InCirc,
            QEasingCurve.OutCirc,
            QEasingCurve.InOutCirc,
            QEasingCurve.OutInCirc,
            QEasingCurve.InElastic,
            QEasingCurve.OutElastic,
            QEasingCurve.InOutElastic,
            QEasingCurve.OutInElastic,
            QEasingCurve.InBack,
            QEasingCurve.OutBack,
            QEasingCurve.InOutBack,
            QEasingCurve.OutInBack,
            QEasingCurve.InBounce,
            QEasingCurve.OutBounce,
            QEasingCurve.InOutBounce,
            QEasingCurve.OutInBounce,
            QEasingCurve.InCurve,
            QEasingCurve.OutCurve,
            QEasingCurve.SineCurve,
            QEasingCurve.CosineCurve,
            QEasingCurve.BezierSpline,
            QEasingCurve.TCBSpline,
            QEasingCurve.Custom,
            QEasingCurve.NCurveTypes,
        ]
        lay = QGridLayout()
        self.lay.addLayout(lay)

        row = 0
        cols = 11
        for index, easing in enumerate(easings):
            button = QMaterialFlatButton(
                "Button Test",
                foregroundColor=Qt.red,
                preset=None,
                overlayOpacity=0.5,
                rippleColor=Qt.green,
                easingCurve=easing,
            )
            button.setMinimumHeight(50)
            if index > 0 and not index % cols:
                row += 1
            lay.addWidget(button, row, index % cols)

    def testFlatButton(self):
        button = QMaterialFlatButton(
            "Flat Button Test",
            foregroundColor=Qt.red,
            backgroundColor=Qt.blue,
            useThemeColors=1,
            # preset=None,
            haloVisible=1,
            overlayOpacity=0.5,
            rippleColor=Qt.green,
        )
        button.setMinimumHeight(50)
        self.lay.addWidget(button)

    def testRaisedButton(self):
        button = QMaterialRaisedButton(
            "Raised Button Test",
            foregroundColor=Qt.red,
            # backgroundColor=Qt.darkBlue,
            # preset=None,
            overlayOpacity=0.5,
            rippleColor=Qt.green,
        )
        button.setMinimumHeight(50)
        self.lay.addWidget(button)

    def testIconButton(self):
        hlay = QHBoxLayout()
        self.lay.addLayout(hlay)
        m = 50

        for a in range(2):
            button = QMaterialIconButton(
                # "res/icon.jpg",
               ":action/alarm_off.svg",
                size=QSize(m, m),
                rippleColor=Qt.red,
                # preset=None,
                # overlayOpacity=0.5,
            )
            button.setMinimumHeight(50)
            hlay.addWidget(button)

    def testCheckButton(self):
        lay = QHBoxLayout()
        self.lay.addLayout(lay)
        
        for a in range(4):
            button = QMaterialCheckBox(
            text=f"Lovely {a}",
            checkedColor=Qt.green,
            uncheckedColor=Qt.red,
            radius=50,
            flipToggle=a > 1,
        )
            lay.addWidget(button)

    def testRadioButton(self):
        lay = QHBoxLayout()
        self.lay.addLayout(lay)

        for a in range(4):
            button = QMaterialRadioButton(
            text=f"Lovely {a}",
            checkedColor=Qt.green,
            uncheckedColor=Qt.red,
            radius=50,
            flipToggle=a > 1,
        )
            lay.addWidget(button)

    def testFABButton(self):
        lay = QHBoxLayout()
        self.lay.addLayout(lay)

        for a in range(4):
            button = QMaterialFloatingActionButton(
            ":action/alarm_off.svg",
        )
            lay.addWidget(button)

    def testDrawer(self):
        self.m = QMaterialDialog(self)
        self.m.setMinimumSize(200, 100)

        def op():
            print(990)
            self.m.showDialog()

        but = QMaterialRaisedButton(text='Open')
        but.clicked.connect(op)
        self.lay.addWidget(but)
        

    def testDialog(self):
        ...

app = QApplication()

test = StateTest()

app.exec()
