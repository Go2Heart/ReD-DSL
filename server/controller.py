""" Controller class is a hanlde to operate the state machine for the user 

Controller has the methods to register a user, accept a condition, and get the current state of the user.
And for every return value from the user, it will record it in the database.
It is a wrapper of the state machine, being used to handle the user's input and output.

Typical usage example:

controller = Controller(lexer, parser, script, debug=True)
controller.register("test", "test")
"""

from server.yacc import Parser
from server.lexer import Lexer
from server.interpreter import StateMachine


class Controller:
    """Controller class for the State machine, acts as the interface between the state machine and the user
    
    Controller has the methods to register a user, log in a user, accept a condition of the user.
    For every return value from the user, it will record it in the database.
    User query with the current state of the user to get the next state and the output as well as the timeout value.
    
    Attributes:
        _lexer: the lexer used to parse the script
        _parser: the parser used to parse the script
        debug: the debug mode
        state_machine: the state machine
        action_table: the action table of the state machine
        _return: the return value of the user
    """

    def __init__(self, lexer: Lexer, paser: Parser, script, db_path="./database.db", debug=False):
        """init the controller with the script"""
        self._lexer = lexer
        self._parser = paser
        self.debug = debug
        self.state_machine = StateMachine(self._parser.parse(script), debug=debug)
        self.state_machine.interpret()
        self.action_table = self.state_machine.action_dict
        self._return = ""

    def register(self, username: str, password: str):
        """register a new user
        
        Args:
            username: the username of the user
            password: the password of the user
            
        Returns:
            True if the user is registered successfully
        
        Raises:
            Exception: if the user is already registered
        """
        try:
            self.state_machine.register(username, password)
        except Exception as e:
            raise e
        return True

    def login(self, username: str, password: str):
        """login a user
        
        Args:
            username: the username of the user
            password: the password of the user
            
        Returns:
            True if the user is logged in successfully
            
        Raises:
            Exception: if the user is not registered or the password is wrong
        """
        try:
            self.state_machine.login(username, password)
        except Exception as e:
            raise e
        return True

    def accept_condition(self, current_state: str, condition: str, username="Guest"):
        """accepts a condition, peforms the required action and returns the next state, output and timeout
        
        The controller will check the database of the state machine to perform the required action if there is any.
        Or it will check the action table to perform the required action if there is any.
        
        Args:
            current_state: the current state of the user
            condition: the condition to check
            username: the username of the user
            
        
        Return: 
            next_state: the next state of the user
            output: the output of the state machine
            timeout: the timeout of the state machine
            
        Raises:
            Exception: if the current state is not in the state machine
            Exception: if the condition is not in the state machine
        """
        next_state = current_state
        output = ""
        is_transferred = False
        is_exit = False
        self._return = condition
        self.state_machine.update_return_value(condition, username)
        if condition not in self.action_table[
            current_state].keys():  # deal with the corresponding action of the condition and current_state
            if '_return' in self.action_table[current_state].keys():  # if there is a return condition
                for action in self.action_table[current_state]['_return']:
                    if action.type == "goto":
                        next_state = action()
                        is_transferred = True
                        break
                    elif action.type == "speak":
                        output += action(username)
                    elif action.type == "exit":
                        output += action()
                        is_exit = True
                    elif action.type == "update":
                        action(username)
                    else:
                        raise Exception("Invalid action")
            elif '<default>' in self.action_table[current_state].keys():  # if there is a default condition
                # perform the default action
                for action in self.action_table[current_state]["<default>"]:
                    if action.type == "goto":
                        next_state = action()
                        is_transferred = True
                        break
                    elif action.type == "speak":
                        output += action(username)
                    elif action.type == "exit":
                        output += action()
                        is_exit = True
                    elif action.type == "update":
                        action(username)
                    else:
                        raise Exception("Invalid action")
            else:
                for key in self.action_table[current_state].keys():
                    if isinstance(key, tuple) and self.state_machine.test(condition, key[1],
                                                                          username):  # it's a compare condition and it's true
                        for action in self.action_table[current_state][key]:
                            if action.type == "goto":
                                next_state = action()
                                is_transferred = True
                                break
                            elif action.type == "speak":
                                output += action(username)
                            elif action.type == "exit":
                                output += action()
                                is_exit = True
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
                elif action.type == "exit":
                    output += action()
                    is_exit = True
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
                elif action.type == "exit":
                    action()
                    is_exit = True
                elif action.type == "update":
                    action(username)
                else:
                    raise Exception("Invalid action")
        timeout = self.state_machine.action_dict[next_state].get("<timeout_value>", 999)
        return next_state, output, int(timeout), is_exit
