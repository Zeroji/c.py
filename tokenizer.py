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
        escape = False
        for i, line in enumerate(self.file):
            for j, c in enumerate(line):
                if c == '\\':
                    escape = True
                    continue
                if escape:
                    if c in ESCAPE_SEQUENCES:
                        c = ESCAPE_SEQUENCES[c]
                    token += c
                    escape = False
                    continue
                if c == quotes:
                    token += c
                    quotes = False
                    add()
                    continue
                elif quotes:
                    token += c
                    continue
                elif c in '\'\"':
                    quotes = c
                    new(c)
                    continue
                if c in ' \t':
                    new('')
                    continue
                if token is None:
                    new('')
                token += c
