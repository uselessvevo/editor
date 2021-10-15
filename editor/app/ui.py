import os
from functools import lru_cache

from PyQt5 import QtGui, Qt
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from toolkit.managers import getFile
from toolkit.managers.system.manager import System

from ui.windows.window import BaseWindowMixin

from components.editor.ui import Editor
from components.console.ui import Console
from components.workbench.ui import Workbench


class MainUI(BaseWindowMixin, QtWidgets.QMainWindow):
    defaultMinSize = (1020, 670)
    defaultPosition = (150, 150)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.trans = System.get_object('LocalesManager')

        self.initMain()
        self.initLayout()
        self.initMenu()
        self.initTextEditor()
        self.initWorkbench()
        self.initStatusBar()

    def initMain(self):
        self.setWindowTitle(f'Editor - {os.getcwd()}')
        self.setWindowIcon(QtGui.QIcon(getFile('shared/icons/magic.svg')))
        self.setMinSize()
        self.moveToCenter()

    def initLayout(self):
        self.mainHBox = QtWidgets.QHBoxLayout()
        self.toolBarHBox = QtWidgets.QHBoxLayout()
        self.workbenchVBox = QtWidgets.QVBoxLayout()
        self.treeViewVBox = QtWidgets.QVBoxLayout()
        self.editorHBox = QtWidgets.QHBoxLayout()

        self.dock = QtWidgets.QDockWidget('Console', self)
        # self.dock.setFloating(True)

        self.mainHBox.addLayout(self.workbenchVBox)
        self.mainHBox.addLayout(self.treeViewVBox)
        self.mainHBox.addLayout(self.editorHBox)
        self.setLayout(self.mainHBox)

        self.mainHBox.setContentsMargins(0, 0, 0, 0)
        self.mainHBox.setSpacing(20)

        widget = QtWidgets.QWidget()
        widget.setLayout(self.mainHBox)
        self.setCentralWidget(widget)

    def initMenu(self):
        self.fileMenu = self.menuBar().addMenu(self.trans('Shared.File'))
        self.editMenu = self.menuBar().addMenu(self.trans('Shared.Edit'))
        self.viewMenu = self.menuBar().addMenu(self.trans('Shared.View'))
        self.runMenu = self.menuBar().addMenu(self.trans('Shared.Run'))
        self.helpMenu = self.menuBar().addMenu(self.trans('Shared.Help'))

    def initWorkbench(self):
        self.workbench = Workbench()
        self.workbench.runConsole.clicked.connect(self.initConsole)
        self.addToolBar(Qt.LeftToolBarArea, self.workbench)

    def initTextEditor(self) -> None:
        self.editor = Editor()
        self.editor.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        self.mainHBox.addWidget(self.editor)

    def initStatusBar(self):
        self.statusBar = QtWidgets.QStatusBar()
        self.statusBar.insertPermanentWidget(0, QtWidgets.QWidget())
        self.setStatusBar(self.statusBar)

    def initConsole(self):
        if not self.mainHBox.findChild(QtWidgets.QDockWidget, 'dock'):
            self.dock = QtWidgets.QDockWidget('Dockable', self)

        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock)
        self.console = Console()
        self.dock.setWidget(self.console)

    def openFiles(self) -> None:
        fileDialog = QtWidgets.QFileDialog(self)
        fileDialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog)

        result, folder = fileDialog.getOpenFileNames(
            parent=self,
            caption=self.trans('Editor.OpenFiles'),
            directory=System.config.get('configs.files.last_opened_folder', os.path.expanduser('~')),
            filter=self.getFileFormats()
        )
        System.config.set('files.last_opened_folder', folder)
        System.config.save('files')

        if result:
            print(result)

    def openFolder(self) -> None:
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            parent=self,
            caption=self.trans('Editor.OpenFolder'),
            directory=System.config.get('configs.files.last_opened_folder', os.path.expanduser('~'))
        )
        System.config.set('files.last_opened_folder', folder)
        if folder:
            print(os.listdir(folder))

    @lru_cache(None)
    def getFileFormats(self) -> str:
        formats = System.config.get('editor.formats')
        result = ';;'.join('{}{}'.format(
            self.translation.get(k), v) for (k, v) in formats.items())
        return result + ';;'.join(formats)

    def onCloseEventAccept(self) -> None:
        # System.config.save('apps.editor.files')
        pass

    def onCloseEventIgnore(self) -> None:
        pass

    def onCloseEventDefault(self) -> None:
        pass
