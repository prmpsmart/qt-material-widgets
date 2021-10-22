import os

currentFolder: str = os.getcwd()
pyFolder = os.path.dirname(currentFolder)
os.sys.path.append(pyFolder)

from components.app_bar import *
from components.autocomplete import *
from components.avatar import *
from components.badge import *
from components.checkbox import *
from components.circularprogress import *
from components.dialog import *
from components.drawer import *
from components.fab import *
from components.flatbutton import *
from components.iconbutton import *
from components.progress import *
from components.radiobutton import *
from components.raisedbutton import *
from components.scrollbar import *
from components.slider import *
from components.snackbar import *
from components.tabs import *
from components.textfield import *
from components.toggle import *

# import examples_resources


# Created to save the trouble of repeating some basics as in the cpp version
class Example_QWidget(QWidget):
    ui_file = ""

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.ui = None
        self.ui_name = ""
        self.ui_parent = None

        self.loadUi()

    def loadUi(self):
        self.ui_parent = QWidget()

        d = os.path.dirname(__file__)
        uiType = loadUiType(os.path.join(d, QString("uis/%s.ui").arg(self.ui_file)))
        
        if uiType:
            form, _ = uiType
            self.ui_name = form.__name__
            self.ui = form()
            self.ui.setupUi(self.ui_parent)

    def __del__(self):
        del self.ui


class AppBarSettingsEditor(Example_QWidget):
    ui_file = "appbarsettingsform"

    def __init__(self, parent: QWidget = None):
        Example_QWidget.__init__(self, parent)

        self.m_appBar = QtMaterialAppBar()

        label = QLabel("Inbox")
        label.setAttribute(Qt.WA_TranslucentBackground)
        label.setForegroundRole(QPalette.WindowText)
        label.setContentsMargins(6, 0, 0, 0)

        palette = label.palette()
        palette.setColor(label.foregroundRole(), Qt.white)
        label.setPalette(palette)

        label.setFont(QFont("Roboto", 18, QFont.Normal))

        button = QtMaterialIconButton(QtMaterialTheme.icon("navigation", "menu"))
        button.setIconSize(QSize(24, 24))
        self.m_appBar.appBarLayout().addWidget(button)
        self.m_appBar.appBarLayout().addWidget(label)
        self.m_appBar.appBarLayout().addStretch(1)
        button.setColor(Qt.white)
        button.setFixedWidth(42)

        layout = QVBoxLayout()
        self.setLayout(layout)

        widget = self.ui_parent
        layout.addWidget(widget)

        canvas = QWidget()
        canvas.setStyleSheet("QWidget { background: white }")
        layout.addWidget(canvas)

        self.ui.setupUi(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        layout = QVBoxLayout()
        canvas.setLayout(layout)
        canvas.setMaximumHeight(300)
        layout.addWidget(self.m_appBar)
        layout.addStretch(1)

        self.setupForm()

        self.ui.useThemeColorsCheckBox.toggled.connect(self.updateWidget)
        self.ui.backgroundColorToolButton.pressed.connect(self.selectColor)

    def setupForm(self) -> void:
        self.ui.useThemeColorsCheckBox.setChecked(self.m_appBar.useThemeColors())

    def updateWidget(self) -> void:
        self.m_appBar.setUseThemeColors(self.ui.useThemeColorsCheckBox.isChecked())

    def selectColor(self) -> void:
        dialog = QColorDialog()
        if dialog.exec():
            color: QColor = dialog.selectedColor()
            senderName: QString = self.sender().objectName()
            if "backgroundColorToolButton" == senderName:
                self.m_appBar.setBackgroundColor(color)
                self.ui.backgroundColorLineEdit.setText(color.name(QColor.HexRgb))

        self.setupForm()


class AutoCompleteSettingsEditor(Example_QWidget):
    ui_file = "autocompletesettingsform"

    def __init__(self, parent: QWidget = None):
        Example_QWidget.__init__(self, parent)

        self.m_autocomplete = QtMaterialAutoComplete()

        layout = QVBoxLayout()
        self.setLayout(layout)

        widget = self.ui_parent
        layout.addWidget(widget)

        canvas = QWidget()
        canvas.setStyleSheet("QWidget { background: white }")
        layout.addWidget(canvas)

        canvas.setMinimumHeight(500)

        layout.setContentsMargins(20, 20, 20, 20)

        layout = QVBoxLayout()
        canvas.setLayout(layout)

        states: QStringList = [
            "Alabama",
            "Alaska",
            "American Samoa",
            "Arizona",
            "Arkansas",
            "California",
            "Colorado",
            "Connecticut",
            "Delaware",
            "District of Columbia",
            "Florida",
            "Georgia",
            "Guam",
            "Hawaii",
            "Idaho",
            "Illinois",
            "Indiana",
            "Iowa",
            "Kansas",
            "Kentucky",
            "Louisiana",
            "Maine",
            "Maryland",
            "Massachusetts",
            "Michigan",
            "Minnesota",
            "Mississippi",
            "Missouri",
            "Montana",
            "Nebraska",
            "Nevada",
            "New Hampshire",
            "New Jersey",
            "New Mexico",
            "New York",
            "North Carolina",
            "North Dakota",
            "Northern Marianas Islands",
            "Ohio",
            "Oklahoma",
            "Oregon",
            "Pennsylvania",
            "Puerto Rico",
            "Rhode Island",
            "South Carolina",
            "South Dakota",
            "Tennessee",
            "Texas",
            "Utah",
            "Vermont",
            "Virginia",
            "Virgin Islands",
            "Washington",
            "West Virginia",
            "Wisconsin",
            "Wyoming",
        ]

        self.m_autocomplete.setDataSource(states)

        layout.addWidget(self.m_autocomplete)
        layout.addSpacing(600)
        layout.setAlignment(self.m_autocomplete, Qt.AlignCenter)

        self.setupForm()

    def setupForm(self) -> void:
        ...

    def updateWidget(self) -> void:
        ...

    def selectColor(self) -> void:
        ...


class AvatarSettingsEditor(Example_QWidget):
    ui_file = "avatarsettingsform"

    def __init__(self, parent: QWidget = None):
        Example_QWidget.__init__(self, parent)

        self.m_avatar = QtMaterialAvatar(letter=QChar("X"))

        layout = QVBoxLayout()
        self.setLayout(layout)

        widget = self.ui_parent
        layout.addWidget(widget)

        canvas = QWidget()
        canvas.setStyleSheet("QWidget { background: white }")
        layout.addWidget(canvas)

        # self.ui.setupUi(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        layout = QVBoxLayout()
        canvas.setLayout(layout)
        layout.addWidget(self.m_avatar)
        layout.setAlignment(self.m_avatar, Qt.AlignCenter)

        self.setupForm()

        self.ui.disabledCheckBox.toggled.connect(self.updateWidget)
        self.ui.useThemeColorsCheckBox.toggled.connect(self.updateWidget)
        self.ui.sizeSpinBox.valueChanged.connect(self.updateWidget)
        self.ui.typeComboBox.currentIndexChanged.connect(self.updateWidget)
        self.ui.backgroundColorToolButton.pressed.connect(self.selectColor)
        self.ui.textColorToolButton.pressed.connect(self.selectColor)

        self.ui.sizeSpinBox.setRange(5, 300)

    def setupForm(self) -> void:
        typ = self.m_avatar.type()
        if typ == Material.LetterAvatar:
            self.ui.typeComboBox.setCurrentIndex(0)

        elif typ == Material.ImageAvatar:
            self.ui.typeComboBox.setCurrentIndex(1)

        elif typ == Material.IconAvatar:
            self.ui.typeComboBox.setCurrentIndex(2)

        self.ui.disabledCheckBox.setChecked(not self.m_avatar.isEnabled())
        self.ui.useThemeColorsCheckBox.setChecked(self.m_avatar.useThemeColors())
        self.ui.sizeSpinBox.setValue(self.m_avatar.size())

    def updateWidget(self) -> void:
        index = self.ui.typeComboBox.currentIndex()
        if index == 0:
            self.m_avatar.setLetter(QChar("X"))

        elif index == 1:
            self.m_avatar.setImage(QImage("assets/sikh.jpg"))

        elif index == 2:
            self.m_avatar.setIcon(QtMaterialTheme.icon("communication", "message"))

        self.m_avatar.setDisabled(self.ui.disabledCheckBox.isChecked())
        self.m_avatar.setUseThemeColors(self.ui.useThemeColorsCheckBox.isChecked())
        self.m_avatar.setSize(self.ui.sizeSpinBox.value())

    def selectColor(self) -> void:
        dialog = QColorDialog()
        if dialog.exec():
            color: QColor = dialog.selectedColor()
            senderName: QString = self.sender().objectName()
            if "textColorToolButton" == senderName:
                self.m_avatar.setTextColor(color)
                self.ui.textColorLineEdit.setText(color.name(QColor.HexRgb))
            elif "backgroundColorToolButton" == senderName:
                self.m_avatar.setBackgroundColor(color)
                self.ui.backgroundColorLineEdit.setText(color.name(QColor.HexRgb))

        self.setupForm()


class BadgeSettingsEditor(Example_QWidget):
    ui_file = "badgesettingsform"

    def __init__(self, parent: QWidget = None):
        Example_QWidget.__init__(self, parent)

        self.m_avatar = QtMaterialAvatar(image=QImage(":assets/sikh.jpg"))
        self.m_badge = QtMaterialBadge()

        layout = QVBoxLayout()
        self.setLayout(layout)

        widget = self.ui_parent
        layout.addWidget(widget)

        canvas = QWidget()
        canvas.setStyleSheet("QWidget { background: white }")
        layout.addWidget(canvas)

        # self.ui.setupUi(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        layout = QVBoxLayout()
        canvas.setLayout(layout)
        layout.addWidget(self.m_avatar)
        layout.setAlignment(self.m_avatar, Qt.AlignCenter)
        self.m_avatar.setSize(60)

        self.m_badge.setParent(self.m_avatar)
        self.m_badge.setRelativePosition(18, 18)
        self.m_badge.setText("3000")

        self.setupForm()

        self.ui.disabledCheckBox.toggled.connect(self.updateWidget)
        self.ui.typeComboBox.currentIndexChanged.connect(self.updateWidget)
        self.ui.useThemeColorsCheckBox.toggled.connect(self.updateWidget)
        self.ui.horizontalOffsetSpinBox.valueChanged.connect(self.updateWidget)
        self.ui.verticalOffsetSpinBox.valueChanged.connect(self.updateWidget)
        self.ui.backgroundColorToolButton.pressed.connect(self.selectColor)
        self.ui.textColorToolButton.pressed.connect(self.selectColor)

        self.ui.verticalOffsetSpinBox.setRange(-40, 40)
        self.ui.horizontalOffsetSpinBox.setRange(-40, 40)

    def setupForm(self) -> void:
        if self.m_badge.icon().isNull():
            self.ui.typeComboBox.setCurrentIndex(0)
        else:
            self.ui.typeComboBox.setCurrentIndex(1)

        self.ui.verticalOffsetSpinBox.setValue(self.m_badge.relativeYPosition())
        self.ui.horizontalOffsetSpinBox.setValue(self.m_badge.relativeXPosition())
        self.ui.disabledCheckBox.setChecked(not self.m_badge.isEnabled())
        self.ui.useThemeColorsCheckBox.setChecked(self.m_badge.useThemeColors())

    def updateWidget(self) -> void:
        index = self.ui.typeComboBox.currentIndex()

        if index == 0:
            self.m_badge.setText("300")

        elif index == 1:
            self.m_badge.setIcon(
                QIcon(QtMaterialTheme.icon("communication", "message"))
            )

        self.m_badge.setRelativeYPosition(self.ui.verticalOffsetSpinBox.value())
        self.m_badge.setRelativeXPosition(self.ui.horizontalOffsetSpinBox.value())
        self.m_badge.setDisabled(self.ui.disabledCheckBox.isChecked())
        self.m_badge.setUseThemeColors(self.ui.useThemeColorsCheckBox.isChecked())

    def selectColor(self) -> void:
        dialog = QColorDialog()

        if dialog.exec():
            color: QColor = dialog.selectedColor()
            senderName: QString = self.sender().objectName()
            if "textColorToolButton" == senderName:
                self.m_badge.setTextColor(color)
                self.ui.textColorLineEdit.setText(color.name(QColor.HexRgb))
            elif "backgroundColorToolButton" == senderName:
                self.m_badge.setBackgroundColor(color)
                self.ui.backgroundColorLineEdit.setText(color.name(QColor.HexRgb))

        self.setupForm()


class CheckBoxSettingsEditor(Example_QWidget):
    ui_file = "checkboxsettingsform"

    def __init__(self, parent: QWidget = None):
        Example_QWidget.__init__(self, parent)

        self.m_checkBox = QtMaterialCheckable(parent=self)

        layout = QVBoxLayout()
        self.setLayout(layout)

        widget = self.ui_parent
        layout.addWidget(widget)

        canvas = QWidget()
        canvas.setStyleSheet("QWidget { background: white }")
        layout.addWidget(canvas)

        # self.ui.setupUi(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        self.m_checkBox.setText("Extra cheese")
        self.m_checkBox.setChecked(true)

        layout = QVBoxLayout()
        canvas.setLayout(layout)
        layout.addWidget(self.m_checkBox)
        layout.setAlignment(self.m_checkBox, Qt.AlignCenter)

        self.setupForm()

        self.ui.disabledCheckBox.toggled.connect(self.updateWidget)
        self.ui.labelPositionComboBox.currentIndexChanged.connect(self.updateWidget)
        self.ui.labelTextLineEdit.textChanged.connect(self.updateWidget)
        self.ui.useThemeColorsCheckBox.toggled.connect(self.updateWidget)
        self.ui.checkedCheckBox.toggled.connect(self.updateWidget)
        self.ui.textColorToolButton.pressed.connect(self.selectColor)
        self.ui.disabledColorToolButton.pressed.connect(self.selectColor)
        self.ui.checkedColorToolButton.pressed.connect(self.selectColor)
        self.ui.uncheckedColorToolButton.pressed.connect(self.selectColor)
        self.m_checkBox.toggled.connect(self.setupForm)

    def setupForm(self) -> void:
        pos = self.m_checkBox.labelPosition()

        if pos == QtMaterialCheckable.LabelPositionLeft:
            self.ui.labelPositionComboBox.setCurrentIndex(0)

        if pos == QtMaterialCheckable.LabelPositionRight:
            self.ui.labelPositionComboBox.setCurrentIndex(1)

        self.ui.disabledCheckBox.setChecked(not self.m_checkBox.isEnabled())
        self.ui.labelTextLineEdit.setText(self.m_checkBox.text())
        self.ui.useThemeColorsCheckBox.setChecked(self.m_checkBox.useThemeColors())
        self.ui.checkedCheckBox.setChecked(self.m_checkBox.isChecked())

    def updateWidget(self) -> void:
        index = self.ui.labelPositionComboBox.currentIndex()

        if index == 0:
            self.m_checkBox.setLabelPosition(QtMaterialCheckable.LabelPositionLeft)

        elif index == 1:
            self.m_checkBox.setLabelPosition(QtMaterialCheckable.LabelPositionRight)

        self.m_checkBox.setDisabled(self.ui.disabledCheckBox.isChecked())
        self.m_checkBox.setText(self.ui.labelTextLineEdit.text())
        self.m_checkBox.setUseThemeColors(self.ui.useThemeColorsCheckBox.isChecked())
        self.m_checkBox.setChecked(self.ui.checkedCheckBox.isChecked())

    def selectColor(self) -> void:
        dialog = QColorDialog()
        if dialog.exec():
            color: QColor = dialog.selectedColor()
            senderName: QString = self.sender().objectName()
            if "textColorToolButton" == senderName:
                self.m_checkBox.setTextColor(color)
                self.ui.textColorLineEdit.setText(color.name(QColor.HexRgb))
            elif "disabledColorToolButton" == senderName:
                self.m_checkBox.setDisabledColor(color)
                self.ui.disabledColorLineEdit.setText(color.name(QColor.HexRgb))
            elif "checkedColorToolButton" == senderName:
                self.m_checkBox.setCheckedColor(color)
                self.ui.checkedColorLineEdit.setText(color.name(QColor.HexRgb))
            elif "uncheckedColorToolButton" == senderName:
                self.m_checkBox.setUncheckedColor(color)
                self.ui.uncheckedColorLineEdit.setText(color.name(QColor.HexRgb))

        self.setupForm()


class CircularProgressSettingsEditor(Example_QWidget):
    ui_file = "circularprogresssettingsform"

    def __init__(self, parent: QWidget = None):
        Example_QWidget.__init__(self, parent)

        self.m_progress = QtMaterialCircularProgress()

        layout = QVBoxLayout()
        self.setLayout(layout)

        widget = self.ui_parent
        layout.addWidget(widget)

        canvas = QWidget()
        canvas.setStyleSheet("QWidget { background: white }")
        layout.addWidget(canvas)

        # self.ui.setupUi(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        layout = QVBoxLayout()
        canvas.setLayout(layout)
        layout.addWidget(self.m_progress)
        layout.setAlignment(self.m_progress, Qt.AlignCenter)

        self.setupForm()

        self.ui.disabledCheckBox.toggled.connect(self.updateWidget)
        self.ui.progressTypeComboBox.currentIndexChanged.connect(self.updateWidget)
        self.ui.progressSlider.valueChanged.connect(self.updateWidget)
        self.ui.lineWidthDoubleSpinBox.valueChanged.connect(self.updateWidget)
        self.ui.sizeSpinBox.valueChanged.connect(self.updateWidget)
        self.ui.useThemeColorsCheckBox.toggled.connect(self.updateWidget)
        self.ui.colorToolButton.pressed.connect(self.selectColor)

        self.ui.sizeSpinBox.setRange(10, 200)
        self.ui.progressSlider.setRange(0, 100)

    def setupForm(self) -> void:
        typ = self.m_progress.progressType()

        if typ == Material.DeterminateProgress:
            self.ui.progressTypeComboBox.setCurrentIndex(0)

        elif typ == Material.IndeterminateProgress:
            self.ui.progressTypeComboBox.setCurrentIndex(1)

        self.ui.disabledCheckBox.setChecked(not self.m_progress.isEnabled())
        self.ui.progressSlider.setValue(self.m_progress.value())
        self.ui.lineWidthDoubleSpinBox.setValue(self.m_progress.lineWidth())
        self.ui.sizeSpinBox.setValue(self.m_progress.size())
        self.ui.useThemeColorsCheckBox.setChecked(self.m_progress.useThemeColors())

    def updateWidget(self) -> void:
        ind = self.ui.progressTypeComboBox.currentIndex()

        if ind == 0:
            self.m_progress.setProgressType(Material.DeterminateProgress)

        elif ind == 1:
            self.m_progress.setProgressType(Material.IndeterminateProgress)

        self.m_progress.setDisabled(self.ui.disabledCheckBox.isChecked())
        self.m_progress.setValue(self.ui.progressSlider.value())
        self.m_progress.setLineWidth(self.ui.lineWidthDoubleSpinBox.value())
        self.m_progress.setSize(self.ui.sizeSpinBox.value())
        self.m_progress.setUseThemeColors(self.ui.useThemeColorsCheckBox.isChecked())

    def selectColor(self) -> void:
        dialog = QColorDialog()
        if dialog.exec():
            color: QColor = dialog.selectedColor()
            senderName: QString = self.sender().objectName()
            if "colorToolButton" == senderName:
                self.m_progress.setColor(color)
                self.ui.colorLineEdit.setText(color.name(QColor.HexRgb))

        self.setupForm()


class DialogSettingsEditor(Example_QWidget):
    ui_file = "dialogsettingsform"

    def __init__(self, parent: QWidget = None):
        Example_QWidget.__init__(self, parent)

        self.m_dialog = QtMaterialDialog()

        layout = QVBoxLayout()
        self.setLayout(layout)

        widget = self.ui_parent
        layout.addWidget(widget)

        canvas = QWidget()
        canvas.setStyleSheet("QWidget { background: white }")
        layout.addWidget(canvas)

        # self.ui.setupUi(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        layout = QVBoxLayout()
        canvas.setLayout(layout)
        canvas.setMaximumHeight(300)

        self.m_dialog.setParent(self)

        dialogWidget = QWidget()
        dialogWidgetLayout = QVBoxLayout()
        dialogWidget.setLayout(dialogWidgetLayout)

        closeButton = QtMaterialFlatButton("Close")
        dialogWidgetLayout.addWidget(closeButton)
        dialogWidgetLayout.setAlignment(closeButton, Qt.AlignBottom | Qt.AlignCenter)

        closeButton.setMaximumWidth(150)

        dialogLayout = QVBoxLayout()
        self.m_dialog.setWindowLayout(dialogLayout)

        dialogWidget.setMinimumHeight(300)

        dialogLayout.addWidget(dialogWidget)

        self.setupForm()

        self.ui.showDialogButton.pressed.connect(self.m_dialog.showDialog)
        closeButton.pressed.connect(self.m_dialog.hideDialog)

    def setupForm(self) -> void:
        ...

    def updateWidget(self) -> void:
        ...


class DrawerSettingsEditor(Example_QWidget):
    ui_file = "drawersettingsform"

    def __init__(self, parent: QWidget = None):
        Example_QWidget.__init__(self, parent)

        self.m_drawer = QtMaterialDrawer()

        layout = QVBoxLayout()
        self.setLayout(layout)

        widget = self.ui_parent
        layout.addWidget(widget)

        canvas = QWidget()
        canvas.setStyleSheet("QWidget { background: white }")
        layout.addWidget(canvas)

        # self.ui.setupUi(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        layout = QVBoxLayout()
        canvas.setLayout(layout)
        canvas.setMaximumHeight(300)

        self.m_drawer.setParent(canvas)
        self.m_drawer.setClickOutsideToClose(true)
        self.m_drawer.setOverlayMode(true)

        drawerLayout = QVBoxLayout()
        self.m_drawer.setDrawerLayout(drawerLayout)

        labels = [
            "Motion",
            "Style",
            "Layout",
            "Components",
            "Patterns",
            "Growth & communications",
            "Usability",
            "Platforms",
            "Resources",
        ]

        for it in labels:
            label = QLabel(it)
            label.setMinimumHeight(30)
            label.setFont(QFont("Roboto", 10, QFont.Medium))
            drawerLayout.addWidget(label)

        drawerLayout.addStretch(3)
        self.m_drawer.setContentsMargins(10, 0, 0, 0)

        drawerLayout.addWidget(QPushButton("abc"))

        self.setupForm()

        self.ui.showDrawerButton.pressed.connect(self.m_drawer.openDrawer)
        self.ui.hideDrawerButton.pressed.connect(self.m_drawer.closeDrawer)
        self.ui.clickToCloseCheckBox.toggled.connect(self.updateWidget)
        self.ui.overlayModeCheckBox.toggled.connect(self.updateWidget)

    def setupForm(self) -> void:
        self.ui.clickToCloseCheckBox.setChecked(self.m_drawer.clickOutsideToClose())
        self.ui.overlayModeCheckBox.setChecked(self.m_drawer.overlayMode())

    def updateWidget(self) -> void:
        self.m_drawer.setClickOutsideToClose(self.ui.clickToCloseCheckBox.isChecked())
        self.m_drawer.setOverlayMode(self.ui.overlayModeCheckBox.isChecked())


class FloatingActionButtonSettingsEditor(Example_QWidget):
    ui_file = "fabsettingsform"

    def __init__(self, parent: QWidget = None):
        Example_QWidget.__init__(self, parent)

        self.m_fab = QtMaterialFloatingActionButton(
            icon=QtMaterialTheme.icon("toggle", "star"), parent=self
        )

        layout = QVBoxLayout()
        self.setLayout(layout)

        widget = self.ui_parent
        layout.addWidget(widget)

        canvas = QWidget()
        canvas.setStyleSheet("QWidget { background: white }")
        layout.addWidget(canvas)

        # self.ui.setupUi(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        self.m_fab.setParent(canvas)

        self.setupForm()

        self.ui.disabledCheckBox.toggled.connect(self.updateWidget)
        self.ui.buttonRoleComboBox.currentIndexChanged.connect(self.updateWidget)
        self.ui.cornerComboBox.currentIndexChanged.connect(self.updateWidget)
        self.ui.horizontalOffsetSpinBox.valueChanged.connect(self.updateWidget)
        self.ui.verticalOffsetSpinBox.valueChanged.connect(self.updateWidget)
        self.ui.miniCheckBox.toggled.connect(self.updateWidget)
        self.ui.rippleStyleComboBox.currentIndexChanged.connect(self.updateWidget)
        self.ui.useThemeColorsCheckBox.toggled.connect(self.updateWidget)
        self.ui.foregroundColorToolButton.clicked.connect(self.selectColor)
        self.ui.backgroundColorToolButton.clicked.connect(self.selectColor)
        self.ui.disabledFgColorToolButton.clicked.connect(self.selectColor)
        self.ui.disabledBgColorToolButton.clicked.connect(self.selectColor)

    def setupForm(self) -> void:
        role = self.m_fab.role()

        if role == Material.Default:
            self.ui.buttonRoleComboBox.setCurrentIndex(0)

        elif role == Material.Primary:
            self.ui.buttonRoleComboBox.setCurrentIndex(1)

        elif role == Material.Secondary:
            self.ui.buttonRoleComboBox.setCurrentIndex(2)

        corner = self.m_fab.corner()

        if corner == Qt.TopLeftCorner:
            self.ui.cornerComboBox.setCurrentIndex(0)

        elif corner == Qt.TopRightCorner:
            self.ui.cornerComboBox.setCurrentIndex(1)

        elif corner == Qt.BottomLeftCorner:
            self.ui.cornerComboBox.setCurrentIndex(2)

        elif corner == Qt.BottomRightCorner:
            self.ui.cornerComboBox.setCurrentIndex(3)

        rippleStyle = self.m_fab.rippleStyle()

        if rippleStyle == Material.CenteredRipple:
            self.ui.rippleStyleComboBox.setCurrentIndex(0)

        elif rippleStyle == Material.PositionedRipple:
            self.ui.rippleStyleComboBox.setCurrentIndex(1)

        elif rippleStyle == Material.NoRipple:
            self.ui.rippleStyleComboBox.setCurrentIndex(2)

        self.ui.disabledCheckBox.setChecked(not self.m_fab.isEnabled())
        self.ui.horizontalOffsetSpinBox.setValue(self.m_fab.xOffset())
        self.ui.verticalOffsetSpinBox.setValue(self.m_fab.yOffset())
        self.ui.miniCheckBox.setChecked(self.m_fab.isMini())
        self.ui.useThemeColorsCheckBox.setChecked(self.m_fab.useThemeColors())

    def updateWidget(self) -> void:
        currentIndex = self.ui.buttonRoleComboBox.currentIndex()

        if currentIndex == 0:
            self.m_fab.setRole(Material.Default)

        elif currentIndex == 1:
            self.m_fab.setRole(Material.Primary)

        elif currentIndex == 2:
            self.m_fab.setRole(Material.Secondary)

        currentIndex = self.ui.cornerComboBox.currentIndex()

        if currentIndex == 0:
            self.m_fab.setCorner(Qt.TopLeftCorner)

        elif currentIndex == 1:
            self.m_fab.setCorner(Qt.TopRightCorner)

        elif currentIndex == 2:
            self.m_fab.setCorner(Qt.BottomLeftCorner)

        elif currentIndex == 3:
            self.m_fab.setCorner(Qt.BottomRightCorner)

        currentIndex = self.ui.rippleStyleComboBox.currentIndex()

        if currentIndex == 0:
            self.m_fab.setRippleStyle(Material.CenteredRipple)

        elif currentIndex == 1:
            self.m_fab.setRippleStyle(Material.PositionedRipple)

        elif currentIndex == 2:
            self.m_fab.setRippleStyle(Material.NoRipple)

        self.m_fab.setDisabled(self.ui.disabledCheckBox.isChecked())
        self.m_fab.setXOffset(self.ui.horizontalOffsetSpinBox.value())
        self.m_fab.setYOffset(self.ui.verticalOffsetSpinBox.value())
        self.m_fab.setMini(self.ui.miniCheckBox.isChecked())
        self.m_fab.setUseThemeColors(self.ui.useThemeColorsCheckBox.isChecked())

    def selectColor(self) -> void:
        dialog = QColorDialog()
        if dialog.exec():
            color: QColor = dialog.selectedColor()
            senderName: QString = self.sender().objectName()
            if "foregroundColorToolButton" == senderName:
                self.m_fab.setForegroundColor(color)
                self.ui.foregroundColorLineEdit.setText(color.name(QColor.HexRgb))
            elif "backgroundColorToolButton" == senderName:
                self.m_fab.setBackgroundColor(color)
                self.ui.backgroundColorLineEdit.setText(color.name(QColor.HexRgb))
            elif "disabledFgColorToolButton" == senderName:
                self.m_fab.setDisabledForegroundColor(color)
                self.ui.disabledFgColorLineEdit.setText(color.name(QColor.HexRgb))
            elif "disabledBgColorToolButton" == senderName:
                self.m_fab.setDisabledBackgroundColor(color)
                self.ui.disabledBgColorLineEdit.setText(color.name(QColor.HexRgb))

        self.setupForm()


class FlatButtonSettingsEditor(Example_QWidget):
    ui_file = "flatbuttonsettingsform"

    def __init__(self, button: QtMaterialFlatButton = None, parent: QWidget = None):
        Example_QWidget.__init__(self, parent)

        self.m_button = button or QtMaterialFlatButton("I'm flat")

        layout = QVBoxLayout()
        self.setLayout(layout)

        widget = self.ui_parent
        layout.addWidget(widget)

        canvas = QWidget()
        canvas.setStyleSheet("QWidget { background: white }")
        layout.addWidget(canvas)

        # self.ui.setupUi(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        self.m_button.setFixedWidth(300)

        layout = QVBoxLayout()
        canvas.setLayout(layout)
        layout.addWidget(self.m_button)
        layout.setAlignment(self.m_button, Qt.AlignCenter)

        self.setupForm()

        self.ui.disabledCheckBox.toggled.connect(self.updateWidget)
        self.ui.checkableCheckBox.toggled.connect(self.updateWidget)
        self.ui.checkedCheckBox.toggled.connect(self.updateWidget)
        self.ui.showHaloCheckBox.toggled.connect(self.updateWidget)
        self.ui.iconCheckBox.toggled.connect(self.updateWidget)
        self.ui.transparentCheckBox.toggled.connect(self.updateWidget)
        self.ui.buttonRoleComboBox.currentIndexChanged.connect(self.updateWidget)
        self.ui.rippleStyleComboBox.currentIndexChanged.connect(self.updateWidget)
        self.ui.hoverStyleComboBox.currentIndexChanged.connect(self.updateWidget)
        self.ui.iconPlacementComboBox.currentIndexChanged.connect(self.updateWidget)
        self.ui.textAlignmentComboBox.currentIndexChanged.connect(self.updateWidget)
        self.ui.cornerRadiusSpinBox.valueChanged.connect(self.updateWidget)
        self.ui.overlayOpacityDoubleSpinBox.valueChanged.connect(self.updateWidget)
        self.ui.iconSizeSpinBox.valueChanged.connect(self.updateWidget)
        self.ui.fontSizeDoubleSpinBox.valueChanged.connect(self.updateWidget)
        self.ui.buttonTextLineEdit.textChanged.connect(self.updateWidget)
        self.ui.useThemeColorsCheckBox.toggled.connect(self.updateWidget)
        self.ui.foregroundColorToolButton.clicked.connect(self.selectColor)
        self.ui.backgroundColorToolButton.clicked.connect(self.selectColor)
        self.ui.disabledFgColorToolButton.clicked.connect(self.selectColor)
        self.ui.disabledBgColorToolButton.clicked.connect(self.selectColor)
        self.ui.overlayColorToolButton.clicked.connect(self.selectColor)
        self.ui.cornerRadiusSpinBox.valueChanged.connect(self.updateWidget)
        self.ui.overlayOpacityDoubleSpinBox.valueChanged.connect(self.updateWidget)
        self.ui.iconSizeSpinBox.valueChanged.connect(self.updateWidget)
        self.ui.fontSizeDoubleSpinBox.valueChanged.connect(self.updateWidget)
        self.ui.buttonTextLineEdit.textChanged.connect(self.updateWidget)
        self.ui.defaultPresetPushButton.pressed.connect(self.applyDefaultPreset)
        self.ui.checkablePresetPushButton.pressed.connect(self.applyCheckablePreset)
        self.m_button.clicked.connect(self.ui.checkedCheckBox.setChecked)

        self.ui.buttonRoleComboBox.setCurrentIndex(1)

    def setupForm(self) -> void:

        role = self.m_button.role()
        if role == Material.Default:
            self.ui.buttonRoleComboBox.setCurrentIndex(0)

        elif role == Material.Primary:
            self.ui.buttonRoleComboBox.setCurrentIndex(1)

        elif role == Material.Secondary:
            self.ui.buttonRoleComboBox.setCurrentIndex(2)

        overlayStyle = self.m_button.overlayStyle()
        if overlayStyle == Material.NoOverlay:
            self.ui.hoverStyleComboBox.setCurrentIndex(0)

        elif overlayStyle == Material.TintedOverlay:
            self.ui.hoverStyleComboBox.setCurrentIndex(1)

        elif overlayStyle == Material.GrayOverlay:
            self.ui.hoverStyleComboBox.setCurrentIndex(2)

        rippleStyle = self.m_button.rippleStyle()
        if rippleStyle == Material.CenteredRipple:
            self.ui.rippleStyleComboBox.setCurrentIndex(0)

        elif rippleStyle == Material.PositionedRipple:
            self.ui.rippleStyleComboBox.setCurrentIndex(1)

        elif rippleStyle == Material.NoRipple:
            self.ui.rippleStyleComboBox.setCurrentIndex(2)

        iconPlacement = self.m_button.iconPlacement()
        if iconPlacement == Material.LeftIcon:
            self.ui.iconPlacementComboBox.setCurrentIndex(0)

        elif iconPlacement == Material.RightIcon:
            self.ui.iconPlacementComboBox.setCurrentIndex(1)

        if self.ui.textAlignmentComboBox.currentIndex() == Qt.AlignLeft:
            self.ui.textAlignmentComboBox.setCurrentIndex(0)

        else:
            self.ui.textAlignmentComboBox.setCurrentIndex(1)

        self.ui.checkedCheckBox.setEnabled(self.m_button.isCheckable())

        self.ui.disabledCheckBox.setChecked(not self.m_button.isEnabled())
        self.ui.checkableCheckBox.setChecked(self.m_button.isCheckable())
        self.ui.checkedCheckBox.setChecked(self.m_button.isChecked())
        self.ui.showHaloCheckBox.setChecked(self.m_button.isHaloVisible())
        self.ui.iconCheckBox.setChecked(not self.m_button.icon().isNull())
        self.ui.useThemeColorsCheckBox.setChecked(self.m_button.useThemeColors())
        self.ui.transparentCheckBox.setChecked(
            Qt.TransparentMode == self.m_button.backgroundMode()
        )
        self.ui.cornerRadiusSpinBox.setValue(self.m_button.cornerRadius())
        self.ui.overlayOpacityDoubleSpinBox.setValue(self.m_button.baseOpacity())
        self.ui.iconSizeSpinBox.setValue(self.m_button.iconSize().width())
        self.ui.fontSizeDoubleSpinBox.setValue(self.m_button.fontSize())
        self.ui.buttonTextLineEdit.setText(self.m_button.text())

    def updateWidget(self) -> void:
        currentIndex = self.ui.buttonRoleComboBox.currentIndex()
        if currentIndex == 0:
            self.m_button.setRole(Material.Default)

        elif currentIndex == 1:
            self.m_button.setRole(Material.Primary)

        elif currentIndex == 2:
            self.m_button.setRole(Material.Secondary)

        currentIndex = self.ui.hoverStyleComboBox.currentIndex()
        if currentIndex == 0:
            self.m_button.setOverlayStyle(Material.NoOverlay)

        elif currentIndex == 1:
            self.m_button.setOverlayStyle(Material.TintedOverlay)

        elif currentIndex == 2:
            self.m_button.setOverlayStyle(Material.GrayOverlay)

        currentIndex = self.ui.rippleStyleComboBox.currentIndex()
        if currentIndex == 0:
            self.m_button.setRippleStyle(Material.CenteredRipple)

        elif currentIndex == 1:
            self.m_button.setRippleStyle(Material.PositionedRipple)

        elif currentIndex == 2:
            self.m_button.setRippleStyle(Material.NoRipple)

        currentIndex = self.ui.iconPlacementComboBox.currentIndex()

        if currentIndex == 0:
            self.m_button.setIconPlacement(Material.LeftIcon)

        elif currentIndex == 1:
            self.m_button.setIconPlacement(Material.RightIcon)

        currentIndex = self.ui.textAlignmentComboBox.currentIndex()

        if currentIndex == 0:
            self.m_button.setTextAlignment(Qt.AlignLeft)

        else:
            self.m_button.setTextAlignment(Qt.AlignHCenter)

        self.m_button.setDisabled(self.ui.disabledCheckBox.isChecked())
        self.m_button.setCheckable(self.ui.checkableCheckBox.isChecked())
        self.m_button.setChecked(self.ui.checkedCheckBox.isChecked())
        self.m_button.setHaloVisible(self.ui.showHaloCheckBox.isChecked())
        self.m_button.setIcon(
            QtMaterialTheme.icon("toggle", "star")
            if self.ui.iconCheckBox.isChecked()
            else QIcon()
        )
        self.m_button.setUseThemeColors(self.ui.useThemeColorsCheckBox.isChecked())
        self.m_button.setBackgroundMode(
            Qt.TransparentMode
            if self.ui.transparentCheckBox.isChecked()
            else Qt.OpaqueMode
        )
        self.m_button.setCornerRadius(self.ui.cornerRadiusSpinBox.value())
        self.m_button.setBaseOpacity(self.ui.overlayOpacityDoubleSpinBox.value())
        self.m_button.setIconSize(
            QSize(self.ui.iconSizeSpinBox.value(), self.ui.iconSizeSpinBox.value())
        )
        self.m_button.setFontSize(self.ui.fontSizeDoubleSpinBox.value())
        self.m_button.setText(self.ui.buttonTextLineEdit.text())

        self.ui.checkedCheckBox.setEnabled(self.m_button.isCheckable())

    def selectColor(self) -> void:
        dialog = QColorDialog()
        if dialog.exec():
            color: QColor = dialog.selectedColor()
            senderName: QString = self.sender().objectName()
            if "foregroundColorToolButton" == senderName:
                self.m_button.setForegroundColor(color)
                self.ui.foregroundColorLineEdit.setText(color.name(QColor.HexRgb))
            elif "backgroundColorToolButton" == senderName:
                self.m_button.setBackgroundColor(color)
                self.ui.backgroundColorLineEdit.setText(color.name(QColor.HexRgb))
            elif "overlayColorToolButton" == senderName:
                self.m_button.setOverlayColor(color)
                self.ui.overlayColorLineEdit.setText(color.name(QColor.HexRgb))
            elif "disabledFgColorToolButton" == senderName:
                self.m_button.setDisabledForegroundColor(color)
                self.ui.disableFgColorLineEdit.setText(color.name(QColor.HexRgb))
            elif "disabledBgColorToolButton" == senderName:
                self.m_button.setDisabledBackgroundColor(color)
                self.ui.disabledBgColorLineEdit.setText(color.name(QColor.HexRgb))

        self.setupForm()

    def applyDefaultPreset(self) -> void:
        self.ui.buttonRoleComboBox.setCurrentIndex(0)
        self.ui.rippleStyleComboBox.setCurrentIndex(1)
        self.ui.iconPlacementComboBox.setCurrentIndex(0)
        self.ui.hoverStyleComboBox.setCurrentIndex(2)
        self.ui.textAlignmentComboBox.setCurrentIndex(1)
        self.ui.transparentCheckBox.setChecked(true)
        self.ui.cornerRadiusSpinBox.setValue(3)
        self.ui.overlayOpacityDoubleSpinBox.setValue(0.13)
        self.ui.fontSizeDoubleSpinBox.setValue(10)
        self.ui.useThemeColorsCheckBox.setChecked(true)
        self.ui.showHaloCheckBox.setChecked(true)
        self.ui.checkableCheckBox.setChecked(false)
        self.ui.disabledCheckBox.setChecked(false)
        self.updateWidget()
        self.m_button.applyPreset(Material.FlatPreset)

    def applyCheckablePreset(self) -> void:
        self.ui.buttonRoleComboBox.setCurrentIndex(0)
        self.ui.rippleStyleComboBox.setCurrentIndex(1)
        self.ui.iconPlacementComboBox.setCurrentIndex(0)
        self.ui.hoverStyleComboBox.setCurrentIndex(2)
        self.ui.textAlignmentComboBox.setCurrentIndex(1)
        self.ui.transparentCheckBox.setChecked(true)
        self.ui.cornerRadiusSpinBox.setValue(3)
        self.ui.overlayOpacityDoubleSpinBox.setValue(0.13)
        self.ui.fontSizeDoubleSpinBox.setValue(10)
        self.ui.useThemeColorsCheckBox.setChecked(true)
        self.ui.showHaloCheckBox.setChecked(true)
        self.ui.checkableCheckBox.setChecked(true)
        self.ui.disabledCheckBox.setChecked(false)
        self.updateWidget()
        self.m_button.applyPreset(Material.CheckablePreset)


class IconButtonSettingsEditor(Example_QWidget):
    ui_file = "iconbuttonsettingsform"

    def __init__(self, button: QtMaterialIconButton, parent: QWidget = None):
        Example_QWidget.__init__(self, parent)

        self.m_button = button or QtMaterialIconButton(
            QtMaterialTheme.icon("toggle", "star")
        )

        layout = QVBoxLayout()
        self.setLayout(layout)

        widget = self.ui_parent
        layout.addWidget(widget)

        canvas = QWidget()
        canvas.setStyleSheet("QWidget { background: white }")
        layout.addWidget(canvas)

        # self.ui.setupUi(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        layout = QVBoxLayout()
        canvas.setLayout(layout)
        layout.addWidget(self.m_button)
        layout.setAlignment(self.m_button, Qt.AlignCenter)

        self.setupForm()

        self.ui.disabledCheckBox.toggled.connect(self.updateWidget)
        self.ui.useThemeColorsCheckBox.toggled.connect(self.updateWidget)
        self.ui.colorToolButton.clicked.connect(self.selectColor)
        self.ui.disabledColorToolButton.clicked.connect(self.selectColor)
        self.ui.sizeSpinBox.valueChanged.connect(self.updateWidget)

    def setupForm(self) -> void:
        self.ui.disabledCheckBox.setChecked(not self.m_button.isEnabled())
        self.ui.useThemeColorsCheckBox.setChecked(self.m_button.useThemeColors())
        self.ui.sizeSpinBox.setValue(self.m_button.iconSize().width())

    def updateWidget(self) -> void:
        self.m_button.setDisabled(self.ui.disabledCheckBox.isChecked())
        self.m_button.setUseThemeColors(self.ui.useThemeColorsCheckBox.isChecked())
        self.m_button.setIconSize(
            QSize(self.ui.sizeSpinBox.value(), self.ui.sizeSpinBox.value())
        )

    def selectColor(self) -> void:
        dialog = QColorDialog()
        if dialog.exec():
            color: QColor = dialog.selectedColor()
            senderName: QString = self.sender().objectName()
            if "colorToolButton" == senderName:
                self.m_button.setColor(color)
                self.ui.colorLineEdit.setText(color.name(QColor.HexRgb))
            elif "disabledColorToolButton" == senderName:
                self.m_button.setDisabledColor(color)
                self.ui.disabledColorLineEdit.setText(color.name(QColor.HexRgb))

        self.setupForm()


class MenuSettingsEditor(Example_QWidget):
    ui_file = "menusettingsform"

    def __init__(self, parent: QWidget = None):
        Example_QWidget.__init__(self, parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        widget = self.ui_parent
        layout.addWidget(widget)

        canvas = QWidget()
        canvas.setStyleSheet("QWidget { background: white }")
        layout.addWidget(canvas)

        # # self.ui.setupUi(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        layout = QVBoxLayout()
        canvas.setLayout(layout)

        layout.addWidget(self.m_menu)
        layout.addSpacing(600)
        layout.setAlignment(self.m_menu, Qt.AlignCenter)

        self.setupForm()

    def setupForm(self) -> void:
        ...

    def updateWidget(self) -> void:
        ...

    def selectColor(self) -> void:
        ...


class ProgressSettingsEditor(Example_QWidget):
    ui_file = "progresssettingsform"

    def __init__(self, parent: QWidget = None):
        Example_QWidget.__init__(self, parent)

        self.m_progress = QtMaterialProgress()

        layout = QVBoxLayout()
        self.setLayout(layout)

        widget = self.ui_parent
        layout.addWidget(widget)

        canvas = QWidget()
        canvas.setStyleSheet("QWidget { background: white }")
        layout.addWidget(canvas)

        # self.ui.setupUi(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        layout = QVBoxLayout()
        canvas.setLayout(layout)
        layout.addWidget(self.m_progress)
        layout.setAlignment(self.m_progress, Qt.AlignCenter)

        self.setupForm()

        self.ui.disabledCheckBox.toggled.connect(self.updateWidget)
        self.ui.progressTypeComboBox.currentIndexChanged.connect(self.updateWidget)
        self.ui.progressSlider.valueChanged.connect(self.updateWidget)
        self.ui.useThemeColorsCheckBox.toggled.connect(self.updateWidget)
        self.ui.progressColorToolButton.pressed.connect(self.selectColor)
        self.ui.backgroundColorToolButton.pressed.connect(self.selectColor)

        self.ui.progressSlider.setRange(0, 100)

    def setupForm(self) -> void:
        typ = self.m_progress.progressType()

        if typ == Material.DeterminateProgress:
            self.ui.progressTypeComboBox.setCurrentIndex(0)

        if typ == Material.IndeterminateProgress:
            self.ui.progressTypeComboBox.setCurrentIndex(1)

        self.ui.disabledCheckBox.setChecked(not self.m_progress.isEnabled())
        self.ui.progressSlider.setValue(self.m_progress.value())
        self.ui.useThemeColorsCheckBox.setChecked(self.m_progress.useThemeColors())

    def updateWidget(self) -> void:
        ind = self.ui.progressTypeComboBox.currentIndex()

        if ind == 0:
            self.m_progress.setProgressType(Material.DeterminateProgress)

        elif ind == 1:
            self.m_progress.setProgressType(Material.IndeterminateProgress)

        self.m_progress.setDisabled(self.ui.disabledCheckBox.isChecked())
        self.m_progress.setValue(self.ui.progressSlider.value())
        self.m_progress.setUseThemeColors(self.ui.useThemeColorsCheckBox.isChecked())

    def selectColor(self) -> void:
        dialog = QColorDialog()
        if dialog.exec():
            color: QColor = dialog.selectedColor()
            senderName: QString = self.sender().objectName()
            if "progressColorToolButton" == senderName:
                self.m_progress.setProgressColor(color)
                self.ui.progressColorLineEdit.setText(color.name(QColor.HexRgb))
            elif "backgroundColorToolButton" == senderName:
                self.m_progress.setBackgroundColor(color)
                self.ui.backgroundColorLineEdit.setText(color.name(QColor.HexRgb))

        self.setupForm()


class RadioButtonSettingsEditor(Example_QWidget):
    ui_file = "radiobuttonsettingsform"

    def __init__(self, parent: QWidget = None):
        Example_QWidget.__init__(self, parent)

        self.m_radioButton1 = QtMaterialRadioButton()
        self.m_radioButton2 = QtMaterialRadioButton()
        self.m_radioButton3 = QtMaterialRadioButton()

        layout = QVBoxLayout()
        self.setLayout(layout)

        widget = self.ui_parent
        layout.addWidget(widget)

        canvas = QWidget()
        canvas.setStyleSheet("QWidget { background: white }")
        layout.addWidget(canvas)

        # self.ui.setupUi(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        self.m_radioButton1.setText("Coffee")
        self.m_radioButton2.setText("Tea")
        self.m_radioButton3.setText("Algebraic Topology")

        layout = QVBoxLayout()
        canvas.setLayout(layout)
        canvas.setMaximumHeight(350)

        buttonWidget = QWidget()
        buttonLayout = QVBoxLayout()
        buttonWidget.setLayout(buttonLayout)

        layout.addWidget(buttonWidget)
        buttonLayout.addWidget(self.m_radioButton1)
        buttonLayout.addWidget(self.m_radioButton2)
        buttonLayout.addWidget(self.m_radioButton3)

        policy = QSizePolicy()
        policy.setHorizontalPolicy(QSizePolicy.Maximum)
        buttonWidget.setSizePolicy(policy)

        layout.setAlignment(Qt.AlignCenter)

        layout.setMargin(0)
        layout.setSpacing(0)

        self.setupForm()

        self.ui.disabledCheckBox.toggled.connect(self.updateWidget)
        self.ui.labelPositionComboBox_2.currentIndexChanged.connect(self.updateWidget)
        self.ui.labelTextLineEdit_2.textChanged.connect(self.updateWidget)
        self.ui.useThemeColorsCheckBox_3.toggled.connect(self.updateWidget)
        self.ui.textColorToolButton_2.pressed.connect(self.selectColor)
        self.ui.disabledColorToolButton_2.pressed.connect(self.selectColor)
        self.ui.checkedColorToolButton_2.pressed.connect(self.selectColor)
        self.ui.uncheckedColorToolButton_2.pressed.connect(self.selectColor)
        self.ui.labelPositionComboBox_2.currentIndexChanged.connect(self.updateWidget)

    def setupForm(self) -> void:
        pos = self.m_radioButton1.labelPosition()

        if pos == QtMaterialCheckable.LabelPositionLeft:
            self.ui.labelPositionComboBox_2.setCurrentIndex(0)
        elif pos == QtMaterialCheckable.LabelPositionRight:
            self.ui.labelPositionComboBox_2.setCurrentIndex(1)

        self.ui.disabledCheckBox.setChecked(not self.m_radioButton1.isEnabled())
        self.ui.labelTextLineEdit_2.setText(self.m_radioButton1.text())
        self.ui.useThemeColorsCheckBox_3.setChecked(
            self.m_radioButton1.useThemeColors()
        )

    def updateWidget(self) -> void:
        index = self.ui.labelPositionComboBox_2.currentIndex()

        if index == 0:
            self.m_radioButton1.setLabelPosition(QtMaterialCheckable.LabelPositionLeft)
            self.m_radioButton2.setLabelPosition(QtMaterialCheckable.LabelPositionLeft)
            self.m_radioButton3.setLabelPosition(QtMaterialCheckable.LabelPositionLeft)

        elif index == 1:
            self.m_radioButton1.setLabelPosition(QtMaterialCheckable.LabelPositionRight)
            self.m_radioButton2.setLabelPosition(QtMaterialCheckable.LabelPositionRight)
            self.m_radioButton3.setLabelPosition(QtMaterialCheckable.LabelPositionRight)

        self.m_radioButton1.setDisabled(self.ui.disabledCheckBox.isChecked())
        self.m_radioButton1.setText(self.ui.labelTextLineEdit_2.text())
        self.m_radioButton1.setUseThemeColors(
            self.ui.useThemeColorsCheckBox_3.isChecked()
        )
        self.m_radioButton2.setUseThemeColors(
            self.ui.useThemeColorsCheckBox_3.isChecked()
        )
        self.m_radioButton3.setUseThemeColors(
            self.ui.useThemeColorsCheckBox_3.isChecked()
        )

    def selectColor(self) -> void:
        dialog = QColorDialog()
        if dialog.exec():
            color: QColor = dialog.selectedColor()
            senderName: QString = self.sender().objectName()
            if "textColorToolButton_2" == senderName:
                self.m_radioButton1.setTextColor(color)
                self.m_radioButton2.setTextColor(color)
                self.m_radioButton3.setTextColor(color)
                self.ui.textColorLineEdit_2.setText(color.name(QColor.HexRgb))
            elif "disabledColorToolButton_2" == senderName:
                self.m_radioButton1.setDisabledColor(color)
                self.m_radioButton2.setDisabledColor(color)
                self.m_radioButton3.setDisabledColor(color)
                self.ui.disabledColorLineEdit_2.setText(color.name(QColor.HexRgb))
            elif "checkedColorToolButton_2" == senderName:
                self.m_radioButton1.setCheckedColor(color)
                self.m_radioButton2.setCheckedColor(color)
                self.m_radioButton3.setCheckedColor(color)
                self.ui.checkedColorLineEdit_2.setText(color.name(QColor.HexRgb))
            elif "uncheckedColorToolButton_2" == senderName:
                self.m_radioButton1.setUncheckedColor(color)
                self.m_radioButton2.setUncheckedColor(color)
                self.m_radioButton3.setUncheckedColor(color)
                self.ui.uncheckedColorLineEdit_2.setText(color.name(QColor.HexRgb))

        self.setupForm()


class RaisedButtonSettingsEditor(FlatButtonSettingsEditor):
    def __init__(self, parent: QWidget):
        FlatButtonSettingsEditor.__init__(
            self, QtMaterialRaisedButton("Rise up"), parent
        )

        self.ui.transparentCheckBox.setDisabled(true)
        self.ui.defaultPresetPushButton.setDisabled(true)
        self.ui.checkablePresetPushButton.setDisabled(true)


class ScrollBarSettingsEditor(Example_QWidget):
    ui_file = "scrollbarsettingsform"

    def __init__(self, parent: QWidget = None):
        Example_QWidget.__init__(self, parent)

        self.m_verticalScrollbar = QtMaterialScrollBar()
        self.m_horizontalScrollbar = QtMaterialScrollBar()

        layout = QVBoxLayout()
        self.setLayout(layout)

        widget = self.ui_parent
        layout.addWidget(widget)

        canvas = QWidget()
        canvas.setStyleSheet("QWidget { background: white }")
        layout.addWidget(canvas)

        # self.ui.setupUi(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        layout = QVBoxLayout()
        canvas.setLayout(layout)
        canvas.setMaximumHeight(400)

        edit = QTextEdit()
        edit.setText(
            "<p>The distinction between the subjects of syntax and semantics has its origin in the study of natural languages.</p><p>The distinction between the subjects of syntax and semantics has its origin in the study of natural languages.</p><p>The distinction between the subjects of syntax and semantics has its origin in the study of natural languages.</p><p>The distinction between the subjects of syntax and semantics has its origin in the study of natural languages.</p><p>The distinction between the subjects of syntax and semantics has its origin in the study of natural languages.</p><p>The distinction between the subjects of syntax and semantics has its origin in the study of natural languages.</p><p>The distinction between the subjects of syntax and semantics has its origin in the study of natural languages.</p><p>The distinction between the subjects of syntax and semantics has its origin in the study of natural languages.</p>"
        )
        edit.setLineWrapMode(QTextEdit.NoWrap)
        edit.update()
        edit.setMaximumHeight(200)

        edit.setVerticalScrollBar(self.m_verticalScrollbar)
        edit.setHorizontalScrollBar(self.m_horizontalScrollbar)

        # m_verticalScrollbar.setHideOnMouseOut(false)

        # m_horizontalScrollbar.setHideOnMouseOut(false)
        self.m_horizontalScrollbar.setOrientation(Qt.Horizontal)

        layout.addWidget(edit)
        layout.setAlignment(edit, Qt.AlignHCenter)

        self.setupForm()

    def setupForm(self) -> void:
        ...

    def updateWidget(self) -> void:
        ...


class SliderSettingsEditor(Example_QWidget):
    ui_file = "slidersettingsform"

    def __init__(self, parent: QWidget = None):
        Example_QWidget.__init__(self, parent)

        self.m_slider = QtMaterialSlider()

        layout = QVBoxLayout()
        self.setLayout(layout)

        widget = self.ui_parent
        layout.addWidget(widget)

        canvas = QWidget()
        canvas.setStyleSheet("QWidget { background: white }")
        layout.addWidget(canvas)

        # self.ui.setupUi(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        layout = QVBoxLayout()
        canvas.setLayout(layout)
        canvas.setMaximumHeight(300)
        layout.addWidget(self.m_slider)
        layout.setAlignment(self.m_slider, Qt.AlignHCenter)

        self.setupForm()

        self.ui.disabledCheckBox.toggled.connect(self.updateWidget)
        self.ui.valueLineEdit.textChanged.connect(self.updateWidget)
        self.ui.orientationComboBox.currentIndexChanged.connect(self.updateWidget)
        self.ui.invertedCheckBox.toggled.connect(self.updateWidget)

        self.m_slider.valueChanged.connect(self.setupForm)

    def setupForm(self) -> void:
        ori = self.m_slider.orientation()

        if ori == Qt.Horizontal:
            self.ui.orientationComboBox.setCurrentIndex(0)

        elif ori == Qt.Vertical:
            self.ui.orientationComboBox.setCurrentIndex(1)

        self.ui.disabledCheckBox.setChecked(not self.m_slider.isEnabled())
        self.ui.valueLineEdit.setText(str(self.m_slider.value()))
        self.ui.invertedCheckBox.setChecked(self.m_slider.invertedAppearance())

    def updateWidget(self) -> void:
        ind = self.ui.orientationComboBox.currentIndex()

        if ind == 0:
            self.m_slider.setOrientation(Qt.Horizontal)

        elif ind == 1:
            self.m_slider.setOrientation(Qt.Vertical)

        self.m_slider.setDisabled(self.ui.disabledCheckBox.isChecked())
        self.m_slider.setValue(int(self.ui.valueLineEdit.text()))
        self.m_slider.setInvertedAppearance(self.ui.invertedCheckBox.isChecked())


class SnackbarSettingsEditor(Example_QWidget):
    ui_file = "snackbarsettingsform"

    def __init__(self, parent: QWidget = None):
        Example_QWidget.__init__(self, parent)

        self.m_snackbar = QtMaterialSnackbar()

        layout = QVBoxLayout()
        self.setLayout(layout)

        widget = self.ui_parent
        layout.addWidget(widget)

        canvas = QWidget()
        canvas.setStyleSheet("QWidget { background: white }")
        layout.addWidget(canvas)

        # self.ui.setupUi(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        layout = QVBoxLayout()
        canvas.setLayout(layout)
        canvas.setMaximumHeight(300)

        self.m_snackbar.setParent(self)

        self.setupForm()

        self.ui.showSnackbarButton.pressed.connect(self.showSnackbar)

    def setupForm(self) -> void:
        ...

    def updateWidget(self) -> void:
        ...

    def selectColor(self) -> void:
        ...

    def showSnackbar(self):
        self.m_snackbar.addMessage(QString("Snack attacknot "))


class TabsSettingsEditor(Example_QWidget):
    ui_file = "tabssettingsform"

    def __init__(self, parent: QWidget = None):
        Example_QWidget.__init__(self, parent)

        self.m_tas = QtMaterialTabs()

        layout = QVBoxLayout()
        self.setLayout(layout)

        widget = self.ui_parent
        layout.addWidget(widget)

        canvas = QWidget()
        canvas.setStyleSheet("QWidget { background: white }")
        layout.addWidget(canvas)

        # self.ui.setupUi(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        layout = QVBoxLayout()
        canvas.setLayout(layout)
        canvas.setMaximumHeight(300)
        layout.addWidget(self.m_tabs)
        layout.setAlignment(self.m_tabs, Qt.AlignHCenter)

        self.m_tabs.addTab("Media")
        self.m_tabs.addTab("Playback")
        self.m_tabs.addTab("Audio")
        self.m_tabs.addTab("Video")
        self.m_tabs.addTab("Tools")

        self.m_tabs.setMinimumWidth(700)

        self.setupForm()

    def setupForm(self) -> void:
        ...

    def updateWidget(self) -> void:
        ...

    def selectColor(self) -> void:
        ...


class TextFieldSettingsEditor(Example_QWidget):
    ui_file = "textfieldsettingsform"

    def __init__(self, parent: QWidget = None):
        Example_QWidget.__init__(self, parent)

        self.m_textField = QtMaterialTextField()

        layout = QVBoxLayout()
        self.setLayout(layout)

        widget = self.ui_parent
        layout.addWidget(widget)

        canvas = QWidget()
        canvas.setStyleSheet("QWidget { background: white }")
        layout.addWidget(canvas)

        # self.ui.setupUi(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        layout = QVBoxLayout()
        canvas.setLayout(layout)
        layout.addWidget(self.m_textField)
        layout.setAlignment(self.m_textField, Qt.AlignCenter)

        self.m_textField.setLabel("Wat is self")
        self.m_textField.setMinimumWidth(250)

        self.setupForm()

        self.ui.disabledCheckBox.toggled.connect(self.updateWidget)
        self.ui.textLineEdit.textChanged.connect(self.updateWidget)
        self.ui.placeholderLineEdit.textChanged.connect(self.updateWidget)
        self.ui.labelCheckBox.toggled.connect(self.updateWidget)
        self.ui.labelTextLineEdit.textChanged.connect(self.updateWidget)
        self.ui.useThemeColorsCheckBox.toggled.connect(self.updateWidget)
        self.ui.textColorToolButton.pressed.connect(self.selectColor)
        self.ui.inkColorToolButton.pressed.connect(self.selectColor)
        self.ui.inputLineColorToolButton.pressed.connect(self.selectColor)
        self.ui.labelColorToolButton.pressed.connect(self.selectColor)
        self.ui.inputLineCheckBox.toggled.connect(self.setShowInputLine)

        self.m_textField.textChanged.connect(self.setupForm)

    def setupForm(self) -> void:
        self.ui.disabledCheckBox.setChecked(not self.m_textField.isEnabled())
        self.ui.textLineEdit.setText(self.m_textField.text())
        self.ui.placeholderLineEdit.setText(self.m_textField.placeholderText())
        self.ui.labelCheckBox.setChecked(self.m_textField.hasLabel())
        self.ui.labelTextLineEdit.setText(self.m_textField.label())
        self.ui.useThemeColorsCheckBox.setChecked(self.m_textField.useThemeColors())
        self.ui.inputLineCheckBox.setChecked(self.m_textField.hasInputLine())

    def updateWidget(self) -> void:
        self.m_textField.setDisabled(self.ui.disabledCheckBox.isChecked())
        self.m_textField.setText(self.ui.textLineEdit.text())
        self.m_textField.setPlaceholderText(self.ui.placeholderLineEdit.text())
        self.m_textField.setLabel(self.ui.labelTextLineEdit.text())
        self.m_textField.setShowLabel(self.ui.labelCheckBox.isChecked())
        self.m_textField.setUseThemeColors(self.ui.useThemeColorsCheckBox.isChecked())
        self.m_textField.setShowInputLine(self.ui.inputLineCheckBox.isChecked())

    def selectColor(self) -> void:
        dialog = QColorDialog()
        if dialog.exec():
            color: QColor = dialog.selectedColor()
            senderName: QString = self.sender().objectName()
            if "textColorToolButton" == senderName:
                self.m_textField.setTextColor(color)
                self.ui.textColorLineEdit.setText(color.name(QColor.HexRgb))
            elif "inkColorToolButton" == senderName:
                self.m_textField.setInkColor(color)
                self.ui.inkColorLineEdit.setText(color.name(QColor.HexRgb))
            elif "inputLineColorToolButton" == senderName:
                self.m_textField.setInputLineColor(color)
                self.ui.inputLineColorLineEdit.setText(color.name(QColor.HexRgb))
            elif "labelColorToolButton" == senderName:
                self.m_textField.setLabelColor(color)
                self.ui.labelColorLineEdit.setText(color.name(QColor.HexRgb))

        self.setupForm()

    def setShowInputLine(self) -> void:
        self.m_textField.setShowInputLine(self.ui.inputLineCheckBox.isChecked())


class ToggleSettingsEditor(Example_QWidget):
    ui_file = "togglesettingsform"

    def __init__(self, parent: QWidget = None):
        Example_QWidget.__init__(self, parent)

        self.m_toggle = QtMaterialToggle()

        layout = QVBoxLayout()
        self.setLayout(layout)

        widget = self.ui_parent
        layout.addWidget(widget)

        canvas = QWidget()
        canvas.setStyleSheet("QWidget { background: white }")
        layout.addWidget(canvas)

        # self.ui.setupUi(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        self.m_toggle.setOrientation(Qt.Vertical)

        layout = QVBoxLayout()
        canvas.setLayout(layout)
        layout.addWidget(self.m_toggle)
        layout.setAlignment(self.m_toggle, Qt.AlignCenter)

        self.setupForm()

        self.ui.disabledCheckBox.toggled(self.updateWidget)
        self.ui.checkedCheckBox.toggled(self.updateWidget)
        self.ui.orientationComboBox.currentIndexChanged(self.updateWidget)
        self.ui.useThemeColorsCheckBox.toggled(self.updateWidget)
        self.ui.disabledColorToolButton.pressed(self.selectColor)
        self.ui.activeColorToolButton.pressed(self.selectColor)
        self.ui.inactiveColorToolButton.pressed(self.selectColor)
        self.ui.trackColorToolButton.pressed(self.selectColor)

        self.m_toggle.toggled.connect(self.setupForm)

    def setupForm(self) -> void:
        ori = self.m_toggle.orientation()

        if ori == Qt.Horizontal:
            self.ui.orientationComboBox.setCurrentIndex(0)

        elif ori == Qt.Vertical:
            self.ui.orientationComboBox.setCurrentIndex(1)

        self.ui.disabledCheckBox.setChecked(not self.m_toggle.isEnabled())
        self.ui.checkedCheckBox.setChecked(self.m_toggle.isChecked())
        self.ui.useThemeColorsCheckBox.setChecked(self.m_toggle.useThemeColors())

    def updateWidget(self) -> void:
        ind = self.ui.orientationComboBox.currentIndex()

        if ind == 0:
            self.m_toggle.setOrientation(Qt.Horizontal)

        elif ind == 1:
            self.m_toggle.setOrientation(Qt.Vertical)

        self.m_toggle.setDisabled(self.ui.disabledCheckBox.isChecked())
        self.m_toggle.setChecked(self.ui.checkedCheckBox.isChecked())
        self.m_toggle.setUseThemeColors(self.ui.useThemeColorsCheckBox.isChecked())

    def selectColor(self) -> void:
        dialog = QColorDialog()
        if dialog.exec():
            color: QColor = dialog.selectedColor()
            senderName: QString = self.sender().objectName()
            if "disabledColorToolButton" == senderName:
                self.m_toggle.setDisabledColor(color)
                self.ui.disabledColorLineEdit.setText(color.name(QColor.HexRgb))
            elif "activeColorToolButton" == senderName:
                self.m_toggle.setActiveColor(color)
                self.ui.activeColorLineEdit.setText(color.name(QColor.HexRgb))
            elif "inactiveColorToolButton" == senderName:
                self.m_toggle.setInactiveColor(color)
                self.ui.inactiveColorLineEdit.setText(color.name(QColor.HexRgb))
            elif "trackColorToolButton" == senderName:
                self.m_toggle.setTrackColor(color)
                self.ui.trackColorLineEdit.setText(color.name(QColor.HexRgb))

        self.setupForm()
