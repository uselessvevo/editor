import sys

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from app.ui import MainUI
from toolkit.managers.system import System
from toolkit.managers.system import prepare_plugins
from toolkit.utils.themes import getTheme
from toolkit.utils.themes import getPalette
from toolkit.utils.requirements import check_qt


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


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
    System.add_objects(
        'toolkit.managers.assets.AssetsManager',
    )
    prepare_plugins()
    System.init_objects()


def launch():
    check_qt()
    prepare_system()
    sys.excepthook = except_hook

    app = get_qt_app()

    translator = QtCore.QTranslator()
    translator.load(f'locales/')

    # Give app needed parameters
    app.installTranslator(translator)
    theme = System.config.get('configs.ui.theme', default_key='ui.default_theme')
    if theme:
        app.setStyleSheet(getTheme(theme))
        app.setPalette(getPalette(theme))

    # widget = ui.IPythonConsoleWidget()
    widget = MainUI()
    widget.show()

    sys.exit(app.exec_())
