import sys
import traceback
from ui.utils.error import SystemError


def except_hook(exc_type, exc_value, exc_traceback):
    traceback_collect = []
    if exc_traceback:
        format_exception = traceback.format_tb(exc_traceback)
        for line in format_exception:
            traceback_collect.append(repr(line).replace('\\n', ''))

    SystemError(exc_type, exc_value, traceback_collect)


# sys.excepthook = except_hook


def getQtApp(*args, **kwargs):
    from PyQt5 import QtWidgets
    from PyQt5.QtCore import Qt

    app = QtWidgets.QApplication.instance()
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    if app is None:
        if not args:
            args = ([''],)
        app = QtWidgets.QApplication(*args, **kwargs)
    return app


def launch():
    from toolkit.package.reqs import manage_requirements

    # Install all requirements
    manage_requirements()

    from toolkit.logger import Messages
    from toolkit.managers.system.manager import System
    from toolkit.utils.objects import is_import_string
    from toolkit.utils.objects import import_string

    System.init(sys_root='toolkit', app_root='editor')

    from PyQt5.QtWidgets import QApplication
    from ui.utils.splash import createSplashScreen

    app = getQtApp()
    splash = createSplashScreen('branding/splash.png')
    splash.show()
    QApplication.processEvents()

    # Get managers
    managers = set()
    # TODO: Create SystemObjectsNode to handle objects dependencies
    managers_order = System.config.get('apps')
    if not managers_order:
        raise KeyError('Key "configs.managers.managers_order" not found')

    for manager in managers_order:
        if is_import_string(manager):
            managers.add(manager)

    System.add_objects(managers)

    launch = System.config.get('launch')
    if not is_import_string(launch):
        System.log(f'Can\'t start application from {launch}.'
                   f' Incorrect import path', Messages.CRITICAL)

    launch = import_string(launch, False)
    splash.close()
    launch(app)
    sys.exit(app.exec_())


if __name__ == '__main__':
    launch()
