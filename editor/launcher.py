import sys
import traceback

from ui.windows.errorwindow import SystemError


def except_hook(exc_type, exc_value, exc_traceback):
    traceback_collect = []
    if exc_traceback:
        format_exception = traceback.format_tb(exc_traceback)
        for line in format_exception:
            traceback_collect.append(repr(line).replace('\\n', ''))

    SystemError(exc_type, exc_value, traceback_collect)


# sys.excepthook = except_hook


def get_qt_app(*args, **kwargs):
    from PyQt5 import QtWidgets

    app = QtWidgets.QApplication.instance()
    if app is None:
        if not args:
            args = ([''],)
        app = QtWidgets.QApplication(*args, **kwargs)
    return app


def launch():
    from toolkit.installer.installer import prepare_dependencies

    prepare_dependencies()

    from toolkit.managers.system.manager import System
    from toolkit.helpers.objects import is_import_string

    System.prepare(sys_root='../toolkit', app_root=__file__)

    # get managers
    managers = set()
    # TODO: Create SystemObjectsNode to handle objects dependencies
    managers_order = System.config.get('configs.managers.managers_order')
    if not managers_order:
        raise KeyError('Key "configs.managers.managers_order" not found')

    for manager in managers_order:
        if is_import_string(manager):
            managers.add(manager)

    System.add_objects(managers)

    from editor.app.ui import MainUI
    from toolkit.managers.themes.services import getTheme
    from toolkit.managers.themes.services import getPalette

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
