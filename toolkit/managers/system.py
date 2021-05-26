#   Copyright @ Crab Dudes Developers
#   Licensed under the terms of the MIT license
#   File system.py - 07.03.2021, 16:40
import os
import glob
from typing import List
from dotty_dict import Dotty

from toolkit.utils.files import read_configs
from toolkit.utils.files import read_json
from toolkit.utils.files import update_json
from toolkit.utils.objects import import_string


class SystemConfig(Dotty):

    def __init__(self, defaults: dict = None):
        dictionary = {}
        if defaults:
            dictionary.update(**defaults)

        super().__init__(dictionary=dictionary)

    def get(self, key, default=None, default_key=None):
        if default_key:
            default = super().get(default_key, default)
        return super().get(key) or default

    def set(self, key, value):
        self[key] = value

    def save(self, key):
        """
        Args:
            key (str): f.e. 'dictionary.nested.key'

        Returns:
            None
        """
        file = self.get(f'{key}.__file__')
        if not file:
            raise FileNotFoundError(f'File or section "{key}.__file__" does not exist')

        update_json(key, self[key])

    def from_json_file(self, file, **kwargs):
        self._dictionary.update(**read_json(file, **kwargs))

    def __repr__(self):
        return f'({self.__class__.__name__}) <items: {list(self._data.keys())[:2]}>'


class SystemManager:
    """
    System is the core manager
    Provides easy access to instances, settings and etc.
    """

    version = '0.0.1'
    config_class = SystemConfig

    def __init__(self):
        self._root = None
        self._objects = {}
        self._config = self.config_class(defaults=read_configs(glob.glob('configs/*.json')))
        print(f'* * * * Starting system {self.version}')

    def set_system_root(self, root):
        """
        Args:
            root (str): project root path

        Returns:
            None
        """
        if not os.path.exists(root):
            raise FileNotFoundError('File or path not found')

        if os.path.isfile(root):
            print(f'* * * * Root set to {root}')
            self._root = os.path.split(root)[0]

    def init_objects(self):
        for key, instance in self._objects.items():
            print(f'* * * * Init object {instance}')
            self._objects[key] = instance()

    def add_objects(self, *objects: str):
        objects = [i for i in objects if i in objects]

        for obj_str in objects:
            print(f'* * * * Adding object {obj_str}')
            self.add_object(*import_string(obj_str))

    def add_object(self, instance: type, name: str) -> None:
        """
        Args:
            instance (type): object that will be added
            name (str): object key name
        """
        if name in self._objects:
            raise KeyError(f'Object {name} already added')

        self._objects[name] = instance
        print(f'* * * * Object {name}/{instance} added')

    def remove_object(self, name: str) -> None:
        if name not in self._objects:
            raise KeyError(f'Object {name} not found')

        del self._objects[name]
        print(f'* * * * Object {name} has been removed')

    def get_object(self, name: str) -> type:
        """
        Get object by name

        Args:
            name (str): object name

        Returns:
            object
        """
        if name not in self._objects:
            raise KeyError(f'Object {name} not found')

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
        return f'<{self.get_objects_list()}>'

    def __repr__(self):
        return f'({self.__class__.__name__}) <objects: {self.get_objects_list()[:5]}>'


System = SystemManager()


def prepare_plugins(plugin_folder: str = 'plugins'):
    config_files = [glob.glob(f'{plugin_folder}/{i}/{i}/configs/*.json') for i in os.listdir(plugin_folder)]
    config_files = read_configs(*config_files)
    System.config.update(config_files)

    manifest_data = read_json(f'{plugin_folder}/manifest.json')
    plugins = [f"plugins.{i.get('exec')}" for i in manifest_data.get('plugins')]
    System.add_objects(*plugins)
