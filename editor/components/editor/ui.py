from pathlib import Path

from PyQt5 import Qsci
from PyQt5.Qt import *

from components.editor.lexer import ViewLexer
from toolkit.managers import System


class Editor(Qsci.QsciScintilla):

    ARROW_MARKER_NUM = 8

    def __init__(self, parent=None):
        super(Editor, self).__init__(parent=parent)

        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        self.setMarginsFont(font)

        fontMetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontMetrics.width('00000') + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor('cccccc'))

        self.setMarginSensitivity(1, True)
        self.marginClicked.connect(self.onMarginClicked)
        self.markerDefine(Qsci.QsciScintilla.RightArrow, self.ARROW_MARKER_NUM)
        self.setMarkerBackgroundColor(QColor('#ee1111'), self.ARROW_MARKER_NUM)

        # -------- Lexer --------
        self.setEolMode(Qsci.QsciScintilla.EolUnix)
        self.lexer = ViewLexer()
        self.setLexer(self.lexer)

        # -------- Shortcuts --------
        self.text_size = 1
        self.s1 = QShortcut('ctrl+1', self, self.reduceTextSize)
        self.s2 = QShortcut('ctrl+2', self, self.increaseTextSize)

        self.setMarginSensitivity(1, True)
        self.marginClicked.connect(self.onMarginClicked)

        # # -------- Multiselection --------
        self.SendScintilla(self.SCI_SETMULTIPASTE, 1)
        self.SendScintilla(self.SCI_SETVSCROLLBAR, True)
        self.SendScintilla(self.SCI_SETHSCROLLBAR, 0)
        self.SendScintilla(self.SCI_SETMULTIPLESELECTION, True)
        self.SendScintilla(self.SCI_SETADDITIONALSELECTIONTYPING, True)
        self.SendScintilla(self.SCI_SETTABWIDTH, 4)

        # -------- Extra settings --------
        self.setExtraSettings(System.get_object('AssetsManager').theme)

    def getLineSeparator(self):
        m = self.eolMode()
        if m == Qsci.QsciScintilla.EolWindows:
            eol = '\r\n'

        elif m == Qsci.QsciScintilla.EolUnix:
            eol = '\n'

        elif m == Qsci.QsciScintilla.EolMac:
            eol = '\r'

        else:
            eol = ''

        return eol

    def setExtraSettings(self, settings):
        self.setIndentationGuidesBackgroundColor(QColor(0, 0, 255, 0))
        self.setIndentationGuidesForegroundColor(QColor(0, 255, 0, 0))

        if 'caret' in settings:
            self.setCaretForegroundColor(QColor(settings['caret']))

        if 'line_highlight' in settings:
            self.setCaretLineBackgroundColor(QColor(settings['line_highlight']))

        if 'brackets_background' in settings:
            self.setMatchedBraceBackgroundColor(QColor(settings['brackets_background']))

        if 'brackets_foreground' in settings:
            self.setMatchedBraceForegroundColor(QColor(settings['brackets_foreground']))

        if 'selection' in settings:
            self.setSelectionBackgroundColor(QColor(settings['selection']))

        if 'background' in settings:
            color = QColor(settings['background'])
            self.resetFoldMarginColors()
            self.setFoldMarginColors(color, color)

    def increaseTextSize(self):
        self.text_size *= 2
        self.genText()

    def reduceTextSize(self):
        if self.text_size == 1:
            return

        self.text_size //= 2
        self.genText()

    def genText(self):
        content = Path(__file__).read_text()
        while len(content) < self.text_size:
            content *= 2
        self.setText(content[:self.text_size])

    def onMarginClicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)
