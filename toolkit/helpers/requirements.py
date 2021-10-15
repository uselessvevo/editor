from toolkit.helpers.files import read_json
from toolkit.helpers.network import check_connection
from toolkit.installer.installer import process_packages


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
