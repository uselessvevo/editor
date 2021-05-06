import math
import time

from PyQt5.Qsci import QsciLexerCustom
from PyQt5.Qt import *

from pygments import lexers, styles
from pygments.lexer import Error, Text, _TokenType


EXTRA_STYLES = {
    'monokai': {
        'background': '#272822',
        'caret': '#F8F8F0',
        'foreground': '#F8F8F2',
        'invisibles': '#F8F8F259',
        'lineHighlight': '#3E3D32',
        'selection': '#49483E',
        'findHighlight': '#FFE792',
        'findHighlightForeground': '#000000',
        'selectionBorder': '#222218',
        'activeGuide': '#9D550FB0',
        'misspelling': '#F92672',
        'bracketsForeground': '#F8F8F2A5',
        'bracketsOptions': 'underline',
        'bracketContentsForeground': '#F8F8F2A5',
        'bracketContentsOptions': 'underline',
        'tagsOptions': 'stippled_underline',
    }
}


def convert_size(size_bytes):
    if size_bytes == 0:
        return '0B'
    size_name = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f'{s} {size_name[i]}'


class ViewLexer(QsciLexerCustom):

    def __init__(self, lexer_name, style_name):
        super().__init__()

        # Lexer + Style
        self.pyg_style = styles.get_style_by_name(style_name)
        self.pyg_lexer = lexers.get_lexer_by_name(lexer_name, stripnl=False)
        self.cache = {
            0: ('root',)
        }
        self.extra_style = EXTRA_STYLES[style_name]

        # Generate QScintilla styles
        self.font = QFont('Iosevka', 12, weight=QFont.Bold)
        self.token_styles = {}
        index = 0
        for k, v in self.pyg_style:
            self.token_styles[k] = index
            if v.get('color', None):
                self.setColor(QColor(f"#{v['color']}"), index)
            if v.get('bgcolor', None):
                self.setPaper(QColor(f"#{v['bgcolor']}"), index)

            self.setFont(self.font, index)
            index += 1

    def defaultPaper(self, style):
        return QColor(self.extra_style['background'])

    def language(self):
        return self.pyg_lexer.name

    def getTokensUnprocessed(self, text, stack=('root',)):
        """
        Split ``text`` into (tokentype, text) pairs.

        ``stack`` is the inital stack (default: ``['root']``)
        """
        lexer = self.pyg_lexer
        pos = 0
        tokendefs = lexer._tokens
        statestack = list(stack)
        statetokens = tokendefs[statestack[-1]]
        while 1:
            for rexmatch, action, new_state in statetokens:
                m = rexmatch(text, pos)
                if m:
                    if action is not None:
                        if type(action) is _TokenType:
                            yield pos, action, m.group()
                        else:
                            for item in action(lexer, m):
                                yield item
                    pos = m.end()
                    if new_state is not None:
                        # state transition
                        if isinstance(new_state, tuple):
                            for state in new_state:
                                if state == '#pop':
                                    statestack.pop()
                                elif state == '#push':
                                    statestack.append(statestack[-1])
                                else:
                                    statestack.append(state)
                        elif isinstance(new_state, int):
                            # pop
                            del statestack[new_state:]
                        elif new_state == '#push':
                            statestack.append(statestack[-1])
                        else:
                            assert False, 'wrong state def: %r' % new_state
                        statetokens = tokendefs[statestack[-1]]
                    break
            else:
                # We are here only if all state tokens have been considered
                # and there was not a match on any of them.
                try:
                    if text[pos] == '\n':
                        # at EOL, reset state to 'root'
                        statestack = ['root']
                        statetokens = tokendefs['root']
                        yield pos, Text, u'\n'
                        pos += 1
                        continue
                    yield pos, Error, text[pos]
                    pos += 1
                except IndexError:
                    break

    def highlightSlow(self, start, end):
        style = self.pyg_style
        view = self.editor()
        code = view.text()[start:end]
        tokensource = self.getTokensUnprocessed(code)

        self.startStyling(start)
        for _, ttype, value in tokensource:
            self.setStyling(len(value), self.token_styles[ttype])

    def styleText(self, start, end):
        view = self.editor()
        t_start = time.time()
        self.highlightSlow(start, end)
        t_elapsed = time.time() - t_start
        len_text = len(view.text())
        text_size = convert_size(len_text)
        view.setWindowTitle(f'Text size: {len_text} - {text_size} Elapsed: {t_elapsed}s')

    def description(self, style_nr):
        return str(style_nr)
