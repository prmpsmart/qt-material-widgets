from . import examples_resources
from .mainwindow import *

def main():
    a = QApplication([])

    window = QWidget()

    # completed
    # window = AppBarSettingsEditor()
    # window = AvatarSettingsEditor()
    # window = BadgeSettingsEditor()
    # window = CircularProgressSettingsEditor()

    # uncompleted or error
    # window = AutoCompleteSettingsEditor()
    # window = CheckBoxSettingsEditor()

    # testing
    window = DialogSettingsEditor()

    # window = DrawerSettingsEditor()
    # window = FloatingActionButtonSettingsEditor()
    # window = FlatButtonSettingsEditor()
    # window = IconButtonSettingsEditor()
    # window = MenuSettingsEditor()
    # window = ProgressSettingsEditor()
    # window = RadioButtonSettingsEditor()
    # window = RaisedButtonSettingsEditor()
    # window = ScrollBarSettingsEditor()
    # window = SliderSettingsEditor()
    # window = SnackbarSettingsEditor()
    # window = TabsSettingsEditor()
    # window = TextFieldSettingsEditor()
    # window = ToggleSettingsEditor()
    
    # window = MainWindow()
    window.show()
    a.exec_()


