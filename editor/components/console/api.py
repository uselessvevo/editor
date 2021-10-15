from PyQt5 import QtWidgets
from IPython.display import Image

from qtconsole.inprocess import QtInProcessKernelManager
from qtconsole.rich_jupyter_widget import RichJupyterWidget

from toolkit.managers.system.manager import System
from toolkit.managers.themes.services import getTheme


def getApp(*args, **kwargs):
    """Create a new qt5 app or return an existing one."""
    app = QtWidgets.QApplication.instance()
    if app is None:
        if not args:
            args = ([''],)
        app = QtWidgets.QApplication(*args, **kwargs)
    return app


class QIPythonWidget(RichJupyterWidget):
    """
    Convenience class for a live IPython console widget.
    We can replace the standard banner using the customBanner argument
    """

    def __init__(self, banner=None, *args, **kwargs):
        super(QIPythonWidget, self).__init__(*args, **kwargs)
        self.banner = banner or 'Console'
        self.kernel_manager = kernel_manager = QtInProcessKernelManager()

        kernel_manager.start_kernel()
        kernel_manager.kernel.gui = 'qt'

        self.kernel_client = kernel_client = self._kernel_manager.client()
        kernel_client.start_channels()

        self.kernel = self.kernel_manager.kernel.shell

        self.exit_requested.connect(self.stop)
        self.style_sheet = getTheme(System.config.get('configs.ui.theme', default_key='ui.default_theme'))

    def stop(self):
        self.kernel_client.stop_channels()
        self.kernel_manager.kernel_manager.shutdown_kernel()
        getApp().exit()

    def registerMethod(self, variableDict):
        """
        Given a dictionary containing name / value pairs,
        push those variables to the IPython console widget
        """
        self.kernel_manager.kernel.shell.push(variableDict)

    def clearTerminal(self):
        """
        Clears the terminal
        """
        self._control.clear()

    def printText(self, text):
        """
        Prints plain text to the console
        """
        self._append_plain_text(text)

    def executeCommand(self, command):
        """
        Execute a command in the frame of the console widget
        """
        self._execute(command, False)

    def printOutput(self):
        return self.export_html()

    def insertImage(self, image):
        return Image(image)
