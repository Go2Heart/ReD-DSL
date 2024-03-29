"""yacc is a parser generator for ReD-DSL.

Typical usage example:
parser = Parser(lexer)
parser.parse(script)
"""
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ply.yacc import yacc
from server.lexer import Lexer


class ASTNode:
    """Abstract syntax tree node
    
    Attributes:
        type: the type of the node
        childs: the child nodes
    """

    def __init__(self, type, *child):
        """init the AST node
        
        Args:
            type: the type of the node
            childs: the child nodes
        """
        self.type = type
        self.childs = list(child)

    def __str__(self):
        """return the string representation of the AST"""
        if self != None:
            return str(self.type)
    
    def __repr__(self):
        """return the string representation of the AST"""
        if self.childs:
            return str(self.type) + "(" + ", ".join([repr(child) for child in self.childs]) + ")"
        else:
            return str(self.type)
    
    def print(self, indent=1):
        """print the AST
        
        Args:
            indent: the indent of the current node
        """
        out = " " * (indent - 1) * 4 + "└──" + " " + str(self)
        print(out)
        for child in self.childs:
            child.print(indent + 1)


class Parser:
    """Parse the script and return the AST
    
    Attributes:
        _lexer: the lexer
        tokens: the tokens
        _yacc: the yacc parser
        debug: the debug mode
    """

    def __init__(self, lexer: Lexer, debug=False):
        """init the parser"""
        self._lexer = lexer
        self.tokens = lexer.tokens
        self._yacc = yacc(module=self, debug=debug)
        self.debug = debug

    def parse(self, script):
        """parse a script
        
        Args:
            script: the script to parse
            
        Returns:
            the AST of the script
            
        Raises:
            SyntaxError: if the script is not valid
        """
        return self._yacc.parse(script, self._lexer.get_lexer())

    start = 'script'

    def p_script(self, p):
        '''
        script : SCRIPT ID variables states
        '''
        p[0] = ASTNode(('script', p[2]), p[3], p[4])

    def p_variables(self, p):
        '''
        variables : VARIABLE vars ENDVARIABLE
        '''
        p[0] = ASTNode(('variables'), *p[2])
        if (self.debug):
            print("variables: ", p[0].childs)

    def p_vars(self, p):
        '''
        vars : var
                | vars var
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]
        if self.debug:
            print("vars: ", *p[0])

    def p_var(self, p):
        '''
        var : ID REAL VAR
                | ID INTEGER VAR
                | ID TEXT STR
        '''
        p[0] = ASTNode(('var', p[1], p[2], p[3]))

    def p_states(self, p):
        '''
        states : state
                | states state
        '''
        if len(p) == 2:
            # p[0] = [p[1]]
            p[0] = ASTNode('states', p[1])
        else:
            # p[0] = p[1] + [p[2]]
            p[0] = ASTNode('states', *p[1].childs, p[2])

    def p_state(self, p):
        '''
        state : STATE ID expressions ENDSTATE
        '''
        p[0] = ASTNode(('state', p[2]), *p[3])  # where p[3] is a list of expression AST Nodes.

    def p_expressions(self, p):
        '''
        expressions : expression
                    | expressions expression
        '''
        if len(p) == 2:
            p[0] = [p[1]]  # where p[1] is an expression AST Node.
        else:
            p[0] = p[1] + [p[2]]

    def p_expression(self, p):
        '''
        expression : switch
                    | speak
                    | goto
                    | timeout
                    | exit
                    | update
        '''
        p[0] = p[1]

    def p_update(self, p):
        '''
        update : UPDATE ID '=' terms
        '''
        p[0] = ASTNode(('update', p[2]), p[4])

    def p_switch(self, p):
        '''
        switch : SWITCH cases default
        '''
        p[0] = ASTNode('switch', *p[2], p[3])

    def p_cases(self, p):
        '''
        cases : case
                | cases case
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_case(self, p):
        '''
        case : CASE STR expressions 
                | CASE RETURN expressions
                | CASE compare expressions
        '''
        if isinstance(p[2], ASTNode):
            p[0] = ASTNode(('case', p[2].type), *p[3])
        else:
            p[0] = ASTNode(('case', p[2]), *p[3])

    def p_condition(self, p):
        '''
            compare : ID '>' term
                    | ID '<' term
                    | ID LESS_EQUAL term
                    | ID GREATER_EQUAL term
                    | RETURN '>' term
                    | RETURN '<' term
                    | RETURN LESS_EQUAL term
                    | RETURN GREATER_EQUAL term
        '''
        p[0] = ASTNode(('compare', p[1], p[2], p[3].type))

    def p_speak(self, p):
        '''
        speak : SPEAK terms
        '''
        p[0] = ASTNode('speak', p[2])

    def p_terms(self, p):
        '''
        terms : term
                | terms '+' term
                | term PLUS term
                | term MINUS term
        '''
        if len(p) == 2:
            p[0] = ASTNode('terms', p[1])
        elif p[2] == '+':
            p[0] = ASTNode('terms', *p[1].childs, p[3])
        else:
            p[0] = ASTNode(('calc', p[2]), p[1], p[3])

    def p_term_str(self, p):
        '''
        term : STR
        '''
        p[0] = ASTNode(('str', p[1]))

    def p_term_var(self, p):
        '''
        term : VAR
        '''
        p[0] = ASTNode(('var', p[1]))

    def p_term_id(self, p):
        '''
        term : ID
        '''
        p[0] = ASTNode(('id', p[1]))

    def p_term_return(self, p):
        '''
        term : RETURN
        '''
        p[0] = ASTNode(('<return>', p[1]))

    def p_goto(self, p):
        '''
        goto : GOTO ID
        '''
        p[0] = ASTNode(('goto', p[2]))

    def p_timeout(self, p):
        '''
        timeout : TIMEOUT VAR expressions ENDTIMEOUT
        '''
        p[0] = ASTNode(('timeout', p[2]), *p[3])

    def p_default(self, p):
        '''
        default : DEFAULT expressions ENDSWITCH
                    | ENDSWITCH
        '''
        if len(p) == 2:
            p[0] = ASTNode('default_empty')
        else:
            p[0] = ASTNode('default', *p[2])

    def p_exit(self, p):
        '''
        exit : EXIT
        '''
        p[0] = ASTNode('exit')

    def p_error(self, p):
        if self.debug:
            print("Syntax error in input!")
            print(p)
        raise SyntaxError


if __name__ == '__main__':
    lexer = Lexer()
    parser = Parser(lexer, debug=True)
    with open('script/mobile_fee.txt') as f:
        script = f.read()
    node = parser.parse(script)   
    print(repr(node))
    node.print()
