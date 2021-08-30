from toolkit.system.manager import System
from toolkit.utils.objects import is_import_string


def get_managers():
    collect = []
    for manager in System.config.get('configs.managers.managers_order'):
        if is_import_string(manager):
            collect.append(manager)

    return collect
