import os
import glob
from typing import Any
from typing import List

from dotty_dict import Dotty

from toolkit.system.objects import SystemObject, SystemObjectTypes
from toolkit.utils.files import read_json_files
from toolkit.utils.files import read_json
from toolkit.utils.files import update_json
from toolkit.utils.logger import MessageTypes, DummyLogger
from toolkit.utils.objects import import_string
from toolkit.utils.objects import is_import_string


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

    def get(self, key, default=None, default_key=None) -> Any:
        if default_key:
            default = super().get(default_key, default)
        return super().get(key) or default

    def set(self, key, value) -> None:
        self[key] = value

    def save(self, key) -> None:
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

    def from_json_file(self, file, **kwargs) -> None:
        self.update(**read_json(file, **kwargs))

    def __repr__(self) -> str:
        return f'({self.__class__.__name__}) <items: {list(self._data.keys())[:2]}\n>'


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
        self.logger = kwargs.get('logger', self.logger)()
        self.log(f'Starting a system. Version: {self.version}')

        self.__root = None
        self.__objects = {}

        defaults = read_json_files(glob.glob('configs/*.json'))
        if not defaults:
            raise ValueError('Configuration is empty')

        self.__config = self.config_class(defaults=defaults)

    def log(self, message: str, message_type: MessageTypes = MessageTypes.INFO, **kwargs) -> None:
        self.logger.log(message=message, message_type=message_type, **kwargs)

    def set_system_root(self, root) -> None:
        """
        Args:
            root (str): project root path

        Returns:
            None
        """
        if not os.path.exists(root):
            raise FileNotFoundError('file or path not found')

        if os.path.isfile(root):
            self.log(f'Root set to {root}')
            self.__root = os.path.split(root)[0]

    # Object management methods

    def init_objects(self) -> None:
        for key, instance in self.__objects.items():
            self.log(f'Init an object {instance}')
            self.__objects[key] = instance()

    def add_objects(self, *objects: str) -> None:
        objects = [i for i in objects if i in objects]

        for obj_str in objects:
            self.log(f'Adding an object {obj_str}')
            self.add_object(*import_string(obj_str))

    def add_object(self, instance: type, name: str) -> None:
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

        if not isinstance(getattr(instance, 'type', None), SystemObject):
            self.log(f'Object "{instance.__class__.__name__}" is not SystemObject based')

        if name in self.__objects:
            self.log(f'Object "{instance}" already added. Skipping', MessageTypes.WARNING)

        self.__objects[name] = instance
        self.log(f'Object "{instance}" ({instance.type}) was added')

    def remove_object(self, name: str) -> None:
        if name not in self.__objects:
            self.log(f'Object "{name}" not found. Skipping', MessageTypes.WARNING)

        self.__objects.pop(name)
        self.log(f'Object "{name}" has been removed')

    # Object access methods

    def get_object(self, name: str) -> object:
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

    def get_objects_list(self) -> List[object]:
        return list(self.__objects.keys())

    # Event methods

    def ready(self) -> None:
        self.log(f'System is ready. Objects loaded: {len(self.__objects)}')

    # Properties

    @property
    def root(self) -> str:
        return self.__root

    @property
    def config(self) -> object:
        return self.__config

    def __str__(self) -> str:
        return f'Objects: {self.get_objects_list()[:4]} . . .'

    def __repr__(self) -> str:
        return f'({self.__class__.__name__}) <objects: {self.get_objects_list()[:4]}, ...>'


System = SystemManager()
