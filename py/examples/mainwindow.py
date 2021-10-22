from .examples import *


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget = None):
        QMainWindow.__init__(self, parent)

        widget = QWidget()
        layout = QHBoxLayout(widget)


        self.stack = QStackedLayout()

        self.list = QListWidget()
        self.list.currentChanged = self.currentItemChanged

        layout.addWidget(self.list)
        layout.addLayout(self.stack)

        layout.setStretch(1, 2)

        self.setCentralWidget(widget)
        self.setMinimumSize(800, 800)

        appBar = AppBarSettingsEditor, "App Bar"
        autocomplete = AutoCompleteSettingsEditor, "Auto Complete"
        avatar = AvatarSettingsEditor, "Avatar"
        badge = BadgeSettingsEditor, "Badge"
        checkbox = CheckBoxSettingsEditor, "CheckBox"
        circularProgress = CircularProgressSettingsEditor, "Circular Progress"
        dialog = DialogSettingsEditor, "Dialog"
        drawer = DrawerSettingsEditor, "Drawer"
        fab = FloatingActionButtonSettingsEditor, "Floating Action Button"
        flatButton = FlatButtonSettingsEditor, "Flat Button"
        iconButton = IconButtonSettingsEditor, "Icon Button"
        menu = MenuSettingsEditor, "Menu"
        progress = ProgressSettingsEditor, "Progress"
        radioButton = RadioButtonSettingsEditor, "Radio Button"
        raisedButton = RaisedButtonSettingsEditor, "Raised Button"
        scrollBar = ScrollBarSettingsEditor, "Scroll Bar"
        slider = SliderSettingsEditor, "Slider"
        snackbar = SnackbarSettingsEditor, "Snackbar"
        tabs = TabsSettingsEditor, "Tabs"
        textField = TextFieldSettingsEditor, "Text Field"
        toggle = ToggleSettingsEditor, "Toggle"

        apps = (
            appBar,
            autocomplete,
            avatar,
            badge,
            checkbox,
            circularProgress,
            dialog,
            drawer,
            fab,
            flatButton,
            iconButton,
            menu,
            progress,
            radioButton,
            raisedButton,
            scrollBar,
            slider,
            snackbar,
            tabs,
            textField,
            toggle,
        )

        err = [20]

        for n in err:
            self.setup(apps[n - 1])

        self.list.setCurrentRow(0)

    def currentChanged(self, current: QModelIndex, previous: QModelIndex):
        self.stack.setCurrentIndex(self.list.currentRow())

    def currentItemChanged(self, current: QListWidgetItem, previous: QListWidgetItem):
        self.stack.setCurrentIndex(self.list.currentRow())

    def setup(self, tup: tuple):
        klass, name = tup
        wid = klass()

        self.stack.addWidget(wid)
        self.list.addItem(name)

