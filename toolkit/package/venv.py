import os
import sys
import subprocess

from toolkit.utils.os import call_subprocess


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
