from PyQt5.Qt import Qt
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from toolkit.managers.system.manager import System
from toolkit.objects.system import SystemObject, SystemObjectTypes


class Workbench(SystemObject, QtWidgets.QToolBar):
    name = 'main_ui.editor'
    type = SystemObjectTypes.UTILITY

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.trans = System.get_object('LocalesManager')
        self.files = System.get_object('AssetsManager')

    def init(self):
        self.setMovable(False)
        self.setIconSize(QtCore.QSize(30, 30))
        self.setContextMenuPolicy(Qt.PreventContextMenu)
        self.setOrientation(Qt.Vertical)
        self.setSizePolicy(QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Maximum
        ))

        openFolder = QtWidgets.QToolButton()
        openFolder.setToolTip(self.trans('Shared.OpenFolder'))
        openFolder.setIcon(QtGui.QIcon(self.files('shared/icons/folder-open.svg')))
        openFolder.setToolButtonStyle(Qt.ToolButtonIconOnly)

        search = QtWidgets.QToolButton()
        search.setToolTip(self.trans('Shared.Search'))
        search.setIcon(QtGui.QIcon(self.files('shared/icons/search.svg')))
        search.setToolButtonStyle(Qt.ToolButtonIconOnly)

        settings = QtWidgets.QToolButton()
        settings.setToolTip(self.trans('Shared.Settings'))
        settings.setIcon(QtGui.QIcon(self.files('shared/icons/settings.svg')))
        settings.setToolButtonStyle(Qt.ToolButtonIconOnly)

        runProcess = QtWidgets.QToolButton()
        runProcess.setToolTip(self.trans('Shared.RunProcess'))
        runProcess.setIcon(QtGui.QIcon(self.files('shared/icons/start.svg')))
        runProcess.setToolButtonStyle(Qt.ToolButtonIconOnly)

        spacer = QtWidgets.QWidget()
        spacer.setObjectName('spacer')
        spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )

        self.runConsole = QtWidgets.QToolButton()
        self.runConsole.setToolTip(self.trans('Shared.runConsole'))
        self.runConsole.setIcon(QtGui.QIcon(self.files('shared/icons/bug.svg')))
        self.runConsole.setToolButtonStyle(Qt.ToolButtonIconOnly)

        # Pack all default actions
        self.addWidget(openFolder)
        self.addWidget(search)
        self.addWidget(runProcess)
        self.addWidget(spacer)
        self.addWidget(self.runConsole)
        self.addWidget(settings)
