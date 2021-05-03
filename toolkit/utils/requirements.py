import pkg_resources


def show_warning(message):
    """Show warning using Tkinter if available"""
    try:
        # If Tkinter is installed (highly probable), showing an error pop-up
        import tkinter
        import tkinter.messagebox

        root = tkinter.Tk()
        root.withdraw()

        tkinter.messagebox.showerror('Editor', message)

    except ImportError:
        pass

    raise RuntimeError(message)


def check_requirements():
    import sys
    import subprocess

    with open('../../requirements.txt') as output:
        required = set(output.readlines())

    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed

    if missing:
        python = sys.executable
        subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)


def check_qt():
    """Check Qt binding requirements"""
    qt_infos = dict(pyqt5=("PyQt5", "5.6"))

    try:
        import PyQt5.QtCore
        package_name, required_ver = qt_infos['pyqt5']
        actual_ver = PyQt5.QtCore.PYQT_VERSION_STR

        if pkg_resources.parse_version(actual_ver) < pkg_resources.parse_version(required_ver):
            show_warning(
                'Please check installation requirements:\n'
                '%s %s+ is required (found v%s).' % (
                    package_name, required_ver, actual_ver
                ))

    except ImportError:
        show_warning(
            'Failed to run user interface'
            'Please check installation requirements'
        )
