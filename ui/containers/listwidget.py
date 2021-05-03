"""
Table item but it's so fancy. I guess.
"""
#   Copyright @ Crab Dudes Developers
#   Licensed under the terms of the MIT license
#   File listwidget.py - 27.01.2021, 19:31

from PyQt5.QtWidgets import QListWidget


class CustomListWidget(QListWidget):
    def __init__(self, parent=None):
        super(CustomListWidget, self).__init__(parent)

    def addToList(self, item):
        self._listWidget.addItem(item)
        self._listWidget.setItemWidget(item, self)
