import os
from pathlib import Path

from typing import Any
from typing import Union

from dotty_dict import Dotty

from toolkit.logger import DummyLogger
from toolkit.logger import Messages
from toolkit.objects.system import SystemObject

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

    def get(self, key: str, default_key: str = None, default_value: Any = None) -> Any:
        """
        Caller -> Config<get method> [check if called ]
        """
        # caller = inspect.stack()
        # caller = caller[1][0].f_locals.get('self')

        if default_key:
            default_value = super().get(default_key, default_value)
        return super().get(key) or default_value

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
    Provides an easy access to the instances, settings and etc.
    """
    version = '0.0.2'
    logger = DummyLogger
    config_class = SystemConfig

    def __init__(self) -> None:
        self.__is_init = False
        self.__app_root = None
        self.__sys_root = None
        self.__config = None
        self.__objects = {}

    def log(self, message: Any, message_type: Messages = Messages.INFO, **kwargs) -> None:
        self.logger.log(message=message, message_type=message_type, **kwargs)

    def init(self, sys_root: str, app_root: str) -> None:
        if self.__is_init:
            raise Exception('Can\'t init twice')

        if not app_root or not sys_root:
            raise AttributeError('System or app root were not set')

        self.__app_root = Path(app_root)
        self.__sys_root = Path(sys_root)

        self.logger = self.logger()
        self.log(f'Starting System. Version: {self.version}')
        self.__read_configuration_files()

        self.__set_system_root(sys_root)
        self.__set_app_root(app_root)
        self.__is_init = True

    # Private methods

    def __read_configuration_files(self):
        """ Read files from .crabs folder """
        root_settings = read_json('settings.json')
        patterns = []
        for p in root_settings.get('configs'):
            patterns += list(Path().rglob(p))

        system_settings = read_json_files(patterns)
        if not system_settings:
            raise ValueError('Configuration is empty')

        self.__config = self.config_class(defaults={**root_settings, **system_settings})

    def __set_system_root(self, path: str) -> None:
        """ Set system/toolkit root by __file__ or by relative path """
        if not os.path.exists(path):
            raise OSError(f'Path "{path}" not found')

        if os.path.isfile(path):
            self.log(f'System root set to "{path}"')
            self.__sys_root = Path(path).parent
        elif os.path.isdir(path):
            self.__sys_root = Path(path)

    def __set_app_root(self, path: str):
        """ Set app root by __file__ or by relative path """
        if not os.path.exists(path):
            raise FileNotFoundError('File or path not found')

        if os.path.isfile(path):
            self.log(f'Root set to {path}')
            self.__app_root = Path(path).parent
        elif os.path.isdir(path):
            self.__sys_root = Path(path)

    # Private object access methods

    def __add_object(self, instance: SystemObject, name: str) -> None:
        """ Add SystemObject """
        if isinstance(instance, str):
            if is_import_string(instance):
                instance = import_string(instance)
            else:
                self.log(f'Can\'t import "{instance}". Invalid import string')

        if not isinstance(getattr(instance, 'type'), SystemObject):
            self.log(f'Object "{instance.__class__.__name__}" is not SystemObject based')

        if name in self.__objects:
            self.log(f'Object "{instance}" already added. Skipping', Messages.WARNING)

        self.__objects[name] = instance
        self.log(f'Object "{instance.name}" with type {instance.type.name} was added')

    # Public object access methods

    def add_objects(self, objects: Union[list, tuple]) -> None:
        # Iter trough the list of objects and import them
        for obj_str in objects:
            self.log(f'Preparing {obj_str}')
            self.__add_object(*import_string(obj_str))

        # Add imported objects into the node
        for obj_name, obj_type in self.__objects.items():
            if not issubclass(obj_type, SystemObject):
                self.log(f'Can\'t init non SystemObject "{obj_name}" object')
                continue

            self.log(f'Initializing "{obj_type.name}"')

            obj_type = obj_type()
            self.__objects[obj_name] = obj_type
            obj_type.init()

    def get_object(self, name: str) -> SystemObject:
        """
        Get object by name

        Args:
            name (str): object name

        Returns:
            object
        """
        if name not in self.__objects:
            self.log(f'Object "{name}" not found')

        return self.__objects[name]

    # Event methods

    def on_ready(self) -> None:
        self.log(f'System is ready. Objects loaded: {len(self.__objects)}')

    # Properties

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

    # Hooks

    def __repr__(self) -> str:
        return f'({self.__class__.__name__}) <objects: {", ".join(self.__objects.keys()[:4])} . . .>'


System = SystemManager()
