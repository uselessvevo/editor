from pathlib import Path

from toolkit.objects.system import SystemObject
from toolkit.managers.system.manager import System


class Project(SystemObject):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._path = System.config.get()

    def init(self, *args, **kwargs) -> None:
        pass

    @property
    def path(self) -> Path:
        return self._path

    @path.setter
    def path(self, path: str) -> None:
        self._path = Path(path)
