"""
    Using the Abstract Syntax Tree (AST) of the Python code, this module
    performs the following tasks:
        1. Extracts the states of DSL code and creates a state machine
        2. Extracts the transitions of DSL code and creates a transition
        3. Extracts the actions of DSL code and creates a action
"""
from parser import Parser, ASTNode
from lexer import Lexer

class Action(object):
    """
        Action class used to perform the actions of the DSL code
    """
    def speak(self, event):
        text = event.kwargs.get('text', 'In Silent Mode')
        print(text)
        
class StateMachine:
    """
        This class creates a state machine transition table
    """
    def __init__(self, AST : ASTNode, debug=False):
        self.AST = AST
        self.states = [] #TODO to be removed
        self.states_dict = {}
        self.states_content = []
        self.transitions = []
        self.initial_state = None
        self.debug = debug
        self.variables = {}
        
        #self._extract_states()
        #self.machine = Machine(model=self, states=self.states, transitions=self.transitions, initial=self.initial_state, send_event=True) TODO 

    def __str__(self):
        return "States: " + str(self.states) + "Transitions: " + str(self.transitions) + "Initial State: " + str(self.initial_state)
    
    def _interpret_variable(self, var):
        """
            @brief: interprets a variable declaration and adds it to the variables database
            @param: var is a quad of ('var', var_id, type, value)
            
        """
        self.variables[var[1]] = [var[2], var[3]]
        
    def _interpret_state(self, state):
        """
            @brief: interprets a state declaration and adds it to the state machine
            @param:state is a duo of ('state', state_id) followed by a list of 
            clauses of {speak}, {switch}, {timeout}, {default}
        """
        state_name = state.type[1]
        for clause in state.childs:
            if clause.type[0] == 'speak':
                terms = clause.childs
                text = ""
                for term in terms:
                    if term.type[0] == 'var': # query the variables database
                        text += str(self.variables[term.type[1]])
                    elif term.type[0] == 'str':
                        text += term.type[1]
                self.states_dict[state_name].append({'on_enter': text})
            elif clause.type[0] == 'switch':
                terms = clause.childs # for all cases, the action can only speak, goto, exit
                for term in terms:
                    if term.type[0] == 'case':
                        case_condition = term.type[1]
                        case_action = term.childs
                        for action in case_action:
                            if 
                        
                        
        

    
    def interpret(self):
        for declaration in self.AST.childs:
            if declaration.type[0] == 'variables':
                for var in declaration.childs:
                    self._interpret_variable(var)
                #TODO add to variables databases
            elif declaration.type[0] == 'states':
                for state in declaration.childs:
                    if self.debug:
                        print(state)
                    self.states.append({'name' : state.type[1]}) # Save the states in the list TODO to be removed
                    self.states_content.append(state) # Save the states content in the list
                    self.states_dict[state.type[1]] = {} # create a dictionary for the state
                if {'name' : 'welcome'} not in self.states:
                    raise Exception("No welcome state found. A welcome state is required.")
                self.initial_state = 'welcome'
                if self.debug:
                    print("States: ", self.states)
                    for state in self.states_content:
                        print(state.print())
                        
        for state in self.states_content: #TODO add a dummy state to enter welcome state
            self._interpret_state(state)
    #def _extract_states(self):
    #    """
    #        Extracts the states from the AST
    #    """
    #    for child in self.AST.childs:
    #        if child.type == 'states':
    #            for state in child.childs:
    #                if self.debug:
    #                    print(state)
    #                self.states.append({'name' : state.type[1]}) # Save the states in the list
    #                self.states_content.append(state) # Save the states content in the list
    #    if {'name' : 'welcome'} not in self.states:
    #        raise Exception("No welcome state found. A welcome state is required.")
    #    self.initial_state = 'welcome'
    #    if self.debug:
    #        print("States: ", self.states)
    #        for state in self.states_content:
    #            print(state.print())
    #def _extract_transitions(self):
    #    """
    #        Extracts the transitions from the AST
    #    """
        
                    
if __name__ == "__main__":
    lexer = Lexer()
    parser = Parser(lexer, debug=False)
    with open("test.txt", "r") as f:
        script = f.read()
    ASTNode = parser.parse(script)
    ASTNode.print()
    state_machine = StateMachine(ASTNode, debug=True)
    
    
    
    
    
    