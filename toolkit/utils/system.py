from toolkit.managers.system.manager import System
from toolkit.utils.objects import is_import_string


def get_managers():
    collect = set()
    # TODO: Create SystemObjectsNode to handle objects dependencies
    managers = System.config.get('configs.managers.managers_order')
    if not managers:
        raise KeyError('Key "configs.managers.managers_order" not found')

    for manager in managers:
        if is_import_string(manager):
            collect.add(manager)

    return collect
