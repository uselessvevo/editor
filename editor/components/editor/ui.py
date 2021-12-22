import keyword
import pkgutil

from PyQt5 import Qsci, QtGui
from PyQt5.Qt import *

from editor.components.editor.lexer import ViewLexer

from toolkit.managers.system.manager import System
from toolkit.utils.files import read_json
from toolkit.objects.system import SystemObject, SystemObjectTypes


class Editor(SystemObject, Qsci.QsciScintilla):
    ARROW_MARKER_NUM = 8
    name = 'main_ui.editor'
    parent_name = 'main_ui'
    type = SystemObjectTypes.PLUGIN

    def init(self, *args, **kwargs):
        self.prepareMainSettings()
        self.prepareLexer()
        self.prepareAutocompletition()
        self.prepareWraping()
        self.prepareEdgeMarker()
        self.prepareIndent()
        self.prepareCaret()
        self.setExtraSettings()

    def prepareMainSettings(self):
        font = QFont()
        font.setFamily('JetBrains Mono')
        font.setFixedPitch(False)
        font.setPointSize(10)

        self.setFont(font)
        self.setMarginsFont(font)
        self.setEolVisibility(System.config.get('app.eol_visibility', default_value=False))
        self.zoomTo(4)

        self.setMarginSensitivity(1, True)
        self.marginClicked.connect(self.onMarginClicked)

    def prepareWraping(self):
        # Set the text wrapping mode to word wrap
        self.setWrapMode(Qsci.QsciScintilla.WrapWord)

        # Set the text wrapping mode visual indication
        self.setWrapVisualFlags(Qsci.QsciScintilla.WrapFlagByText)

        # Set the text wrapping to indent the wrapped lines
        self.setWrapIndentMode(Qsci.QsciScintilla.WrapIndentSame)

    def prepareEdgeMarker(self):
        # Set the edge marker's position and set it to color the background
        # when a line goes over the limit of 50 characters
        self.setEdgeMode(Qsci.QsciScintilla.EdgeBackground)
        self.setEdgeColumn(50)
        edge_color = QtGui.QColor(System.config.get('app.edge_color', default_value='ff00ff00'))
        self.setEdgeColor(edge_color)

    def prepareIndent(self):
        # Set indentation with spaces instead of tabs
        self.setIndentationsUseTabs(System.config.get('app.indent.use_tabs', default_value=False))

        # Set the tab width to 4 spaces
        self.setTabWidth(System.config.get('app.indent.tab_width', default_value=4))

        # Set tab indent mode, see the 3.3.4 chapter in QSciDocs
        # for a detailed explanation
        self.setTabIndents(System.config.get('app.indent.tab_indents', default_value=True))

        # Set autoindentation mode to maintain the indentation
        # level of the previous line (the editor's lexer HAS
        # to be disabled)
        self.setAutoIndent(System.config.get('app.indent.auto_indent', default_value=True))

        # Make the backspace jump back to the tab width guides
        # instead of deleting one character, but only when
        # there are ONLY whitespaces on the left side of the
        # cursor
        self.setBackspaceUnindents(System.config.get('app.indent.backspace_unindents', default_value=True))

        # Set indentation guides to be visible
        self.setIndentationGuides(System.config.get('app.indent.indentation_guides', default_value=True))

    def prepareCaret(self):
        # Set the caret color to red
        caret_fg_color = QtGui.QColor(System.config.get('app.caret_fg_color'))
        self.setCaretForegroundColor(caret_fg_color)

        # Enable and set the caret line background color to slightly transparent blue
        # self.setCaretLineVisible(True)
        caret_bg_color = QtGui.QColor(System.config.get('app.caret_bg_color'))
        self.setCaretLineBackgroundColor(caret_bg_color)

        # Set the caret width of 4 pixels
        self.setCaretWidth(System.config.get('app.caret_width', default_value=4))

    def prepareLexer(self):
        # lexer = Qsci.QsciLexerPython(self)
        lexer = ViewLexer(self)
        lexer.init()

        self.setLexer(lexer)
        self.api = Qsci.QsciAPIs(lexer)

        # TEST

        for key in keyword.kwlist + dir(__builtins__):
            self.api.add(key)

        for importer, name, ispkg in pkgutil.iter_modules():
            self.api.add(name)

        self.api.prepare()

    def prepareAutocompletition(self):
        # Set the autocompletions to case INsensitive
        self.setAutoCompletionCaseSensitivity(False)

        # Set the autocompletion to not replace the word to the right of the cursor
        # self.setAutoCompletionReplaceWord(False)

        # Set the autocompletion dialog to appear as soon as 1 character is typed
        self.setAutoCompletionThreshold(1)

        # Set the autocompletion source to be the words in the API
        self.setAutoCompletionSource(Qsci.QsciScintilla.AcsAPIs)

    def prepareShortcuts(self):
        self.text_size = 1
        self.reduceTextSizeShortcut = QShortcut('Ctrl+-', self, self.reduceTextSize)
        self.increaseTextSizeShortcut = QShortcut('Ctrl+=', self, self.increaseTextSize)

    def prepareScintilaSignals(self):
        self.SendScintilla(self.SCI_SETMULTIPASTE, 1)
        self.SendScintilla(self.SCI_SETVSCROLLBAR, True)
        self.SendScintilla(self.SCI_SETHSCROLLBAR, 0)
        self.SendScintilla(self.SCI_SETMULTIPLESELECTION, True)
        self.SendScintilla(self.SCI_SETADDITIONALSELECTIONTYPING, True)
        self.SendScintilla(self.SCI_SETTABWIDTH, 4)

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

    def setExtraSettings(self):
        settings = read_json(System.get_object('AssetsManager').theme_folder / 'editor/style.json').get('extra')
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

    def reduceTextSize(self):
        if self.text_size == 1:
            return

        self.text_size //= 2

    def onCursorChangePosition(self, event):
        return

    def onMarginClicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)
