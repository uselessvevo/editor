from typing import Tuple

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from toolkit.helpers.os import getScreenInfo

from ui.abstracts.window import AbstractWindow
from ui.windows.messagebox import MessageBox


class BaseWindowMixin(AbstractWindow):
    defaultMinSize: Tuple[int, int] = None
    defaultPosition: Tuple[int, int] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__config = kwargs.get('config', {})

    def setMinSize(self, w: int = None, h: int = None) -> None:
        if not all((w, h)):
            w, h = self.defaultMinSize

        self.setMinimumSize(QtCore.QSize(w, h))

    def setMaxSize(self, w: int = None, h: int = None) -> None:
        screen = getScreenInfo()
        if not all((w, h)) or (w, h) > screen:
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
        notification = self.__config.get('ui.show_close_notification', False)
        if notification:
            message = MessageBox(self)

            if message.clickedButton() == message.yesButton:
                self.onCloseEventAccept()
                event.accept()

            else:
                self.onCloseEventIgnore()
                event.ignore()

        self.onCloseEventDefault()
