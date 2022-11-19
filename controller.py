from parser import Parser, ASTNode
from lexer import Lexer
from interpreter import StateMachine, CallBack

class Controller:
    """
        @breif: Controller class for the State machine, acts as the interface between the state machine and the user
    """
    def __init__(self, lexer:Lexer, paser:Parser, script, debug=False):
        self._lexer = lexer
        self._parser = paser
        self.debug = debug
        self.state_machine = StateMachine(self._parser.parse(script), debug=debug)
        self.state_machine.interpret()
        self.state_machine.build_database("./database.db")
        self.action_table = self.state_machine.action_dict
        self._return = ""
        
    def register(self, username:str, password:str):
        """
            @brief: register a new user
            @param: username is the username of the user
            @param: password is the password of the user
        """
        try : 
            self.state_machine._register(username, password)
        except Exception as e:
            raise e
        return True
    
    def login(self, username:str, password:str):
        """
            @brief: login a user
            @param: username is the username of the user
            @param: password is the password of the user
        """
        try:
            self.state_machine._login(username, password)
        except Exception as e:
            raise e
        return True
    
    def accept_condition(self, current_state:str, condition:str, username="Guest"):
        """
            @brief: accepts a condition, peforms the required action and returns the next state
            @param: condition is the condition to check
            @return: the next state
        """
        # deal with the corresponding action of the condition and current_state
        next_state = current_state
        output = ""
        is_transferred = False
        self._return = condition
        self.state_machine.update_return_value(condition, username)
        if condition not in self.action_table[current_state].keys():
            if '_return' in self.action_table[current_state].keys(): # if there is a return condition
                for action in self.action_table[current_state]['_return']:
                    if action.type == "goto":
                        next_state = action()
                        is_transferred = True
                        break
                    elif action.type == "speak":
                        output += action(username)
                        output += "\n"
                    elif action.type == "exit":
                        action()
                    elif action.type == "update":
                        action(username) ## TODO add user info BREAKPOINT
                    else:
                        raise Exception("Invalid action")
            elif '<default>' in self.action_table[current_state].keys(): # if there is a default condition
                # perform the default action
                for action in self.action_table[current_state]["<default>"]:
                    if action.type == "goto":
                        next_state = action()
                        is_transferred = True
                        break
                    elif action.type == "speak":
                        output += action(username)
                        output += "\n"
                    elif action.type == "exit":
                        action()
                    elif action.type == "update":
                        action(username)
                    else:
                        raise Exception("Invalid action")
            else:
                for key in self.action_table[current_state].keys():
                    if isinstance(key, tuple) and self.state_machine.test(condition, key[1], username): # it's a compare condition and it's true
                        for action in self.action_table[current_state][key]:
                            if action.type == "goto":
                                next_state = action()
                                is_transferred = True
                                break
                            elif action.type == "speak":
                                output += action(username)
                                output += "\n"
                            elif action.type == "exit":
                                action()
                            elif action.type == "update":
                                action(username)
                            else:
                                raise Exception("Invalid action")   
                        break
        else:
            for action in self.action_table[current_state][condition]:
                if action.type == "goto":
                    next_state = action()
                    is_transferred = True
                    break
                elif action.type == "speak":
                    output += action(username)
                    output += "\n"
                elif action.type == "exit":
                    action()
                elif action.type == "update":
                    action(username)
                else:
                    raise Exception("Invalid action")
                
        if is_transferred:
            for action in self.action_table[next_state]["<on_enter>"]:
                if action.type == "goto":
                    next_state = action()
                elif action.type == "speak":
                    output += action(username)
                    output += "\n"
                elif action.type == "exit":
                    action()
                elif action.type == "update":
                    action(username)
                else:
                    raise Exception("Invalid action")
        timeout = self.state_machine.action_dict[next_state].get("<timeout_value>", 999)
        return next_state, output, int(timeout)
    
    
                    
        
        
        