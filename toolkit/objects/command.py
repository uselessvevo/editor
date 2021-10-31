import types

from toolkit.managers.system.manager import SystemObject


class Command(SystemObject):
    """ Base Command object. Doesn't provide a UI interaction """

    def registerShortcut(self, key: str, method: types.MethodType) -> bool:
        """ Register keyboard shortcut to given method """

    def unregisterShortcut(self) -> bool:
        """ Unregister keyboard shortcut """

    def getActiveProject(self):
        """ Get active project from ProjectManager (.crabs directory) """
