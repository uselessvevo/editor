import enum
import inspect
import types
import typing
import uuid
from typing import Tuple

from toolkit.logger import Messages
from toolkit.logger import DummyLogger


class SystemObjectTypes(enum.Enum):
    # Managers
    CORE_MANAGER = 'core_manager'
    PLUGIN_MANAGER = 'plugin_manager'

    # Objects
    OBJECT = 'object'
    PLUGIN = 'plugin'
    UTILITY = 'utility'

    # Etc.
    UNSPECIFIED = 'unspecified'


class SystemConfigCategories(enum.Enum):
    # Can share data with any object
    PUBLIC = 'public'

    # Can share data inside a package
    SHARED = 'shared'

    # Private, protected data
    PROTECTED = 'protected'


class SystemObject:
    # Object name
    name: str = None

    # Allowance policy
    type: SystemObjectTypes = None
    allowed_types: Tuple[SystemObjectTypes] = ()

    # System configuration key. Gives access to configuration
    section: str = None
    config_access: SystemConfigCategories = None

    # Just a logger
    logger: type = DummyLogger

    def __init__(self, *args, **kwargs) -> None:
        # Node settings
        self.id: uuid.UUID = uuid.uuid4()
        # self._hooked_methods: typing.Set[types.MethodType] = set()
        self.logger: type = kwargs.get('logger', self.logger)()

        if not self.name:
            self.name = self.__class__.__name__
            self.log(f'Object attribute "name" was not set. '
                     f'Will be set with default class name "{self.name}"', Messages.WARNING)

        if not self.type:
            self.type = SystemObjectTypes.UNSPECIFIED
            self.log(f'Object attribute "type" for object "{self.name}" was not set. '
                     f'Will be set with default type "{self.type.name}"', Messages.WARNING)

        if not self.config_access:
            self.config_access = SystemConfigCategories.PROTECTED
            self.log(f'Object attribute "config_access" in object "{self.name}" is None. '
                     f'Will be set with default type "{self.config_access.name}"', Messages.WARNING)

        if not self.section:
            self.log(f'Object attribute "section" in object "{self.name}" was not set. '
                     'Will not be able to get access to object\'s configuration', Messages.WARNING)

        # Collect methods to create hooks
        self._hook_methods(['init', '_hook_methods'], '_logger_hook')
        super().__init__(*args, **kwargs)

    # Private methods

    def _hook_methods(self, ignored: typing.List[typing.AnyStr], hook: str):
        """ Creates hooks for methods with given method call """
        methods = [i for i in inspect.getmembers(self)
                   if inspect.ismethod(i[1])
                   and not i[0].startswith('__')
                   and not i[0].endswith('__')
                   and i[0] not in ignored]

        for name, method in methods:
            setattr(self, name, getattr(self, hook)(method))

    def _logger_hook(self, method: types.MethodType):
        self.logger(method, f'Method "{self.name}.{method.__name__}" was called', Messages.INFO)

    # Public methods

    def init(self, *args, **kwargs) -> None:
        self.log(f'Initializing object "{self.name}"')

    def log(self, message: str, message_type: Messages = Messages.INFO, **kwargs) -> None:
        self.logger.log(message=message, message_type=message_type, **kwargs)

    # Hooks

    def __str__(self) -> str:
        return f'{self.name} ({self.id})'

    def __repr__(self) -> str:
        return f'({self.__class__.__name__}) <id: {self.id}, name: {self.name!r}, type: {self.type.value!r}>'
