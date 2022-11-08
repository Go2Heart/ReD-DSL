from ply.yacc import yacc
from lexer import Lexer


class Node:
    """
        Abstract syntax tree node
    """
    def __init__(self, type, *child):
        self.type = type
        self.childs = list(child)
        
    def print(self, indent=0):
        """
            print the AST
        """
        print(' ' * indent, self.type)
        for child in self.childs:
            if isinstance(child, str):
                print(' ' * (indent+1), "str: ",child)
            elif isinstance(child, list):
                for c in child:
                    c.print(indent + 1)
            else:
                child.print(indent + 1)
        
class Parser:
    def __init__(self, lexer:Lexer): #TODO add config
        self._lexer = lexer
        self.tokens = lexer.tokens
        self._yacc = yacc(module=self, debug=True)
    
    def parse(self, line):
        """
            parse a line
            @param line: the line to parse
        """
        return self._yacc.parse(line, self._lexer.getLexer())
    
    start = 'script'
    def p_script(self, p):
        '''
        script : SCRIPT ID variables states
        '''
        p[0] = Node('script', p[2], p[3], *p[4])
    
    def p_variables(self, p):
        '''
        variables : VARIABLE vars
        '''
        p[0] = Node(('variables'), *p[2])
    def p_vars(self, p):
        '''
        vars : var
                | vars var
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]
    
    def p_var(self, p):
        '''
        var : ID REAL VAR
                | ID INTEGER VAR
                | ID TEXT STR
        '''
        p[0] = Node('var', p[1], p[2], p[3])
    
    def p_states(self, p):
        '''
        states : state
                | states state
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]
    
    def p_state(self, p):
        '''
        state : STATE ID expressions
        '''
        p[0] = Node('state', p[2], *p[3]) # where p[3] is a list of expression AST Nodes.
        
    def p_expressions(self, p):
        '''
        expressions : expression
                    | expressions expression
        '''
        if len(p) == 2:
            p[0] = [p[1]] # where p[1] is an expression AST Node.
        else:
            p[0] = p[1] + [p[2]]
            
    def p_expression(self, p):
        '''
        expression : switch
                    | speak
                    | goto
                    | timeout
                    | default
                    | exit
        '''
        p[0] = p[1]
    
    def p_switch(self, p):
        '''
        switch : SWITCH cases
        '''
        p[0] = Node('switch', *p[2])
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
        '''
        p[0] = Node('case', p[2], *p[3])
        
    def p_speak(self, p):
        '''
        speak : SPEAK terms
        '''
        p[0] = Node('speak', p[2])
    
    def p_terms(self, p):
        '''
        terms : term
                | terms term
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]
    
    def p_term(self, p):
        '''
        term : STR
                | VAR
        '''
        if(p[1] == 'STR'):
            p[0] = Node('str', p[1])
        else:
            p[0] = Node('var', p[1])
    def p_goto(self, p):
        '''
        goto : GOTO ID
        '''
        p[0] = Node('goto', p[2])
        
    def p_timeout(self, p):
        '''
        timeout : TIMEOUT VAR expressions
        '''
        p[0] = Node('timeout', p[2], *p[3])
    
    def p_default(self, p):
        '''
        default : DEFAULT expressions
        '''
        p[0] = Node('default', *p[2])
        
    def p_exit(self, p):
        '''
        exit : EXIT
        '''
        p[0] = Node('exit')
        
    def p_error(self, p):
        print("Syntax error in input!")
        print(p)
        raise SyntaxError
    
    
    
if __name__ == '__main__':
    lexer = Lexer()
    parser = Parser(lexer)
    node = parser.parse('''
    script test
    variable
        x real $100
        y integer $100
        z text "hello"
    
    state start
        switch
            case "hello" speak "hello"
            case "bye" speak "bye"
            case "exit" exit
            default speak "default"
    state end
        timeout $10 goto start
    ''')
    node.print()
    