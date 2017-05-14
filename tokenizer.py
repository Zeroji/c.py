import string

TWO_CHAR_OPS = ('+=', '-=', '*=', '/=', '%=', '++', '--', '&&', '||', '==', '!=', '>=', '<=', '>>', '<<')
ESCAPE_SEQUENCES = {'a': '\a', 'b': '\b', 'f': '\f', 'n': '\n', 'r': '\r', 't': '\t', 'v': '\v', '0': '\x00'}


class Tokenizer:
    def __init__(self, file):
        self.file = file
        self.tokens = []

    def parse(self):
        token = None

        def new(tok):
            nonlocal token, word, number
            if token is not None and token != '':
                self.tokens.append(token)
            token = tok
            word = False
            number = False

        def add():
            new(None)

        quotes = ''
        quotes_pos = None
        escape = False
        word = False
        number = False
        for i, line in enumerate(self.file):
            preprocessor = False
            empty = True
            for j, c in enumerate(line):
                if empty and c == '#':  # Handling preprocessor directives as a single token
                    preprocessor = True
                    empty = False
                    new(c)
                    continue
                if preprocessor:
                    token += c
                    continue
                if c not in string.whitespace:
                    empty = False
                if c == '\\':  # Escape character
                    escape = True
                    continue
                if escape:  # Escape sequences
                    if c in ESCAPE_SEQUENCES:
                        c = ESCAPE_SEQUENCES[c]
                    token += c
                    escape = False
                    continue
                if c == quotes:  # Closing quotes
                    token += c
                    quotes = False
                    add()
                    continue
                elif quotes:  # Continuing quotes
                    token += c
                    continue
                elif c in '\'\"':  # Opening quotes
                    quotes = c
                    new(c)
                    quotes_pos = (i, j)
                    continue
                if c in string.digits:
                    if not number:
                        if token not in ('-', '+'):  # Allowing +1 and -1
                            new(c)
                        number = True
                    else:
                        token += c
                    continue
                elif c in ('x', 'o', 'b') and number and token in ('0', '+0', '-0'):  # hexa, octal, bin
                    token += c
                    continue
                elif c == '.' and number:  # Floating point
                    token += c
                    continue
                elif c in ('e', 'E') and number:  # Exponent
                    token += c
                    continue
                elif c in ('+', '-') and number and token[-1] in ('e', 'E'):  # Signed exponent
                    token += c
                    continue
                elif number:
                    add()
                if c in string.ascii_letters + '_' + string.digits + ('./' if preprocessor else ''):
                    if not word:
                        new(c)
                        word = True
                    else:
                        token += c
                    continue
                elif word:
                    add()
                if token is not None and (token + c) in TWO_CHAR_OPS:
                    token += c
                    add()
                    continue
                if c in ' \t':  # Basic whitespace splitting
                    new('')
                    continue
                if token is None:  # Basic token creation
                    new('')
                token += c
            if quotes and not escape:
                self.file.error("Unmatched `{quote}'".format(quote=quotes), quotes_pos)
                return False
            if not escape:
                add()
        return True
