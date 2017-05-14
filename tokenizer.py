TWO_CHAR_OPS = ('+=', '-=', '*=', '/=', '%=', '++', '--', '&&', '||', '==', '!=', '>=', '<=', '>>', '<<')
ESCAPE_SEQUENCES = {'a': '\a', 'b': '\b', 'f': '\f', 'n': '\n', 'r': '\r', 't': '\t', 'v': '\v', '0': '\x00'}


class Tokenizer:
    def __init__(self, file):
        self.file = file
        self.tokens = []

    def parse(self):
        token = None

        def new(tok):
            nonlocal token
            if token is not None and token != '':
                self.tokens.append(token)
            token = tok

        def add():
            new(None)

        quotes = ''
        quotes_pos = None
        escape = False
        for i, line in enumerate(self.file):
            for j, c in enumerate(line):
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
                if c in ' \t':  # Basic whitespace splitting
                    new('')
                    continue
                if token is None:  # Basic token creation
                    new('')
                token += c
            if quotes and not escape:
                self.file.error("Unmatched `{quote}'".format(quote=quotes), quotes_pos)
                return False
        add()
        return True
