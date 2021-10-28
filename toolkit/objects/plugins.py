from toolkit.managers.system.manager import SystemObject


class BasePluginObject(SystemObject):
    pass


class Plugin(BasePluginObject):

    def register_shortcut(self, key: str):
        pass
