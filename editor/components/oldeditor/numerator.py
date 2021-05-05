#!/usr/bin/python3
# QcodeEditor.py by acbetter.
# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5 import QtWidgets


class QLineNumerator(QtWidgets.QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QtCore.QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)
