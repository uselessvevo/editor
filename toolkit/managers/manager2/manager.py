from toolkit.managers.base import BaseManager
from toolkit.managers.system.objects import SystemObjectTypes


class Manager2(BaseManager):
    type = SystemObjectTypes.CORE_MANAGER
    name = 'manager2'
    section = 'locales'
