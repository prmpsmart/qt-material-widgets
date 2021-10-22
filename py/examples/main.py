from . import examples_resources
from .mainwindow import *

def main():
    a = QApplication([])

    window = MainWindow()
    window.show()

    a.exec_()
