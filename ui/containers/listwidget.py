"""
Custom QListWidget
"""
from PyQt5.QtWidgets import QListWidget


class CustomListWidget(QListWidget):
    def __init__(self, parent=None):
        super(CustomListWidget, self).__init__(parent)

    def addToList(self, item):
        self._listWidget.addItem(item)
        self._listWidget.setItemWidget(item, self)
