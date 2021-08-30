#   Copyright @ Crab Dudes Developers
#   Licensed under the terms of the MIT license
#   File objects.py - 15.02.2021, 12:00

import re
import sys
import importlib
from toolkit.utils.files import read_json
from toolkit.utils.os import check_connection
from ui.windows.errorwindow import SystemErrorWindow


def prepare_dependencies(file: str = 'requirements.json', dev: bool = False):
    import subprocess
    import pkg_resources

    requirements = read_json(file)
    requirements = requirements.get('dev') if dev else requirements.get('prod')

    to_install = set(f'{k.lower()}=={v}' for (k, v) in requirements.get('install').items())
    to_delete = set(f'{k.lower()}=={v}' for (k, v) in requirements.get('delete').items())

    installed = set(str(v).replace(' ', '==').lower() for v in pkg_resources.working_set.by_key.values())
    missing = to_install - installed
    run_subprocess = None

    if missing:
        if not check_connection():
            SystemErrorWindow(
                err_type='ConnectionError',
                err_value='Can\'t connect to the internet',
                err_traceback='Can\'t install libraries - can\'t establish internet connection'
            )

        subprocess.call((sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'))
        run_subprocess = subprocess.check_call((sys.executable, '-m', 'pip', 'install', *missing))

        if run_subprocess != 0:
            raise subprocess.SubprocessError('can\'t install requirements')
        return run_subprocess

    if to_delete:
        subprocess.call((sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'))
        run_subprocess = subprocess.check_call((sys.executable, '-m', 'pip', 'uninstall', *to_delete))

        if run_subprocess != 0:
            raise subprocess.SubprocessError('can\'t remove libraries ')
        return run_subprocess

    return run_subprocess


def is_import_string(string: str):
    return True if re.match(r'^([a-zA-Z.]+)$', string) else False


def is_file_path_string(string: str):
    return True if re.match(r'(\w+:|/[a-zA-Z./]*[\s]?)', string) else False


def import_string(string: str, both: bool = True):
    """
    Import module by string:

    Args:
        string (str): <module path>.<ClassName>
        both (bool): if true - get import string and module, else - only module

    Returns:
        object
    """
    if not is_import_string(string):
        raise TypeError('string is not a valid "import string"')

    string = string.split('.')
    path, name = '.'.join(string[:-1]), string[-1]

    module = importlib.import_module(path)
    module = getattr(module, name)

    return (module, name) if both else module


def is_debug():
    trace = getattr(sys, 'gettrace', False)
    return True if trace() else False
