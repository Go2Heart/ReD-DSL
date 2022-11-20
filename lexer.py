from ast import keyword
from ply.lex import lex


class Lexer:

    keywords = {
        "real": "REAL",
        "integer": "INTEGER",
        "text": "TEXT",
        "variable": "VARIABLE",
        "state": "STATE",
        "switch": "SWITCH",
        "case": "CASE",
        "goto": "GOTO",
        "default": "DEFAULT",
        "timeout": "TIMEOUT",
        "script": "SCRIPT",
        "endState": "ENDSTATE",
        "endVariable": "ENDVARIABLE",
        "endSwitch": "ENDSWITCH",
        "endTimeout": "ENDTIMEOUT",
        "exit": "EXIT",
        "speak": "SPEAK",
        "_return": "RETURN",
        "update": "UPDATE",
        "PLUS": "PLUS",
        "MINUS": "MINUS",
    }
    tokens = [
        # "NEWLINE",
        "ID",
        "VAR",
        "STR",
        "LESS_EQUAL",
        "GREATER_EQUAL",
    ] + list(keywords.values())
    t_ignore = ' \t\n'

    literals = ['+', '-', '=', '>', '<']

    def __init__(self):
        """
            init the lexer
            self._lexer is the lexer object
            self._input is the input target
        """
        self._lexer = lex(module=self)
        self._input = None

    def getLexer(self):
        """
            get the lexer object
        """
        return self._lexer

    def load_str(self, input):
        """
            load the input string
            @param input: the input string
        """
        self._input = input
        self._lexer.input(input)
        self._lexer.lineno = 1

    def load_script(self, path):
        """
            load the script file
            @param path: the script file path
        """
        self._input = None
        with open(path, 'r', encoding='utf8') as f:
            self._input = f.read()
        if not self._input:
            print(f'Failed to load file {path}')
            return
        self._lexer.input(self._input)
        self._lexer.lineno = 1

    def token(self):
        """
            get the next token
        """
        if not self._input:
            raise RuntimeError('reading token before load.')
        return self._lexer.token()

    def t_LESS_EQUAL(self, t):
        r'<='
        return t

    def t_GREATER_EQUAL(self, t):
        r'>='
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.keywords.get(t.value, "ID")
        return t

    def t_VAR(self, t):
        r'\$[a-zA-Z_0-9]*'
        t.value = t.value[1:]  # remove the $
        return t

    def t_STR(self, t):
        r'"[^"]*"'
        t.value = t.value[1:-1]
        return t

    def t_error(self, t):
        raise SyntaxError(f'Illegal character {t.value[0]}')
        t.lexer.skip(1)


if __name__ == "__main__":
    lexer = Lexer()
    #lexer.load_str("test variable test $123 \"123\"")
    lexer.load_script("test.txt")
    token = lexer.token()
    while token:
        print(token)
        token = lexer.token()
