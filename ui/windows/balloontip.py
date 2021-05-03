#   Copyright @ Crab Dudes Developers
#   Licensed under the terms of the MIT license
#   File balloontip.py - 27.01.2021, 19:31
from cloudykit.managers import tr

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QSystemTrayIcon


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)
        traySignal = "activated(QSystemTrayIcon::ActivationReason)"
        self.connect()
        self.connect(self, QtCore.PYQT_SIGNAL(traySignal), self._activateRoutine)
        self.balloon = QBalloonWidget('BalloonWidget')

    def _activateRoutine(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.balloon.show(self.geometry())


class QBalloonWidget(QWidget):
    def __init__(self, name, parent=None):
        super().__init__(parent=parent, flags=Qt.Popup)

        self.name = name
        self.offsetX = 10
        self.offsetY = 10
        self.outInfo = QLabel(self)

        self.setStyleSheet("QWidget {border:5px solid rgb(170, 170, 255);}")

    def show(self, coord):
        richText = tr('Any text with Rich Format')
        self.outInfo.setText(richText)
        self.outInfo.show()
        self.adjustSize()

        origin = QDesktopWidget().availableGeometry().bottomRight()

        if coord.y() < origin.y()/2:
            moveY = coord.bottomLeft().y() + self.offsetY
        else:
            moveY = coord.topLeft().y() - (self.height() + self.offsetY)

        if coord.x() + self.width() + self.offsetX >= origin.x():
            moveX = origin.x() - (self.width() + self.offsetX)
        else:
            moveX = coord.x()

        self.move(moveX,moveY)
        self.setVisible(True)

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def mousePressEvent(self, event):
        self.close()
