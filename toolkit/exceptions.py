"""
Exceptions
"""


class ProtectedSystemSectionKey(KeyError):

    def __init__(self, section: str):
        self._section = section

    def __str__(self) -> str:
        return self._section
