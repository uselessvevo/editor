from toolkit.managers.base import BaseManager
from toolkit.managers.system.objects import SystemObjectTypes


class Manager2(BaseManager):
    name = 'manager1'
    type = SystemObjectTypes.CORE_MANAGER
    section = 'locales'
