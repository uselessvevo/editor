"""
Toolbar API
"""
from PyQt5 import QtGui
from PyQt5 import QtWidgets


def createButton(*args, **kwargs):
    return QtWidgets.QPushButton(*args, **kwargs)
