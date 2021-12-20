import abc
import enum
from datetime import datetime
import functools
from types import MethodType
from typing import Union

from toolkit.utils.objects import is_debug


class Messages(enum.Enum):
    INFO = 'Info'
    WARNING = 'Warning'
    CRITICAL = 'Critical'
    ERROR = 'Error'


class LoggerException(Exception):

    def __init__(self, exc_message: str) -> None:
        self._exc_message = exc_message

    def __str__(self) -> str:
        return self._exc_message


class AbstractLogger(abc.ABC):

    def __init__(self, **kwargs) -> None:
        self._stdout: MethodType = kwargs.get('stdout', print)

    def __call__(self, *args, **kwargs):
        self.log(*args, **kwargs)

    @abc.abstractmethod
    def log(self, *args, **kwargs) -> None:
        pass


class DummyLogger(AbstractLogger):

    def log(
        self,
        message: str,
        message_type: Messages = Messages.INFO,
        do_raise: bool = False,
        debug: bool = False,
        exc_type: Exception = Exception
    ) -> None:
        timestamp: datetime.now = datetime.now().strftime('%H:%M:%S %m.%d.%Y')
        if do_raise:
            if not issubclass(exc_type, Exception):
                raise TypeError('Exception type (exc_type) is not an exception')

            exc_message: str = (
                f'[{"DEBUG |" if debug else ""}{timestamp} | '
                f'{message_type.value + "]":<10} {exc_type}, {message}'
            )
            raise LoggerException(exc_message)

        self._stdout(f'[{"DEBUG |" if debug else ""}{timestamp} | {message_type.value + "]":<10} {message}')

    def __call__(self, method):
        self.log(f'Method "{method.__qualname__}" was called', Messages.INFO)
