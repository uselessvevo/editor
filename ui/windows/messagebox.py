#   Copyright @ Crab Dudes Developers
#   Licensed under the terms of the MIT license
#   File messagebox.py - 02.03.2021, 16:01
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton

from toolkit.system.manager import System


class MessageBox(QMessageBox):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.trans = System.get_object('TranslationManager')

        self.setStyleSheet('QLabel{min-width: 300px; min-height: 50}')
        self.setWindowTitle(self.trans('Shared.Exit'))  # Exit
        self.setText(self.trans('Shared.ExitMessage'))  # Are you sure you want to quit?

        self.yesButton = QPushButton()
        self.yesButton.setText(self.trans('Shared.Yes'))

        self.noButton = QPushButton()
        self.noButton.setText(self.trans('Shared.No'))

        self.addButton(self.yesButton, QMessageBox.YesRole)
        self.addButton(self.noButton, QMessageBox.NoRole)
        self.setDefaultButton(self.noButton)

        self.exec_()
