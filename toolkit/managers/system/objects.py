import enum
from toolkit.logger import DummyLogger
from toolkit.logger import MessageTypes


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


class SystemConfigCategories:
    # Configuration keys

    # Can share data publicly
    PUBLIC = 'public'

    # Can share data inside a package
    SHARED = 'shared'

    # Private, protected data
    PROTECTED = 'protected'


class SystemObject:
    # System object name
    name: str = None

    # System object type
    type: SystemObjectTypes = SystemObjectTypes.UNSPECIFIED

    # System configuration key. Gives access to configuration
    section: str = None

    # Just a logger
    logger: type = DummyLogger

    def __init__(self, *args, **kwargs) -> None:
        self.logger = kwargs.get('logger', self.logger)()

        if not self.name:
            self.log(f'System attribute "name" was not set. Will be set with default class name', MessageTypes.WARNING)
            self.name = self.__class__.__name__

        if not self.type:
            self.log(f'System attribute "type" was not set. Will be set with default type', MessageTypes.WARNING)
            self.type = SystemObjectTypes.UNSPECIFIED

        if not self.section:
            self.log('System attribute "section" was not set. '
                     'Will not be able to get access to System configuration', MessageTypes.WARNING)

    def log(self, message: str, message_type: MessageTypes = MessageTypes.INFO, **kwargs) -> None:
        self.logger.log(message=message, message_type=message_type, **kwargs)

    def __repr__(self) -> str:
        return f'({self.__class__.__name__}) <hash: {self.__hash__()} name: {self.name} type: {self.type.value}>'
