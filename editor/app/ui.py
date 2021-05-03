import os
from functools import lru_cache

from PyQt5 import QtGui
from PyQt5 import QtWidgets

from toolkit.managers import System
from toolkit.managers import getFile
from ui.windows.window import BaseWindow

from components.editor.ui import TextArea
from components.console.ui import Console
from components.toolbar.ui import Toolbar


class Main(BaseWindow, QtWidgets.QMainWindow):

    defaultMinSize = (600, 350)
    defaultPosition = (150, 150)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setMinSize()
        self.setMaxSize()
        self.moveToCenter()

        self.initMain()
        self.initToolbar()
        self.initTextEditor()
        self.initGrid()

    def initGrid(self):
        self.grid.addWidget(self.toolBar, 0, 0)
        self.grid.addWidget(self.textArea, 1, 0)

    def initMain(self):
        self.setWindowTitle(f'Redaktor - {os.getcwd()}')
        self.setWindowIcon(QtGui.QIcon(getFile('shared/icons/magic.svg')))

        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)
        self.grid = QtWidgets.QGridLayout(self.centralWidget)

    def initToolbar(self) -> None:
        self.toolBar = Toolbar()

    def initTextEditor(self) -> None:
        self.textArea = TextArea()

    def openFiles(self) -> None:
        fileDialog = QtWidgets.QFileDialog(self)
        fileDialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog)

        result, folder = fileDialog.getOpenFileNames(
            parent=self,
            caption=self.tr('Editor.OpenFiles'),
            directory=System.config.get('files.last_opened_folder', os.path.expanduser('~')),
            filter=self.getFileFormats()
        )
        System.config.set('files.last_opened_folder', folder)
        System.config.save('files')

        if result:
            print(result)

    def openFolder(self) -> None:
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            parent=self,
            caption=self.tr('Editor.OpenFolder'),
            directory=System.config.get('files.last_opened_folder', os.path.expanduser('~'))
        )
        System.config.set('files.last_opened_folder', folder)
        if folder:
            print(os.listdir(folder))

    @lru_cache(None)
    def getFileFormats(self) -> str:
        formats = System.config.get('formats')
        result = ';;'.join(
            '{}{}'.format(self.tr(key), val) for (key, val)
            in formats.items() if key != 'formats'
        )
        return result + ';;'.join(formats)

    def onCloseEventAccept(self) -> None:
        pass

    def onCloseEventIgnore(self) -> None:
        pass

    def onCloseEventDefault(self) -> None:
        pass

    def closeEvent(self, event) -> None:
        pass
