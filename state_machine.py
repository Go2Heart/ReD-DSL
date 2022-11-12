"""
    Using the Abstract Syntax Tree (AST) of the Python code, this module
    performs the following tasks:
        1. Extracts the states of DSL code and creates a state machine
        2. Extracts the transitions of DSL code and creates a transition
        3. Extracts the actions of DSL code and creates a action
"""
from parser import Parser, ASTNode
from lexer import Lexer

  
class CallBack(object):
    """
        CallBack class used to perform the actions of the DSL code
    """
    def __init__(self, callback, *args):
        self.callback = callback
        self.args = args
        #self.kwargs = kwargs
        self.type = ""
        if self.callback.__name__ == "_speak_action":
            self.type = "speak"
        elif self.callback.__name__ == "_goto_action":
            self.type = "goto"
        elif self.callback.__name__ == "_exit_action":
            self.type = "exit"
        else:
            raise Exception("Unknown action type")
        
    def __call__(self):
        return self.callback(*self.args)
        
    def __str__(self) -> str:
        return f"CallBack({self.callback}, {self.args})\n"
    
    def __repr__(self) -> str:
        #return f"CallBack({self.callback}, {self.args}, {self.kwargs})\n"
        return f"CallBack({self.callback.__name__}, {self.args})\n"
class StateMachine:
    """
        This class creates a state machine transition table
    """
    def __init__(self, AST : ASTNode, debug=False):
        self.AST = AST
        self.states_dict = dict()
        self.states_content = []
        self.initial_state = '<mono_begin>'
        self.debug = debug
        self.variables = dict()
        self.action_dict = dict()
        #self._extract_states()

    def __str__(self):
        return "States: " + str(self.states_dict) + "\nAction Table: " + str(self.action_dict) + "\nInitial State: " + str(self.initial_state) + "\nVariables: " + str(self.variables)
    
    def interpret(self):
        for declaration in self.AST.childs:
            if declaration.type == 'variables':
                for var in declaration.childs:
                    self._interpret_variable(var.type)
                #TODO add to variables databases
            elif declaration.type == 'states':
                for state in declaration.childs:
                    if self.debug:
                        print(state)
                    self.states_content.append(state) # Save the states content in the list
                    self.states_dict[state.type[1]] = {} # create a dictionary for the state
                if 'welcome' not in self.states_dict.keys():
                    raise Exception("No welcome state found. A welcome state is required.")
                self.states_dict[self.initial_state] = {} 
                self.action_dict[self.initial_state] = {} # create a action dictionary for the initial state
                self.action_dict[self.initial_state]['<on_enter>'] = [CallBack(self._goto_action, 'welcome')]
                if self.debug:
                    for state in self.states_content:
                        print(state.print())
                        
        for state in self.states_content: 
            self.action_dict[state.type[1]] = {} # keys should be user events
            self._interpret_state(state)
    
    
    def _interpret_variable(self, var):
        """
            @brief: interprets a variable declaration and adds it to the variables database
            @param: var is a quad of ('var', var_id, type, value)
            
        """
        if(self.debug):
            print(var)
        self.variables[var[1]] = [var[2], var[3]]
        
    def _interpret_state(self, state):
        """
            @brief: interprets a state declaration and adds it to the state machine
            @param:state is a duo of ('state', state_id) followed by a list of 
            clauses of {speak}, {switch}, {timeout}, {default}
        """
        state_name = state.type[1]
        for clause in state.childs:
            if clause.type == 'speak':
                speaks = clause.childs # only one child
                for speak in speaks:
                    try: 
                        self.action_dict[state_name]['<on_enter>'].append(CallBack(self._speak_action, speak))
                    except:
                        self.action_dict[state_name]['<on_enter>'] = [CallBack(self._speak_action, speak)]
                    
            elif clause.type == 'switch':
                terms = clause.childs # for all cases, the action can only speak, goto, exit
                for term in terms:
                    if term.type =='default' or term.type[0] == 'case':
                        case_condition = term.type[1] if term.type[0] == 'case' else '<default>'
                        case_actions = term.childs
                        self._extract_actions(state_name, case_condition, case_actions)
            elif clause.type[0] == 'timeout':
                timeout_condition = '<on_timeout>:' + clause.type[1]
                actions = clause.childs
                self._extract_actions(state_name, timeout_condition, actions)
                      
    def _speak_action(self, terms):
        """
            @brief: performs the speak action
            @param: term is a the child nodes of the speak clause
        """
        text = ""
        for term in terms.childs:
            if term.type[0] == 'id': # query the variables database
                text += str(self.variables[term.type[1]])
            elif term.type[0] == 'str':
                text += term.type[1]
            elif term.type[0] == 'var':
                text += str(term.type[1])
        #if self.debug:
        print(text)
        return text

    def _goto_action(self, new_state):
        """
            @brief: performs the goto action
            @param: new_state is the state to go to
        """
        print("Going to state: " + new_state)
        return new_state
    
    def _exit_action(self):
        """
            @brief: performs the exit action
        """
        print("Exiting")
        return 'exit'
    
    def _extract_actions(self, current_state, condition, actions):
        for action in actions:
            action_func = None
            if action.type == 'speak':
                action_func = CallBack(self._speak_action, action.childs[0])
                #self.action_dict[current_state][condition] = CallBack(self._speak_action, action.childs[0])
            elif action.type == 'exit':
                action_func = CallBack(self._exit_action)
                #self.action_dict[current_state][condition] = CallBack(self._exit_action)
            elif action.type[0] == 'goto':
                action_func = CallBack(self._goto_action, str(action.type[1]))
                #self.action_dict[current_state][condition] = CallBack(self._goto_action, action.type[1])
            else:
                raise Exception("Invalid action")
            if condition in self.action_dict[current_state].keys():
                self.action_dict[current_state][condition].append(action_func)
            else:
                self.action_dict[current_state][condition] = [action_func]
    
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
    #ASTNode.print()
    state_machine = StateMachine(ASTNode, debug=True)
    state_machine.interpret()
    print(state_machine)
    
    
    
    
    