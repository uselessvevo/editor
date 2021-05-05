import os
from functools import lru_cache

from PyQt5 import QtGui, Qt
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from toolkit.managers import System
from toolkit.managers import getFile
from ui.windows.window import BaseWindow

from components.editor.ui import Editor
from components.console.ui import Console
from components.workbench.ui import Workbench


class Main(BaseWindow, QtWidgets.QMainWindow):

    defaultMinSize = (1020, 670)
    defaultPosition = (150, 150)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.initMain()
        self.initLayout()
        self.initMenu()
        self.initTextEditor()
        self.initWorkbench()
        self.initStatusBar()

    def initMain(self):
        self.setWindowTitle(f'Redaktor - {os.getcwd()}')
        self.setWindowIcon(QtGui.QIcon(getFile('shared/icons/magic.svg')))
        self.setMinSize()
        self.moveToCenter()

    def initLayout(self):
        self.mainHBox = QtWidgets.QHBoxLayout()
        # self.toolBarHBox = QtWidgets.QHBoxLayout()
        self.workbenchVBox = QtWidgets.QVBoxLayout()
        self.treeViewVBox = QtWidgets.QVBoxLayout()
        self.editorHBox = QtWidgets.QHBoxLayout()

        self.mainHBox.addLayout(self.workbenchVBox)
        self.mainHBox.addLayout(self.treeViewVBox)
        # self.mainHBox.addLayout(self.toolBarHBox)
        self.mainHBox.addLayout(self.editorHBox)

        self.setLayout(self.mainHBox)

        widget = QtWidgets.QWidget()
        widget.setLayout(self.mainHBox)
        self.setCentralWidget(widget)

    def initMenu(self):
        self.fileMenu = self.menuBar().addMenu('&File')
        # self.fileMenu.addAction()

    def initWorkbench(self):
        self.workbench = Workbench()
        self.addToolBar(Qt.LeftToolBarArea, self.workbench)

    def initTextEditor(self) -> None:
        self.editor = Editor()
        self.editorHBox.addWidget(self.editor)

    def initStatusBar(self):
        self.statusBar = QtWidgets.QStatusBar()
        self.statusBar.insertPermanentWidget(0, QtWidgets.QWidget())
        self.setStatusBar(self.statusBar)

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
