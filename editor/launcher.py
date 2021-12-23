import os
from pathlib import Path

import sys
import traceback

from editor_core.utils.objects import is_debug
from editor_ui.utils.error import SystemError


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
    from editor_core.package.reqs import manage_requirements

    # Install all requirements
    manage_requirements(Path(Path.cwd()).parent, run_ui=True)

    from editor_core.logger import Messages
    from editor_core.managers.system.manager import System
    from editor_core.utils.objects import is_import_string
    from editor_core.utils.objects import import_string

    System.init(sys_root='toolkit', app_root='editor')

    from PyQt5.QtWidgets import QApplication
    from editor_ui.utils.splash import createSplashScreen

    app = get_qt_app()
    if not System.config.get('debug') and not is_debug():
        splash = createSplashScreen(
            path='branding/splash.svg',
            width=720,
            height=480,
            project_name='Toolkit.Editor',
            project_version=System.version
        )
        splash.show()
    QApplication.processEvents()

    # Get managers
    managers = []
    managers_order = System.config.get('apps')
    if not managers_order:
        raise KeyError('Key "configs.managers.managers_order" not found')

    for manager in managers_order:
        if is_import_string(manager):
            managers.append(manager)

    System.add_objects(managers)

    launch = System.config.get('launch')
    if not is_import_string(launch):
        System.log(f'Can\'t start application from {launch}.'
                   f' Incorrect import path', Messages.CRITICAL)

    launch = import_string(launch, False)
    if not System.config.get('debug') and not is_debug():
        splash.close()

    launch(app)
    sys.exit(app.exec_())


if __name__ == '__main__':
    launch()
