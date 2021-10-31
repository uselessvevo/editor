import types

from toolkit.objects.project import Project
from toolkit.managers.system.manager import SystemObject


class PluginObject(SystemObject):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._shortcut = None

    def mount(self) -> bool:
        """ Mount plugin into PluginManager """

    def unmount(self) -> None:
        """ Unmount plugin from PluginManager """

    def register_shortcut(self, key: str, method: types.MethodType) -> bool:
        """ Register keyboard shortcut to given method """

    def unregister_shortcut(self) -> bool:
        """ Unregister keyboard shortcut """

    def get_projects_list(self) -> Project:
        """ Get active project from ProjectManager (.crabs directory) """
