from PyQt5.Qt import Qt
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from editor.components.console.api import QIPythonWidget
from editor.components.console.methods import get_process_id
from editor.components.console.methods import rainbow

from toolkit.managers.system.manager import System
from toolkit.objects.system import SystemObject, SystemObjectTypes


class Console(SystemObject, QtWidgets.QWidget):
    """
    Main GUI Window including a button and IPython Console widget inside vertical layout
    """
    name = 'main_ui.console'
    type = SystemObjectTypes.PLUGIN

    def __init__(self, parent=None):
        super(Console, self).__init__(parent)
        self.trans = System.get_object('LocalesManager')
        self.files = System.get_object('AssetsManager')

    def init(self, *args, **kwargs):
        self.setWindowTitle('Editor Console')
        self.setGeometry(300, 300, 800, 550)

        self.initMain()
        self.initToolbar()
        self.initConsole()
        self.initGrid()

    def initGrid(self):
        self.grid.addWidget(self.toolBar, 0, 0)
        self.grid.addWidget(self.console, 1, 0)

    def initMain(self):
        self.setWindowIcon(QtGui.QIcon(self.files('shared/icons/flag.svg')))
        self.grid = QtWidgets.QGridLayout(self)
        self.centralWidget = QtWidgets.QWidget()
        self.grid.addWidget(self.centralWidget)

    def initToolbar(self) -> None:
        # Init toolbar
        self.toolBar = QtWidgets.QToolBar('&File')
        self.toolBar.setMovable(False)
        self.toolBar.setIconSize(QtCore.QSize(15, 15))
        self.toolBar.setFixedHeight(36)

        self.toolBar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.toolBar.setOrientation(Qt.Horizontal)
        self.toolBar.setSizePolicy(QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Maximum
        ))

        # Actions
        runProccess = QtWidgets.QToolButton()
        runProccess.setToolTip(self.trans('Shared.RunProcess'))
        runProccess.setIcon(QtGui.QIcon(self.files('shared/icons/start.svg')))
        runProccess.setToolButtonStyle(Qt.ToolButtonIconOnly)

        stopProccess = QtWidgets.QToolButton(self)
        stopProccess.setToolTip(self.trans('Shared.StopProcess'))
        stopProccess.setIcon(QtGui.QIcon(self.files('shared/icons/stop.svg')))
        stopProccess.setToolButtonStyle(Qt.ToolButtonIconOnly)

        restoreGrid = QtWidgets.QToolButton(self)
        restoreGrid.setToolTip(self.trans('Console.RestoreGrid'))
        restoreGrid.setIcon(QtGui.QIcon(self.files('shared/icons/grid.svg')))
        restoreGrid.setToolButtonStyle(Qt.ToolButtonIconOnly)

        exitAct = QtWidgets.QToolButton(self)
        exitAct.setToolTip(self.trans('Shared.Exit'))
        exitAct.setIcon(QtGui.QIcon(self.files('shared/icons/delete.svg')))
        exitAct.setToolButtonStyle(Qt.ToolButtonIconOnly)

        printOutput = QtWidgets.QToolButton(self)
        printOutput.setToolTip(self.trans('Shared.Print'))
        printOutput.setIcon(QtGui.QIcon(self.files('shared/icons/printer.svg')))
        printOutput.setToolButtonStyle(Qt.ToolButtonIconOnly)

        # Pack all default actions
        self.toolBar.addWidget(runProccess)
        self.toolBar.addWidget(stopProccess)
        self.toolBar.addWidget(restoreGrid)
        self.toolBar.addWidget(exitAct)
        self.toolBar.addWidget(printOutput)

    def initConsole(self):
        self.console = QIPythonWidget(f'Editor console ({System.version})\n\n')
        self.console.registerMethod({'proc_id': get_process_id})
        self.console.registerMethod({'rainbow': rainbow})
        self.console.registerMethod({'image': self.console.insertImage})
        self.console.registerMethod({'print_output': self.console.printOutput})
