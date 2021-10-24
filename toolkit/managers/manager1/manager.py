from toolkit.managers.base import BaseManager
from toolkit.managers.system.objects import SystemObjectTypes


class Manager1(BaseManager):
    type = SystemObjectTypes.CORE_MANAGER
    section = 'locales'
    name = 'manager1'
    parent_name = 'Manager2'
