#   Copyright @ Crab Dudes Developers
#   Licensed under the terms of the MIT license
#   File itemwidget.py - 27.01.2021, 19:31

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QSpacerItem
# from PyQt5.QtCore import Qt, QEvent


class CustomItemWidget(QWidget):
    def __init__(self, parent):
        super(CustomItemWidget, self).__init__()
        self._parent = parent

        self.answerButton = QPushButton(self._parent)
        self.answerButton.setWindowIcon('icons/24x24/Chat.png')
        self.answerButton.setObjectName('ControlButton')

        self.favButton = QPushButton(self._parent)
        self.favButton.setWindowIcon('icons/24x24/Favourite.png')
        self.favButton.setObjectName('ControlButton')

        menuButton = QPushButton(self._parent)
        menuButton.setWindowIcon('icons/24x24/Menu.png')
        menuButton.setObjectName('ControlButton')

        vlTopControls = QHBoxLayout()
        vlTopControls.addWidget(self.answerButton)
        vlTopControls.addWidget(self.favButton)
        vlTopControls.addSpacerItem(QSpacerItem(100, 0, QSizePolicy.Expanding))

        self.labelTitle = QLabel()
        self.descriptionTitle = QLabel()
        self.descriptionTitle.setWordWrap(True)

        vlTextContent = QVBoxLayout()
        vlTextContent.addLayout(vlTopControls)
        vlTextContent.addWidget(self.labelTitle)
        vlTextContent.addWidget(self.descriptionTitle)

        hlMain = QHBoxLayout()
        hlMain.addLayout(vlTextContent, 0)
        self.setLayout(hlMain)
        self.installEventFilter(self)

    def setTitle(self, text):
        text = f'{text[:50]} ...'
        self.labelTitle.setText(text)

    def setDescription(self, text):
        self.descriptionTitle.setText(text)

    # def eventFilter(self, object, event, *widgets):
    #     """
    #     Args:
    #         object (object) - object ot hide
    #         event (QEvent)
    #         widgets ([QWidget])
    #     """
    #     if event.type() == QEvent.Enter:
    #         self.favButton.setVisible(True)
    #         self.answerButton.setVisible(True)
    #
    #     elif event.type() == QEvent.Leave:
    #         self.favButton.setVisible(False)
    #         self.answerButton.setVisible(False)
    #
    #     return False
