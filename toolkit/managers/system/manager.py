import os
import glob
from pathlib import Path

from typing import Any
from typing import List
from typing import Union

from dotty_dict import Dotty

from toolkit.logger import DummyLogger
from toolkit.logger import MessageTypes
from toolkit.managers.system.objects import SystemObject
from toolkit.managers.system.services import get_caller_name

from toolkit.helpers.objects import import_string
from toolkit.helpers.objects import is_import_string

from toolkit.helpers.files import read_json
from toolkit.helpers.files import update_json
from toolkit.helpers.files import read_json_files


class CustomDictionary(dict):

    def __init__(self, *args, **kwargs):
        self._show_hidden_attributes = kwargs.get('show_hidden_attributes', False)
        super().__init__(*args, **kwargs)

    def items(self):
        return {k: v for (k, v) in super().items() if not k.startswith('__') and not k.endswith('__')}

    def values(self):
        return set(i for i in super().values() if not i.startswith('__') and not i.endswith('__'))

    def keys(self):
        return set(i for i in super().keys() if not i.startswith('__') and not i.endswith('__'))


class SystemConfig(Dotty):
    show_hidden_attributes: bool = False

    def __init__(self, defaults: dict = None) -> None:
        dictionary = CustomDictionary(show_hidden_attributes=self.show_hidden_attributes)
        if defaults:
            dictionary.update(**defaults)

        super().__init__(dictionary=dictionary)

    def get(self, key: str, default_key: str = None, default: Any = None) -> Any:
        if default_key:
            default = super().get(default_key, default)
        return super().get(key) or default

    def set(self, key, value) -> None:
        self[key] = value

    def save(self, key: str) -> None:
        """
        Args:
            key (str): f.e. 'dictionary.nested.key'

        Returns:
            None
        """
        file = self.get(f'{key}.__file__')
        if not file:
            raise KeyError(f'section "{key}.__file__" does not exist')

        if not os.path.exists(file):
            raise KeyError(f'file "{file}" does not exist')

        update_json(key, self[key])

    def from_json_file(self, file: Union[str, os.PathLike], **kwargs) -> None:
        self.update(**read_json(file, **kwargs))

    def __repr__(self) -> str:
        return f'({self.__class__.__name__}) <items keys: {list(self._data.keys())[:4]} . . .>'


class SystemManager:
    """
    System is the core manager
    Provides easy access to the instances, settings and etc.
    """
    version = '0.0.2'
    logger = DummyLogger
    config_class = SystemConfig

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.__app_root = None
        self.__sys_root = None
        self.__config = None
        self._objects = {}

    def log(self, message: str, message_type: MessageTypes = MessageTypes.INFO, **kwargs) -> None:
        self.logger.log(message=message, message_type=message_type, **kwargs)

    def prepare(self, sys_root: str, app_root: str) -> None:
        if not app_root or not sys_root:
            raise AttributeError('System or app root were not set')

        self.logger = self.logger()
        self.log(f'Starting a system. Version: {self.version}')
        self._read_configuration_files()

        self._set_system_root(sys_root)
        self._set_app_root(app_root)

    # Private methods

    def _read_configuration_files(self, root: str = 'configs', pattern: str = '*.json'):
        defaults = read_json_files(glob.glob(f'{root}/{pattern}'))
        if not defaults:
            raise ValueError('Configuration is empty')

        self.__config = self.config_class(defaults=defaults)

    def _set_system_root(self, path: str) -> None:
        if not os.path.exists(path):
            raise OSError(f'Path "{path}" not found')

        if os.path.isfile(path):
            self.log(f'System root set to "{path}"')
            self.__sys_root = Path(path).parent
        elif os.path.isdir(path):
            self.__sys_root = Path(path)

    def _set_app_root(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError('File or path not found')

        if os.path.isfile(path):
            self.log(f'Root set to {path}')
            self.__app_root = Path(path).parent
        elif os.path.isdir(path):
            self.__sys_root = Path(path)

    # Private object access methods

    def _add_object(self, instance: type, name: str) -> None:
        """
        Args:
            instance (type): object that will be added
            name (str): object key name
        """
        if isinstance(instance, str):
            if is_import_string(instance):
                instance = import_string(instance)
            else:
                self.log(f'Can\'t import "{instance}". Invalid import string')

        if not isinstance(getattr(instance, 'type'), SystemObject):
            self.log(f'Object "{instance.__class__.__name__}" is not SystemObject based')

        if name in self._objects:
            self.log(f'Object "{instance}" already added. Skipping', MessageTypes.WARNING)

        self._objects[name] = instance
        self.log(f'Object "{instance}" ({instance.type}) added')

    # Public object access methods

    def add_objects(self, objects: Union[list, tuple]) -> None:
        for obj_str in objects:
            self.log(f'Adding {obj_str}')
            self._add_object(*import_string(obj_str))

        for obj_name, obj_type in self._objects.items():
            self.log(f'Initializing {obj_type}')
            self._objects[obj_name] = obj_type()

    def get_object(self, name: str) -> object:
        """
        Get object by name

        Args:
            name (str): object name

        Returns:
            object
        """
        if name not in self._objects:
            self.log(f'Object "{name}" not found')

        return self._objects[name]

    def remove_object(self, name: str) -> None:
        """ Semiprivate method """
        caller = get_caller_name()

        if name not in self._objects:
            self.log(f'Object "{name}" not found. Skipping', MessageTypes.WARNING)

        self._objects.pop(name)
        self.log(f'Object "{name}" has been removed')

    # Event methods

    def ready(self) -> None:
        self.log(f'System is ready. Objects loaded: {len(self._objects)}')

    # Properties

    def get_objects_list(self) -> List[object]:
        return list(self._objects.keys())

    @property
    def sys_root(self) -> Path:
        # System/Toolkit root
        return self.__sys_root

    @property
    def app_root(self) -> Path:
        return self.__app_root

    @property
    def config(self) -> SystemConfig:
        return self.__config

    def __repr__(self) -> str:
        return f'({self.__class__.__name__}) <objects: {self.get_objects_list()[:4]} . . .>'


System = SystemManager()
