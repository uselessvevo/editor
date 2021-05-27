#   Copyright @ Crab Dudes Developers
#   Licensed under the terms of the MIT license
#   File errorwindow.py - 02.03.2021, 16:01

# Standard libraries
import sys

# Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QErrorMessage

from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QPushButton

from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QStyle


def ErrorWindow(message):
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)

    app.setWindowIcon(app.style().standardIcon(QStyle.SP_MessageBoxWarning))
    window = QErrorMessage()
    window.finished.connect(lambda e: app.quit)
    window.resize(450, 300)

    # window.setWindowFlags(~Qt.WindowContextHelpButtonHint)
    window.setWindowTitle('Error')

    window.findChild(QLabel, '').setVisible(False)
    window.findChild(QCheckBox, '').setVisible(False)
    window.findChild(QPushButton, '').setVisible(False)
    window.showMessage(message)

    sys.exit(app.exec_())


def exceptionhook(type_, value, traceback):
    sys._excepthook = sys.excepthook
    ErrorWindow(f'{type_} {value} {traceback}')
    sys._excepthook(type_, value, traceback)
    sys.exit(1)
