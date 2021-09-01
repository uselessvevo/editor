import sys
import traceback

from PyQt5 import QtWidgets

from app.ui import MainUI

from toolkit.system.manager import System
from toolkit.utils.objects import prepare_dependencies
from toolkit.utils.system import get_managers
from toolkit.utils.themes import getTheme
from toolkit.utils.themes import getPalette
from ui.windows.errorwindow import SystemErrorWindow


def except_hook(exc_type, exc_value, exc_traceback):
    traceback_collect = []
    if exc_traceback:
        format_exception = traceback.format_tb(exc_traceback)
        for line in format_exception:
            traceback_collect.append(repr(line).replace('\\n', ''))

    SystemErrorWindow(exc_type, exc_value, traceback_collect)


sys.excepthook = except_hook


def get_qt_app(*args, **kwargs):
    """Create a new qt5 app or return an existing one."""
    app = QtWidgets.QApplication.instance()
    if app is None:
        if not args:
            args = ([''],)
        app = QtWidgets.QApplication(*args, **kwargs)
    return app


def prepare_system():
    System.set_system_root(__file__)
    System.add_objects(*get_managers())
    System.init_objects()


def launch():
    prepare_dependencies()
    prepare_system()

    app = get_qt_app()

    theme = System.config.get(
        key='configs.ui.theme',
        default_key='configs.ui.default_theme'
    )
    if theme:
        app.setStyleSheet(getTheme(theme))
        app.setPalette(getPalette(theme))

    # widget = ui.IPythonConsoleWidget()
    widget = MainUI()
    widget.show()

    sys.exit(app.exec_())
