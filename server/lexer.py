"""lexer is a module that contains the Lexer class, which is used to tokenize the input script

Typical usage example:

lexer = Lexer()
lexer.load_script(script)
"""
from ply.lex import lex
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Lexer:
    """Lexer is for tokenizing the input script
    
    Attributes:
        _lexer: the lexer object
        input: the input target
    """

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
        """init the lexer
        
        Attributes:
            _lexer: the lexer object
            input: the input target
        """
        self._lexer = lex(module=self)
        self._input = None

    def get_lexer(self):
        """get the lexer object
        
        Returns:
            the lexer object
        """
        return self._lexer

    def load_str(self, input):
        """load the input string
        
        Args:
            input: the input string
        """
        self._input = input
        self._lexer.input(input)
        self._lexer.lineno = 1

    def load_script(self, path):
        """load the script file
           
        Args:
            path: the script file path
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
        """get the next token
        
        Returns:
            the next token tokenized
            
        Raises:
            SyntaxError: if the input is illegal
            RuntimeError: if the input is not loaded
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
        t.value = t.value[1:]    # remove the $
        return t

    def t_STR(self, t):
        r'"[^"]*"'
        t.value = t.value[1:-1]
        return t

    def t_error(self, t):
        t.lexer.skip(1)
        raise SyntaxError(f'Illegal character {t.value[0]}')



if __name__ == "__main__":
    lexer = Lexer()
    lexer.load_script("script/bank_service.txt")
    token = lexer.token()
    while token:
        print(token)
        token = lexer.token()
