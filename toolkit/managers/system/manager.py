import fnmatch
import os
import atexit
import anytree
from pathlib import Path

from typing import Any, List
from typing import Union

from anytree import RenderTree, TreeError
from dotty_dict import Dotty

from toolkit.logger import DummyLogger
from toolkit.logger import MessageTypes
from toolkit.managers.system.objects import SystemObject

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
        self.__objects_node_map = {}

    def log(self, message: Any, message_type: MessageTypes = MessageTypes.INFO, **kwargs) -> None:
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

    def __read_configuration_files(self, folder: str = '.crabs', pattern: str = '*.json'):
        root_settings = read_json('settings.json')
        patterns = []
        for p in root_settings.get('configs'):
            patterns += list(Path().rglob(p))

        system_settings = read_json_files(patterns)
        if not system_settings:
            raise ValueError('Configuration is empty')

        self.__config = self.config_class(defaults={**root_settings, **system_settings})

    def __set_system_root(self, path: str) -> None:
        if not os.path.exists(path):
            raise OSError(f'Path "{path}" not found')

        if os.path.isfile(path):
            self.log(f'System root set to "{path}"')
            self.__sys_root = Path(path).parent
        elif os.path.isdir(path):
            self.__sys_root = Path(path)

    def __set_app_root(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError('File or path not found')

        if os.path.isfile(path):
            self.log(f'Root set to {path}')
            self.__app_root = Path(path).parent
        elif os.path.isdir(path):
            self.__sys_root = Path(path)

    # Private object access methods

    def __add_object(self, instance: type, name: str) -> None:
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

        if name in self.__objects:
            self.log(f'Object "{instance}" already added. Skipping', MessageTypes.WARNING)

        self.__objects[name] = instance
        self.log(f'Object "{instance}" ({instance.type}) added')

    def __add_to_parent_node(self, parent: object, children: List[object]) -> None:
        try:
            parent.children = children
            self.log(f'Object "{parent.name}" was set as parent for "{self.name}"')
            self.log(RenderTree(parent))
        except TreeError:
            self.log(f'Can\'t set parent node', MessageTypes.CRITICAL)

    def __get_objects_order(self, obj_name: str) -> list:
        """ Get object's node order  """
        obj = self.__objects.get(obj_name)
        if not obj:
            self.log(f'Can\'t find object name "{obj_name}"')

        return [i for i in anytree.iterators.levelorderiter.LevelOrderIter(obj)]

    # Public object access methods

    def add_objects(self, objects: Union[list, tuple]) -> None:
        # Iter trough the list of objects and import them
        for obj_str in objects:
            self.log(f'Adding {obj_str}')
            self.__add_object(*import_string(obj_str))

        # Add imported objects into the node
        for obj_name, obj_type in self.__objects.items():
            self.log(f'Initializing "{obj_type.name}"')

            # Init object with the parent node
            if obj_type.parent_name:
                parent_obj = self.__objects.get(obj_type.parent_name)
                if not parent_obj:
                    raise KeyError(f'Can\'t find object named "{parent_obj.parent_name}"')

                # Create init order
                # По сути, нам надо собрать все классы объектов, пробежаться по ним и взять атрибут `parent_name`
                # Потом составить карту зависимостей и составить порядок запуска
                self.__objects[obj_name] = obj_type()

            # Init object without the parent node
            else:
                self.__objects[obj_name] = obj_type()

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
        return f'({self.__class__.__name__}) <objects: {list(self.__objects.keys())[:4]} . . .>'


System = SystemManager()
