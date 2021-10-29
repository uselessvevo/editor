from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets


def createSplashScreen(path: str) -> QtWidgets.QSplashScreen:
    """ Create splash screen. Forked from Spyder: spyder/app/utils.py """
    splashPix = QtGui.QPixmap(path)
    splashPix = splashPix.scaled(720, 480)
    splash = QtWidgets.QSplashScreen(splashPix, QtCore.Qt.WindowStaysOnTopHint)

    splashFont = splash.font()
    splashFont.setPixelSize(14)
    splash.setFont(splashFont)

    return splash
