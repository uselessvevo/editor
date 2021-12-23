from editor_core.objects.plugin import Plugin
from editor_core.objects.system import SystemObjectTypes
from editor_core.objects.system import SystemConfigCategories
from editor_core.managers.system.manager import SystemManager


class TestPlugin(Plugin):

    def init(self, *args, **kwargs):
        pass
