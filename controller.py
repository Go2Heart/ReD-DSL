from parser import Parser, ASTNode
from lexer import Lexer
from state_machine import StateMachine, CallBack

class Controller:
    """
        @breif: Controller class for the State machine, acts as the interface between the state machine and the user
    """
    def __init__(self, lexer:Lexer, paser:Parser, script, debug=False):
        self._lexer = lexer
        self._parser = paser
        self.debug = debug
        self.state_machine = StateMachine(self._parser.parse(script), debug=False)
        self.state_machine.interpret()
        self.action_table = self.state_machine.action_dict
        
    def accept_condition(self, current_state:str, condition:str) -> str:
        """
            @brief: accepts a condition, peforms the required action and returns the next state
            @param: condition is the condition to check
            @return: the next state
        """
        # deal with the corresponding action of the condition and current_state
        next_state = current_state
        if condition not in self.action_table[current_state].keys():
            # perform the default action
            for action in self.action_table[current_state]["<default>"]:
                if action.type == "goto":
                    next_state = action()
                elif action.type == "speak":
                    action()
                elif action.type == "exit":
                    action()
        else:
            for action in self.action_table[current_state][condition]:
                if action.type == "goto":
                    next_state = action()
                elif action.type == "speak":
                    action()
                elif action.type == "exit":
                    action()
                
        if next_state != current_state:
            for action in self.action_table[next_state]["<on_enter>"]:
                if action.type == "goto":
                    next_state = action()
                elif action.type == "speak":
                    action()
                elif action.type == "exit":
                    action()
        return next_state
    
    
                    
        
        
        