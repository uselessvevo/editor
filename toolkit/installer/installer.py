import os
import sys
import subprocess

from toolkit.helpers.files import read_json
from toolkit.helpers.os import call_subprocess
from toolkit.helpers.network import check_connection


def create_packaging_env(directory: str, pyver: str, name: str = 'packaging-env', conda_path: str = None):
    """
    Create a Python virtual environment in the target_directory.

    Returns the path to the newly created environment's Python executable.
    """
    fullpath = os.path.join(directory, name)

    if conda_path:
        command = (conda_path, 'create', '-p', os.path.normpath(fullpath), f'python={pyver}', '-y')
        env_path = os.path.join(fullpath, 'python.exe')

    elif os.name == 'nt':
        command = [sys.executable, '-m', 'venv', fullpath]
        env_path = os.path.join(fullpath, 'Scripts', 'python.exe')

    elif os.name in ('darwin', 'posix'):
        command = [sys.executable, '-m', 'venv', fullpath]
        env_path = os.path.join(fullpath, 'bin', fullpath)

    else:
        raise OSError('Can\'t create virtual environment')

    call_subprocess(command)
    return env_path


def process_packages(command: str, *packages) -> int:
    call_subprocess((sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'))
    run_subprocess = subprocess.check_call((sys.executable, '-m', 'pip', command, *packages))

    if run_subprocess != 0:
        raise subprocess.SubprocessError('can\'t install requirements')
    return run_subprocess


def prepare_dependencies(file: str = 'requirements.json', dev: bool = False) -> int:
    import pkg_resources

    requirements = read_json(file)
    requirements = requirements.get('dev') if dev else requirements.get('prod')

    to_install = set(f'{k.lower()}=={v}' for (k, v) in requirements.get('install').items())
    to_delete = set(f'{k.lower()}=={v}' for (k, v) in requirements.get('delete').items())

    installed = set(str(v).replace(' ', '==').lower() for v in pkg_resources.working_set.by_key.values())
    to_install = to_install - installed

    if to_install:
        if not check_connection():
            raise ConnectionError('Can\'t connect to the internet')

        return process_packages('install', *to_install)

    if to_delete:
        return process_packages('uninstall', *to_delete)
