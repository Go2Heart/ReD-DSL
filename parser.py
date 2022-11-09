from ply.yacc import yacc
from lexer import Lexer


class Node:
    """
        Abstract syntax tree node
    """
    def __init__(self, type, *child):
        self.type = type
        self.childs = list(child)
    
    def __str__(self) -> str:
        return self.type
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
    def __init__(self, lexer:Lexer, debug=False): #TODO add config
        self._lexer = lexer
        self.tokens = lexer.tokens
        self._yacc = yacc(module=self, debug=True)
        self.debug = debug
    
    def parse(self, script):
        """
            parse a script
            @param script: the script to parse
        """
        return self._yacc.parse(script, self._lexer.getLexer())
    
    start = 'script'
    def p_script(self, p):
        '''
        script : SCRIPT ID variables NEWLINE states
        '''
        p[0] = Node(('script', p[2]), p[3], p[4+1])
    
    
    
    def p_variables(self, p):
        '''
        variables : NEWLINE VARIABLE vars END
        '''
        p[0] = Node(('variables'), *p[3])
        if(self.debug):
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
        var : NEWLINE ID REAL VAR
                | NEWLINE ID INTEGER VAR
                | NEWLINE ID TEXT STR
        '''
        p[0] = Node('var', p[1+1], p[2+1], p[3+1])
    
    def p_states(self, p):
        '''
        states : state
                | states state
        '''
        if len(p) == 2:
            #p[0] = [p[1]]
            p[0] = Node('states', p[1])
        else:
            #p[0] = p[1] + [p[2]]
            p[0] = Node('states', *p[1].child, p[2])
    
    def p_state(self, p):
        '''
        state : NEWLINE STATE ID expressions END
        '''
        p[0] = Node(('state', p[2+1]), *p[3+1]) # where p[3] is a list of expression AST Nodes.
        
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
        expression : NEWLINE switch
                    | NEWLINE speak
                    | NEWLINE goto
                    | NEWLINE timeout
                    | NEWLINE exit
        '''
        p[0] = p[2]
    
    def p_switch(self, p):
        '''
        switch : SWITCH cases NEWLINE default
        '''
        p[0] = Node('switch', *p[2], p[4])
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
        case : NEWLINE CASE STR expressions 
        '''
        p[0] = Node('case', p[2+1], *p[3+1])
        
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
    parser = Parser(lexer, debug=True)
    with open('test.txt') as f:
        script = f.read()
        
    node = parser.parse(script)
    node.print()
    