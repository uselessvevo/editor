import logging

# Qt
from PyQt5.QtWidgets import QLabel

# Utils
from toolkit.utils.themes import textParser


class RichLabel(QLabel):
    def __init__(self, parent=None):
        """
        Args:
            parent (object) - object prepare methods in _linkWrapper
        """
        super(RichLabel, self).__init__()
        self._parent = parent
        self.__view = []
        self.__methods = {}
        self.linkActivated.connect(self._linkWrapper)

    def addText(self, text):
        self.__view.append(textParser('<br>'.join(text)))
        self.setText('<br>'.join(self.__view))

    def addMethod(self, key, method, *args, **kwargs):
        """
        Args:
            key (str) - method key (#tag)
            method (str) - method name
            args and kwargs for method attributes
        >>> label = RichLabel(self)
        >>> label.addText('Click on @(method;methodA_key) or @(this;methodB_key)')
        >>> label.addMethod('methodA_key', 'methodA', args, kwargs)
        """
        if key in self.__view:
            self.log.warning(f'Key "{key}" already exists!')
        self.__methods[key] = {'name': method, 'args': args, 'kwargs': kwargs}

    def _linkWrapper(self, link):
        try:
            name = self.__methods[link]['name']
            args = self.__methods[link]['args']
            kwargs = self.__methods[link]['kwargs']
            getattr(self._parent, name)(*args, **kwargs)
        except (KeyError, AttributeError):
            logging.warning('Key "{link}" doesn\'t exist')
