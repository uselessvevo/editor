import os
import glob
from typing import List

from dotty_dict import Dotty

from toolkit.system.objects import SystemObject
from toolkit.utils.files import read_configs
from toolkit.utils.files import read_json
from toolkit.utils.files import update_json
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

    def __init__(self, defaults: dict = None):
        dictionary = CustomDictionary(show_hidden_attributes=self.show_hidden_attributes)
        if defaults:
            dictionary.update(**defaults)

        super().__init__(dictionary=dictionary)

    def get(self, key, default=None, default_key=None):
        if default_key:
            default = super().get(default_key, default)
        return super().get(key) or default

    def set(self, key, value):
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

    def from_json_file(self, file, **kwargs):
        self.update(**read_json(file, **kwargs))

    def __repr__(self):
        return f'({self.__class__.__name__}) <items: {list(self._data.keys())[:2]}\n>'


class SystemManager(SystemObject):
    """
    System is the core manager
    Provides easy access to the instances, settings and etc.
    """
    version = '0.0.2'
    config_class = SystemConfig

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._root = None
        self._objects = {}
        self._config = self.config_class(defaults=read_configs(glob.glob('configs/*.json')))
        self.log(f'Starting system {self.version}')

    def set_system_root(self, root):
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
            self._root = os.path.split(root)[0]

    def init_objects(self):
        for key, instance in self._objects.items():
            self.log(f'Init object {instance}')
            self._objects[key] = instance()

    def add_objects(self, *objects: str):
        objects = [i for i in objects if i in objects]

        for obj_str in objects:
            self.log(f'Adding object {obj_str}')
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
                self.log('Can\'t import invalid string')

        if name in self._objects:
            raise KeyError(f'Object {name} already added')

        self._objects[name] = instance
        self.log(f'Object "{self.name}" ({self.type.value}) was added')

    def remove_object(self, name: str) -> None:
        if name not in self._objects:
            raise KeyError(f'Object {name} not found')

        self._objects.pop(name)
        self.log(f'Object {name} has been removed')

    def get_object(self, name: str) -> type:
        """
        Get object by name

        Args:
            name (str): object name

        Returns:
            object
        """
        if name not in self._objects:
            self.log(f'Object {name} not found')

        return self._objects[name]

    def get_objects_list(self) -> List[object]:
        return list(self._objects.keys())

    @property
    def root(self):
        return self._root

    @property
    def config(self):
        return self._config

    @property
    def objects(self):
        return self._objects

    def __str__(self):
        return f'Objects: {self.get_objects_list()[:4]} . . .'

    def __repr__(self):
        return f'({self.__class__.__name__}) <objects: {self.get_objects_list()[:4]}, ...>'


System = SystemManager()
