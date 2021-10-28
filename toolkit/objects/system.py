import enum
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
    UTILITY = 'utility'

    # Applications and plugins
    PLUGIN = 'plugin'

    # Etc.
    UNSPECIFIED = 'unspecified'


class SystemConfigCategories(enum.Enum):
    # Can share data publicly
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
    config_category: SystemConfigCategories = None

    # Just a logger
    logger: type = DummyLogger

    def __init__(self, *args, **kwargs) -> None:
        # Node settings
        self.id = uuid.uuid4()
        self.logger = kwargs.get('logger', self.logger)()

        if not self.name:
            self.name = self.__class__.__name__
            self.log(f'System attribute "name" was not set. '
                     f'Will be set with default class name "{self.name}"', Messages.WARNING)

        if not self.type:
            self.type = SystemObjectTypes.UNSPECIFIED
            self.log(f'System attribute "type" for object "{self.name}" was not set. '
                     f'Will be set with default type "{self.type.name}"', Messages.WARNING)

        if not self.config_category:
            self.config_category = SystemConfigCategories.PROTECTED
            self.log(f'System attribute "config_access" in object "{self.name}" is None'
                     f'Will be set with default type "{self.config_category.name}"', Messages.WARNING)

        if not self.section:
            self.log(f'System attribute "section" in object "{self.name}" was not set. '
                     'Will not be able to get access to object\'s configuration', Messages.WARNING)

        # Init node
        super().__init__(*args, **kwargs)

    # Public methods

    def init(self, *args, **kwargs):
        self.log(f'Initializing object "{self.name}"')

    def log(self, message: str, message_type: Messages = Messages.INFO, **kwargs) -> None:
        self.logger.log(message=message, message_type=message_type, **kwargs)

    # Hooks

    def __str__(self):
        return f'{self.name} ({self.id})'

    def __repr__(self) -> str:
        return f'({self.__class__.__name__}) <id: {self.id}, name: {self.name!r}, type: {self.type.value!r}>'
