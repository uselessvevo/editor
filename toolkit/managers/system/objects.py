import enum
import uuid
from typing import List

import anytree
from anytree import TreeError, RenderTree

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


class SystemConfigCategories(enum.Enum):
    # Can share data publicly
    PUBLIC = 'public'

    # Can share data inside a package
    SHARED = 'shared'

    # Private, protected data
    PROTECTED = 'protected'

    # Etc.
    UNSPECIFIED = 'unspecified'


class SystemObject(anytree.NodeMixin):
    # System object name
    name: str = None

    # Node settings
    parent_name: str = None

    # System object type
    type: SystemObjectTypes = SystemObjectTypes.UNSPECIFIED

    # System configuration key. Gives access to configuration
    section: SystemConfigCategories = SystemObjectTypes.UNSPECIFIED

    # Just a logger
    logger: type = DummyLogger

    def __init__(self, *args, **kwargs) -> None:
        # Node settings
        self.id = uuid.uuid4()
        self.separator = '.'
        self.logger = kwargs.get('logger', self.logger)()

        if not self.name:
            self.name = self.__class__.__name__
            self.log(f'System attribute "name" was not set. '
                     f'Will be set with default class name "{self.name}"', MessageTypes.WARNING)

        if self.type is SystemObjectTypes.UNSPECIFIED:
            self.type = SystemObjectTypes.UNSPECIFIED
            self.log(f'System attribute "type" was not set. '
                     f'Will be set with default type "{self.type}"', MessageTypes.WARNING)

        if self.section is SystemConfigCategories.UNSPECIFIED:
            self.log('System attribute "section" was not set. '
                     'Will not be able to get access to System configuration', MessageTypes.WARNING)

        # Init node
        super().__init__(*args, **kwargs)

    # Public methods

    def log(self, message: str, message_type: MessageTypes = MessageTypes.INFO, **kwargs) -> None:
        self.logger.log(message=message, message_type=message_type, **kwargs)

    def add_to_parent_node(self, parent: object, children: List[object]) -> None:
        try:
            parent.children = children
            self.log(f'Object "{parent.name}" was set as parent for "{self.name}"')
            self.log(RenderTree(parent))
        except TreeError:
            self.log(f'Can\'t set parent node', MessageTypes.CRITICAL)

    def __repr__(self) -> str:
        return f'({self.__class__.__name__}) <id: {self.id}, name: {self.name!r}, type: {self.type.value!r}>'
