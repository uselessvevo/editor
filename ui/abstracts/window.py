#   Copyright @ Crab Dudes Developers
#   Licensed under the terms of the MIT license
#   File window.py - 27.01.2021, 19:31
import abc
from typing import Tuple


class AbstractWindow:

    defaultMinSize: Tuple[int, int] = None
    defaultPosition: Tuple[int, int] = None

    @abc.abstractmethod
    def setMinSize(self, w: int, h: int) -> None:
        """ Set minimum window size """

    @abc.abstractmethod
    def setMaxSize(self, w: int, h: int) -> None:
        """ Set maximum window size """

    @abc.abstractmethod
    def onCloseEventAccept(self) -> None:
        """ After "Accept" button was pressed """

    @abc.abstractmethod
    def onCloseEventIgnore(self) -> None:
        """ After "Cancel" button was pressed """

    @abc.abstractmethod
    def onCloseEventDefault(self) -> None:
        """ After window was closed """

    @abc.abstractmethod
    def closeEvent(self, event) -> None:
        """ Close event handler """
