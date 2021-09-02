import sys
from toolkit.utils.files import read_json
from toolkit.utils.os import check_connection


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
            raise ConnectionError('Can\'t connect to the internet')

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