import sys
import argparse
import traceback

from ui.windows.errorwindow import SystemError


def except_hook(exc_type, exc_value, exc_traceback):
    traceback_collect = []
    if exc_traceback:
        format_exception = traceback.format_tb(exc_traceback)
        for line in format_exception:
            traceback_collect.append(repr(line).replace('\\n', ''))

    SystemError(exc_type, exc_value, traceback_collect)


sys.excepthook = except_hook


def get_qt_app(*args, **kwargs):
    from PyQt5 import QtWidgets

    app = QtWidgets.QApplication.instance()
    if app is None:
        if not args:
            args = ([''],)
        app = QtWidgets.QApplication(*args, **kwargs)
    return app


def launch():
    from toolkit.utils.installer import prepare_dependencies

    prepare_dependencies()

    from toolkit.system.manager import System
    from toolkit.utils.system import get_managers

    System.set_system_root(__file__)
    System.add_objects(*get_managers())
    System.init_objects()

    from editor.app.ui import MainUI
    from toolkit.utils.themes import getTheme
    from toolkit.utils.themes import getPalette

    app = get_qt_app()

    theme = System.config.get(
        key='configs.ui.theme',
        default_key='configs.ui.default_theme'
    )
    if theme:
        app.setStyleSheet(getTheme(theme))
        app.setPalette(getPalette(theme))

    widget = MainUI()
    widget.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    launch()
