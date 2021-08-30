"""
Exceptions
"""


class ProtectedSystemSectionKey(KeyError):

    def __init__(self, section: str):
        self._section = section

    def __str__(self):
        return self._section
