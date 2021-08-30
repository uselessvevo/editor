#   Copyright @ Crab Dudes Developers
#   Licensed under the terms of the MIT license
#   File dialoglayout.py - 02.03.2021, 16:01

# Qt
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout

# Managers
from toolkit.system.manager import System


class DialogLayout(QHBoxLayout):

    def __init__(self, parent=None, props=None):
        super(DialogLayout, self).__init__(parent)

        self.trans = System.objects.get('TranslationsManager')

        self.helpButton = QPushButton(parent)
        self.helpButton.setText('?')
        self.helpButton.setObjectName('helpButton')

        self.okButton = QPushButton(parent)
        self.okButton.setFocus()
        self.okButton.setText(self.trans('Shared.Ok'))

        self.cancelButton = QPushButton(parent)
        self.cancelButton.setText(self.trans('Shared.Cancel'))

        # Add horizontal and vertical layouts
        vlButtons = QVBoxLayout()
        hlButtons = QHBoxLayout()

        # Shrink 'em
        vlButtons.addStretch()
        hlButtons.addStretch()

        # Add widgets to layouts with some horizontal space
        hlButtons.addWidget(self.helpButton)
        hlButtons.addStretch(1)
        hlButtons.addWidget(self.okButton)
        hlButtons.addWidget(self.cancelButton)
        vlButtons.addLayout(hlButtons)
        self.addLayout(vlButtons)

    def setHelp(self, hid):
        """
        Override this function
        Args:
            hid (any) - help id
        """
        raise NotImplementedError('method "setHelp" must be implemented')
