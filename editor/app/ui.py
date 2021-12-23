import os
import sys
from functools import lru_cache

from PyQt5 import QtGui, Qt
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QAction

from editor_core.managers.system.manager import System
from editor_core.objects.system import SystemObject
from editor_core.objects.system import SystemObjectTypes

from editor_ui.windows.window import BaseWindowMixin

from editor.components.editor.ui import Editor
from editor.components.console.ui import Console
from editor.components.workbench.ui import Workbench


class MainUI(SystemObject, BaseWindowMixin, QtWidgets.QMainWindow):
    defaultMinSize = (1020, 670)
    defaultPosition = (150, 150)
    name = 'main_ui'
    type = SystemObjectTypes.PLUGIN

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trans = System.get_object('LocalesManager')
        self.files = System.get_object('AssetsManager')

    def init(self, *args, **kwargs):
        self.prepareMain()
        self.prepareLayout()
        self.prepareMenu()
        self.prepareTextEditor()
        self.prepareWorkbench()
        self.prepareStatusBar()
        self.prepareShortcuts()

    def prepareMain(self):
        self.setWindowTitle(f'Editor - {os.getcwd()}')
        self.setWindowIcon(QtGui.QIcon(self.files('shared/icons/magic.svg')))
        self.setMinSize()
        self.moveToCenter()

    def prepareLayout(self):
        self.mainHBox = QtWidgets.QHBoxLayout()
        self.toolBarHBox = QtWidgets.QHBoxLayout()
        self.workbenchVBox = QtWidgets.QVBoxLayout()
        self.treeViewVBox = QtWidgets.QVBoxLayout()
        self.editorHBox = QtWidgets.QHBoxLayout()

        self.dock = QtWidgets.QDockWidget('Console', self)

        self.mainHBox.addLayout(self.workbenchVBox)
        self.mainHBox.addLayout(self.treeViewVBox)
        self.mainHBox.addLayout(self.editorHBox)
        self.setLayout(self.mainHBox)

        self.mainHBox.setContentsMargins(0, 0, 0, 0)
        self.mainHBox.setSpacing(20)

        widget = QtWidgets.QWidget()
        widget.setLayout(self.mainHBox)
        self.setCentralWidget(widget)

    def prepareMenu(self):
        self.mainMenuBar = self.menuBar()
        self.fileMenu = self.mainMenuBar.addMenu(self.trans('Shared.File'))
        self.fileMenu.addAction(QAction(self.trans('Shared.OpenFile'), self))
        self.editMenu = self.mainMenuBar.addMenu(self.trans('Shared.Edit'))
        self.viewMenu = self.mainMenuBar.addMenu(self.trans('Shared.View'))
        self.runMenu = self.mainMenuBar.addMenu(self.trans('Shared.Run'))
        self.helpMenu = self.mainMenuBar.addMenu(self.trans('Shared.Help'))

    def prepareShortcuts(self):
        self.shortcutClose = QtWidgets.QShortcut(QKeySequence('Ctrl+Q'), self)
        self.shortcutClose.activated.connect(self.close)

    def prepareWorkbench(self):
        self.workbench = Workbench()
        self.workbench.init()
        self.workbench.runConsole.clicked.connect(self.prepareConsole)
        self.addToolBar(Qt.LeftToolBarArea, self.workbench)

    def prepareTextEditor(self) -> None:
        self.editor = Editor()
        self.editor.init()
        self.editor.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        self.mainHBox.addWidget(self.editor)

    def prepareStatusBar(self):
        self.statusBar = QtWidgets.QStatusBar()
        self.statusBar.insertPermanentWidget(0, QtWidgets.QWidget())
        self.setStatusBar(self.statusBar)

    def prepareConsole(self):
        if not self.mainHBox.findChild(QtWidgets.QDockWidget, 'dock'):
            self.dock = QtWidgets.QDockWidget('Dockable', self)

        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock)
        self.console = Console()
        self.console.init()
        self.dock.setWidget(self.console)

    def openFiles(self) -> None:
        fileDialog = QtWidgets.QFileDialog(self)
        fileDialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog)

        result, folder = fileDialog.getOpenFileNames(
            parent=self,
            caption=self.trans('Editor.OpenFiles'),
            directory=System.config.get('app.files.last_opened_folder', os.path.expanduser('~')),
            filter=self.getFileFormats()
        )
        System.config.set('app.files.last_opened_folder', folder)
        System.config.save('files')

        if result:
            print(result)

    def openFolder(self) -> None:
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            parent=self,
            caption=self.trans('Editor.OpenFolder'),
            directory=System.config.get('app.files.last_opened_folder', os.path.expanduser('~'))
        )
        System.config.set('files.last_opened_folder', folder)
        if folder:
            print(os.listdir(folder))

    @lru_cache(None)
    def getFileFormats(self) -> str:
        formats = System.config.get('app.editor.formats')
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


def main(app, options: dict = None) -> None:
    from editor_core.managers.assets.services import getTheme
    from editor_core.managers.assets.services import getPalette

    widget = MainUI()
    theme = System.config.get('app.ui.theme', 'app.ui.default_theme')
    if theme:
        app.setStyleSheet(getTheme(System.app_root, theme))
        app.setPalette(getPalette(System.app_root, theme))

    widget.init()
    widget.show()
    sys.exit(app.exec_())
