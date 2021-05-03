#   Copyright @ Crab Dudes Developers
#   Licensed under the terms of the MIT license
#   File objects.py - 15.02.2021, 12:00

import re
import os
import sys
import inspect
import importlib
from pathlib import Path


def get_object_name(instance):
    """
    Get object (class) name or OBJECT_NAME (cloudykit/base/settings)

    Args:
        instance (object)
    """
    if not isinstance(instance, object):
        raise AttributeError(f'Instance is {type(instance)}')

    name = getattr(instance, 'name')

    return instance.__class__.__name__ if name else None


def get_object_path(instance, file=True):
    """
    Get object path

    Args:
        instance (object)
        file (bool): set false to return path without file

    Returns:
        relative path to object folder (str)
    """
    if not isinstance(instance, object):
        raise AttributeError(f'Instance is {type(instance)}')

    result = Path(inspect.getfile(instance.__class__))
    return result if file else result.parts[:-1]
    # return result if file else os.sep.join(result.split(os.sep)[:-1])


def get_object_folder_name(instance):
    """
    Get instance folder name

    Args:
        instance (object)

    Returns:
        relative path to object folder (str)
    """
    if not isinstance(instance, object):
        raise AttributeError(f'Instance is {type(instance)}')

    return os.path.split(os.path.relpath(inspect.getfile(instance.__class__)))[0]


def prepare_dependencies(debug=False):
    # Standard libraries
    import subprocess
    import pkg_resources

    from cloudykit.utils.files import read_json

    if debug:
        requirements = read_json('settings/requirements.dev.json')
    else:
        requirements = read_json('settings/requirements.release.json')

    to_install = set(k.lower() for k in requirements.get('toInstall'))
    to_delete = set(k.lower() for k in requirements.get('toDelete'))

    installed = set(str(v).replace(' ', '==').lower() for v in pkg_resources.working_set.by_key.values())
    missing = to_install - installed

    run_subprocess = None

    if missing:
        subprocess.call((sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'))
        run_subprocess = subprocess.check_call((sys.executable, '-m', 'pip', 'install', *missing))

        if run_subprocess != 0:
            raise subprocess.SubprocessError('Can\'t install requirements Aborting ')
        return run_subprocess

    if to_delete:
        subprocess.call((sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'))
        run_subprocess = subprocess.check_call((sys.executable, '-m', 'pip', 'uninstall', *to_delete))

        if run_subprocess != 0:
            raise subprocess.SubprocessError('Can\'t remove libraries Aborting ')
        return run_subprocess

    return run_subprocess


def is_import_string(string):
    return True if re.match(r'^([a-zA-Z.]+)$', string) else False


def is_file_path_string(string):
    return True if re.match(r'(\w+:|/[a-zA-Z./]*[\s]?)', string) else False


def import_string(string, both=True):
    """
    Import module by string:

    Args:
        string (str): <module path>.<ClassName>
        both (bool): if true - get import string and module, else - only module

    Returns:
        object
    """
    string = string.split('.')
    path, name = '.'.join(string[:-1]), string[-1]

    module = importlib.import_module(path)
    module = getattr(module, name)

    return (module, name) if both else module


def is_debug():
    trace = getattr(sys, 'gettrace', False)
    return True if trace() else False
