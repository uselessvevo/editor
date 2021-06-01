import math
import importlib
import importlib.util

from PyQt5.Qt import *
from PyQt5.Qsci import QsciLexerCustom

from pygments import lexers
from pygments import styles
from pygments.lexer import Text
from pygments.lexer import Error
from pygments.lexer import _TokenType

from toolkit.managers import System
from toolkit.utils.files import read_json


def convert_size(size_bytes):
    if size_bytes == 0:
        return '0B'
    size_name = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f'{s} {size_name[i]}'


class LexerNotFound(Exception):
    pass


class ViewLexer(QsciLexerCustom):

    def __init__(self):
        super().__init__()

        # Lexer + Style
        assets = System.get_object('AssetsManager')
        lexer = System.config.get('configs.editor.current_lexer')
        if not lexer:
            raise LexerNotFound()

        self.cache = {0: ('root',)}
        self.pyg_style = self.getEditorStyle(assets.theme_folder)
        # self.pyg_style = styles.get_style_by_name('monokai')
        self.pyg_lexer = lexers.get_lexer_by_name(lexer, stripnl=False)
        self.extra_style = read_json(assets.theme_folder / 'editor/style.json').get('extra')

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

    def getEditorStyle(self, theme_folder):
        spec = importlib.util.spec_from_file_location(
            name='style',
            location=theme_folder / 'editor/style.py'
        )
        style = read_json(theme_folder / 'editor/style.json').get('style')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        module = getattr(module, 'EditorStyle')
        for k, v in module.styles.items():
            val = style.get(str(k))
            module.styles[k] = val

        return module

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

        token_defs = lexer._tokens
        state_stack = list(stack)
        state_tokens = token_defs[state_stack[-1]]

        while 1:
            for rex_match, action, new_state in state_tokens:
                m = rex_match(text, pos)
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
                                    state_stack.pop()

                                elif state == '#push':
                                    state_stack.append(state_stack[-1])

                                else:
                                    state_stack.append(state)
                        elif isinstance(new_state, int):
                            # pop
                            del state_stack[new_state:]

                        elif new_state == '#push':
                            state_stack.append(state_stack[-1])

                        else:
                            assert False, 'wrong state def: %r' % new_state
                        state_tokens = token_defs[state_stack[-1]]
                    break
            else:
                # We are here only if all state tokens have been considered
                # and there was not a match on any of them.
                try:
                    if text[pos] == '\n':
                        # at EOL, reset state to 'root'
                        state_stack = ['root']
                        state_tokens = token_defs['root']
                        yield pos, Text, u'\n'
                        pos += 1
                        continue
                    yield pos, Error, text[pos]
                    pos += 1
                except IndexError:
                    break

    def highlightSlow(self, start, end):
        view = self.editor()
        code = view.text()[start:end]
        token_source = self.getTokensUnprocessed(code)

        self.startStyling(start)
        for _, ttype, value in token_source:
            self.setStyling(len(value), self.token_styles[ttype])

    def styleText(self, start, end):
        self.highlightSlow(start, end)

    def description(self, style_nr):
        return str(style_nr)
