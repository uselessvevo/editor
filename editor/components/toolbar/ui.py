from PyQt5.Qt import Qt
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from toolkit.managers import getFile


class Toolbar(QtWidgets.QToolBar):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        hbox = QtWidgets.QHBoxLayout()
        self.setLayout(hbox)
        self.setMovable(False)
        self.setContextMenuPolicy(Qt.PreventContextMenu)
        self.setFixedHeight(35)

        openFolder = QtWidgets.QToolButton()
        openFolder.setToolTip(self.tr('Shared.OpenFolder'))
        openFolder.setIcon(QtGui.QIcon(getFile('shared/icons/folder-open.svg')))
        openFolder.setToolButtonStyle(Qt.ToolButtonIconOnly)
        openFolder.setFixedSize(QtCore.QSize(15, 15))
        openFolder.setIconSize(QtCore.QSize(15, 15))

        runProcess = QtWidgets.QToolButton()
        runProcess.setToolTip(self.tr('Shared.RunProcess'))
        runProcess.setIcon(QtGui.QIcon(getFile('shared/icons/start.svg')))
        runProcess.setToolButtonStyle(Qt.ToolButtonIconOnly)
        runProcess.setFixedSize(QtCore.QSize(15, 15))
        runProcess.setIconSize(QtCore.QSize(15, 15))

        # Pack all default actions
        self.addWidget(openFolder)
        self.addWidget(runProcess)
