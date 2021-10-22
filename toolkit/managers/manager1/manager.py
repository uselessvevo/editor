from toolkit.managers.base import BaseManager
from toolkit.managers.system.objects import SystemObjectTypes


class Manager1(BaseManager):
    name = 'manager1'
    type = SystemObjectTypes.CORE_MANAGER
    section = 'locales'

    parent_name = 'Manager2'
