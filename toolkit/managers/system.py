#   Copyright @ Crab Dudes Developers
#   Licensed under the terms of the MIT license
#   File system.py - 07.03.2021, 16:40
import os
from typing import List
from dotty_dict import Dotty

from toolkit.utils.files import read_json
from toolkit.utils.files import read_json_files
from toolkit.utils.files import write_json
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
        write_json(key, self[key])

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
        self.root = None
        self.objects = {}
        files = read_json_files([f'config/{i}' for i in os.listdir('config')])
        self.config = self.config_class(defaults=files)

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
            self.root = os.path.split(root)[0]

    def init(self):
        for key, instance in self.objects.items():
            self.objects[key] = instance()

    def add_objects(self, *objects: str):
        objects = [i for i in objects if i in objects]

        for obj_str in objects:
            self.add_object(*import_string(obj_str))

    def add_object(self, instance: type, name: str) -> None:
        """
        Args:
            instance (type): object that will be added
            name (str): object key name
        """
        if name in self.objects:
            raise KeyError(f'Object {name} already added')

        self.objects[name] = instance

    def remove_object(self, name: str) -> None:
        if name not in self.objects:
            raise KeyError(f'Object {name} not found')

        del self.objects[name]

    def get_object(self, name: str) -> type:
        """
        Get object by name

        Args:
            name (str): object name

        Returns:
            object
        """
        if name not in self.objects:
            raise KeyError(f'Object {name} not found')

        return self.objects[name]

    def get_objects_list(self) -> List[object]:
        return list(self.objects.keys())

    def __str__(self):
        return f'<{self.get_objects_list()}>'

    def __repr__(self):
        return f'({self.__class__.__name__}) <objects: {self.get_objects_list()[:5]}>'


System = SystemManager()
