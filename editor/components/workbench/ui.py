from PyQt5.Qt import Qt
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from toolkit.managers import getFile


class Workbench(QtWidgets.QToolBar):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setMovable(False)
        self.setIconSize(QtCore.QSize(30, 30))
        self.setContextMenuPolicy(Qt.PreventContextMenu)
        self.setOrientation(Qt.Vertical)
        self.setSizePolicy(QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Maximum
        ))

        openFolder = QtWidgets.QToolButton()
        openFolder.setToolTip(self.tr('Shared.OpenFolder'))
        openFolder.setIcon(QtGui.QIcon(getFile('shared/icons/folder-open.svg')))
        openFolder.setToolButtonStyle(Qt.ToolButtonIconOnly)

        search = QtWidgets.QToolButton()
        search.setToolTip(self.tr('Shared.Search'))
        search.setIcon(QtGui.QIcon(getFile('shared/icons/search.svg')))
        search.setToolButtonStyle(Qt.ToolButtonIconOnly)

        settings = QtWidgets.QToolButton()
        settings.setToolTip(self.tr('Shared.Settings'))
        settings.setIcon(QtGui.QIcon(getFile('shared/icons/settings.svg')))
        settings.setToolButtonStyle(Qt.ToolButtonIconOnly)

        runProcess = QtWidgets.QToolButton()
        runProcess.setToolTip(self.tr('Shared.RunProcess'))
        runProcess.setIcon(QtGui.QIcon(getFile('shared/icons/start.svg')))
        runProcess.setToolButtonStyle(Qt.ToolButtonIconOnly)

        spacer = QtWidgets.QWidget()
        spacer.setObjectName('spacer')
        spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )

        self.runConsole = QtWidgets.QToolButton()
        self.runConsole.setToolTip(self.tr('Shared.runConsole'))
        self.runConsole.setIcon(QtGui.QIcon(getFile('shared/icons/bug.svg')))
        self.runConsole.setToolButtonStyle(Qt.ToolButtonIconOnly)

        # Pack all default actions
        self.addWidget(openFolder)
        self.addWidget(search)
        self.addWidget(runProcess)
        self.addWidget(spacer)
        self.addWidget(self.runConsole)
        self.addWidget(settings)
