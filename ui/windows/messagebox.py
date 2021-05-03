#   Copyright @ Crab Dudes Developers
#   Licensed under the terms of the MIT license
#   File messagebox.py - 02.03.2021, 16:01

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton


class MessageBox(QMessageBox):

    def __init__(self, parent=None):
        super(MessageBox, self).__init__(parent)
        self.setStyleSheet('QLabel{min-width: 300px; min-height: 50}')
        self.setWindowTitle(self.tr('shared.Exit'))  # Exit
        self.setText(self.tr('shared.ExitMessage'))  # Are you sure you want to quit?

        self.yesButton = QPushButton()
        self.yesButton.setText(self.tr('shared.Yes'))

        self.noButton = QPushButton()
        self.noButton.setText(self.tr('shared.No'))

        self.addButton(self.yesButton, QMessageBox.YesRole)
        self.addButton(self.noButton, QMessageBox.NoRole)
        self.setDefaultButton(self.noButton)

        self.exec_()
