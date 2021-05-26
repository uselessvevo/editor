from typing import Tuple

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from toolkit.managers import System
from toolkit.utils.os import getScreenInfo
from ui.abstracts.window import AbstractWindow
from ui.windows.messagebox import MessageBox


class BaseWindow(AbstractWindow):

    defaultMinSize: Tuple[int, int] = None
    defaultPosition: Tuple[int, int] = None

    def setMinSize(self, w: int = None, h: int = None) -> None:
        if not w and not h:
            w, h = self.defaultMinSize

        self.setMinimumSize(QtCore.QSize(w, h))

    def setMaxSize(self, w: int = None, h: int = None) -> None:
        screen = getScreenInfo()
        if (not w or not h) or (w, h) > screen:
            w, h = screen

        self.setMaximumSize(QtCore.QSize(w, h))

    def moveToCenter(self):
        rect = self.frameGeometry()
        center = QtWidgets.QDesktopWidget().availableGeometry().center()
        rect.moveCenter(center)
        self.move(rect.topLeft())

    def onCloseEventAccept(self) -> None:
        """ After "Accept" button was pressed """

    def onCloseEventIgnore(self) -> None:
        """ After "Cancel" button was pressed """

    def onCloseEventDefault(self) -> None:
        """ After window was closed """

    def closeEvent(self, event) -> None:
        notification = System.config.get('configs.ui.show_close_dialog', True)
        if notification:
            message = MessageBox(self)
            if message.clickedButton() == message.yesButton:
                self.onCloseEventAccept()
                event.accept()
            else:
                self.onCloseEventIgnore()
                event.ignore()

        self.onCloseEventDefault()
