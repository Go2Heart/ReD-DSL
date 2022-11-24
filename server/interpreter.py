""" Consists of the UserVariableSet class and CallBack class and StateMachine class 

StateMachine class:

StateMachine Using the Abstract Syntax Tree (AST) of the Python code, this module performs the following tasks:
    1. Extracts the states of DSL code and creates a state machine
    2. Extracts the transitions of DSL code and creates a transition
    3. Extracts the actions of DSL code and creates a action
    
Typical usage example:

state_machine = StateMachine(AST)
state_machine.interpret()
state_machine.build_database("./database.db")

CallBack class:

CallBack class is used to create a callback function for the actions of DSL code.

Typical usage example:

action = CallBack("print", "Hello World")
action()

UserVariableSet class:

UserVariableSet class is used to store the user variables.

Typical usage example:

user_variable_set = UserVariableSet()
setattr(user_variable_set, "username", "Guest")
    
"""
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pickle
from server.yacc import  ASTNode
from storm.locals import create_database, Store
from storm.properties import Unicode, Int, Float
from threading import Lock

class UserVariableSet(object):
    """creates a new user variable set
    
    Attributes:
        username (str): the username of the user
        passwd (str): the password of the user
    """
    __storm_table__ = 'user_variable'
    column_type = {"username": "Text", "passwd": "Text"}
    username = Unicode(primary=True)
    passwd = Unicode()

    def __init__(self, username: str, passwd: str):
        """Inits UserVariableSet with username and passwd
        
        Note that other attributes can be added dynamically
        
        Args:
            username: the username of the user
            passwd: the password of the user
        """
        self.username = username
        self.passwd = passwd



class CallBack(object):
    """CallBack class used to perform the actions of the DSL code
    
    Attributes:
        callback (function): the callback function
        args (tuple): the arguments of the callback function
        type (str): the type of the callback function
    """
    def __init__(self, callback, *args):
        """Inits CallBack with callback and args"""
        self.callback = callback
        self.args = args
        self.type = ""
        if self.callback.__name__ == "_speak_action":
            self.type = "speak"
        elif self.callback.__name__ == "_goto_action":
            self.type = "goto"
        elif self.callback.__name__ == "_exit_action":
            self.type = "exit"
        elif self.callback.__name__ == "_update_action":
            self.type = "update"
        else:
            raise Exception("Unknown action type")
        
    def __call__(self, *args): 
        """calls the callback function"""
        return self.callback(*self.args,*args)
    
    def __str__(self) -> str:
        """returns the string representation of the CallBack object"""
        return f"CallBack({self.callback}, {self.args})\n"
    
    def __repr__(self) -> str:
        """returns the string representation of the CallBack object"""
        return f"CallBack({self.callback.__name__}, {self.args})"
class StateMachine:
    """This class creates a state machine transition table
    
    StateMachine will not create one instance for each state, but provides a dictionary of states transition table.
    Thus, the memory usage is reduced. And for all users, only one instance of StateMachine is created. They share the same state machine.
    Only the user variables are different. They are stored in the database. Users can only read and write their own variables. 
    Users will query the transition table of the state machine to get the next state and the actions of the next state.
    
    Attributes:
        AST (ASTNode): the abstract syntax tree of the DSL code
        states_dict (dict): the states of the state machine
        states_content (list): the content of the states
        initial_state (str): the initial state of the state machine
        debug (bool): the debug mode
        variable_dict (dict): the variables of the state machine
        action_dict (dict): the actions of the state machine
        compare_list (list): the list of the comparison operators
        db_path (str): the path of the database
    """
    def __init__(self, AST : ASTNode, db_path="./database.db",debug=False):
        """Inits StateMachine with AST and debug
        
        Args:
            AST (ASTNode): the abstract syntax tree of the DSL code
            db_path (str): the path of the database
            debug (bool): the debug mode
        """
        self.AST = AST
        self.states_dict = dict()
        self.states_content = []
        self.initial_state = '<mono_begin>'
        self.debug = debug
        self.variable_dict = dict()
        self.action_dict = dict()
        self.compare_list = []
        self.db_path = db_path

    def __str__(self):
        """returns the string representation of the StateMachine object"""
        return "States: " + str(self.states_dict) + "\nAction Table: " + str(self.action_dict) + "\nInitial State: " + str(self.initial_state) + "\nVariables: " + str(self.variable_dict)
    
    def interpret(self):
        """interprets the DSL code and builds the state machine transition table
        
        Raises:
            Exception: if the DSL code is invalid
        """
        for declaration in self.AST.childs:
            if declaration.type == 'variables':
                for var in declaration.childs:
                    self._interpret_variable(var.type)
            elif declaration.type == 'states':
                for state in declaration.childs:
                    if self.debug:
                        print(state)
                    self.states_content.append(state)   # Save the states content in the list
                    self.states_dict[state.type[1]] = {}    # create a dictionary for the state
                if 'welcome' not in self.states_dict.keys():
                    raise Exception("No welcome state found. A welcome state is required.")
                self.states_dict[self.initial_state] = {} 
                self.action_dict[self.initial_state] = {}   # create a action dictionary for the initial state
                self.action_dict[self.initial_state]['<on_enter>'] = [CallBack(self._goto_action, 'welcome')]
                if self.debug:
                    for state in self.states_content:
                        print(state.print())
                        
        for state in self.states_content: 
            self.action_dict[state.type[1]] = {} # keys should be user events
            self._interpret_state(state)
        
        self._build_database(self.db_path)
        
    def test(self, condition, num, username="Guest"):
        """tests the condition
        
        Args:
            condition: the condition to test
            num: the entry to compare list
            
        Returns:
            True if the condition is true, False otherwise
            
        Raises:
            Exception: if the condition type is unknown
        """
        compare = self.compare_list[num]
        compare_source = float(condition) if compare[1] == '_return' else float(self._get_value(ASTNode(('id', compare[1])), username))
        compare_op = compare[2]
        compare_target = float(self._get_value(ASTNode(compare[3]), username))
        if compare_op == '<':
            return compare_source < compare_target
        elif compare_op == '>':
            return compare_source > compare_target
        elif compare_op == '<=':
            return compare_source <= compare_target
        elif compare_op == '>=':
            return compare_source >= compare_target
        else:
            raise Exception("Unknown comparison operator")
        
    def update_return_value(self, value, username="Guest"):
        """updates the return value
            
        Args:
            value: value is the value to return
            username: the username of the user
        """
        global db_lock, database
        with db_lock:
            store = Store(database)
            user = store.find(UserVariableSet, UserVariableSet.username == username)
            user.set(_return=value)
            store.commit()
            store.close()
            
    def register(self, username, passwd):
        """registers a new user
        
        Args:
            username: the username of the new user
            passwd: the password of the new user
            
        Returns:
            "Registered" if the user was registered successfully
            
        Raises:
            Exception: if the user already exists
        """
        global database, db_lock
        with db_lock:
            store = Store(database)
            if store.get(UserVariableSet, username) is not None:
                store.close()
                raise Exception("User already exists")
            store.add(UserVariableSet(username, passwd))
            store.commit()
            store.close()
        return True
    
    def login(self, username, passwd):
        """logs in a user
        
        Args:
            username: the username of the user
            passwd: the password of the user
            
        Returns:
            True if the user is logged in, Exception otherwise
            
        Exceptions:
            Exception: if the user does not exist
            Exception: if the password is incorrect
        """
        global database, db_lock
        with db_lock:
            store = Store(database)
            user = store.get(UserVariableSet, username)
            if user is None:
                store.close()
                raise Exception("User does not exist")
            if user.passwd != passwd:
                store.close()
                raise Exception("Incorrect password")
            store.close()
        return True
        
    def _build_database(self, path):
        """builds the database of the state machine
        
        Args:
            path (str): the path of the database
        """
        global database, db_lock
        dir, file_name = os.path.split(path)
        if file_name in os.listdir(dir):
            os.remove(path)
        database = create_database("sqlite:" + path)
        db_lock = Lock()
        create_table_statement = ["CREATE TABLE user_variable (username TEXT PRIMARY KEY, passwd TEXT"]
        for k,v  in self.variable_dict.items():
            if v[0] == 'integer':
                setattr(UserVariableSet, k, Int(default=int(v[1])))
            elif v[0] == 'real':
                setattr(UserVariableSet, k, Float(default=float(v[1])))
            elif v[0] == 'text':
                setattr(UserVariableSet, k, Unicode(default=v[1]))
            UserVariableSet.column_type[k] = v[0]
            create_table_statement.append(k + " " + v[0])
        setattr(UserVariableSet, "_return", Unicode(default=""))
        create_table_statement.append("_return TEXT")
        with db_lock:
            store = Store(database)
            store.execute(','.join(create_table_statement) + ')')
            store.add(UserVariableSet("Guest", ''))  # add a guest user
            store.commit()
            store.close()
    
    def get_database(self):
        """gets the database
        
        Returns:
            the database
        """
        return database

    def _interpret_variable(self, var):
        """interprets a variable declaration and adds it to the variables dictionary
            
        Args:
            var: var is a quad of ('var', var_id, type, value)
            
        """
        if(self.debug):
            print(var)
        self.variable_dict[var[1]] = [var[2], var[3]]
        
    def _interpret_state(self, state):
        """interprets a state declaration and adds it to the state machine
        
        Args:
            state:state is a duo of ('state', state_id) followed by a list of clauses of {speak}, {switch}, {timeout}, {default}
            
        """
        state_name = state.type[1]
        for clause in state.childs:
            if clause.type == 'speak':
                speaks = clause.childs   # only one child
                for speak in speaks:
                    try: 
                        self.action_dict[state_name]['<on_enter>'].append(CallBack(self._speak_action, speak))
                    except:
                        self.action_dict[state_name]['<on_enter>'] = [CallBack(self._speak_action, speak)]
                    
            elif clause.type == 'switch':
                terms = clause.childs   # for all cases, the action can only speak, goto, exit or update
                for term in terms:
                    if term.type =='default' or term.type[0] == 'case':
                        case_condition = term.type[1] if term.type[0] == 'case' else '<default>'
                        if isinstance(case_condition, tuple):
                            case_condition = ('<compare>' , len(self.compare_list))
                            self.compare_list.append(term.type[1])
                        case_actions = term.childs
                        self._extract_actions(state_name, case_condition, case_actions)
            elif clause.type[0] == 'timeout':
                timeout_condition = '<on_timeout>'
                self.action_dict[state_name]["<timeout_value>"] = clause.type[1]
                actions = clause.childs
                self._extract_actions(state_name, timeout_condition, actions)
            else:
                raise Exception("Unknown clause type", clause)
                      
    def _speak_action(self, terms, username="Guest"):
        """performs the speak action
        Args: 
            term: term is a the child nodes of the speak clause
            username: the username of the user
        """
        text = ""
        for term in terms.childs:
            text += str(self._get_value(term, username))
        print(text)
        return text + '\n'

    def _goto_action(self, new_state):
        """performs the goto action
        
        Args:
            new_state: new_state is the state to go to
        """
        if(self.debug): 
            print("Going to state", new_state)
        return new_state
    
    def _exit_action(self):
        """performs the exit action"""
        if(self.debug): 
            print("Exiting...")
        return 'Exiting...\n'
    
    def _update_action(self, id, calculation, username="Guest"):
        """performs the update action
        
        Args:
            id: id is the id of the variable to update
            calculation: calculation is the calculation to perform
            username: the username of the user
            
        Raises:
            Exception: if the variable is not found
            Exception: if the calculation is invalid
            Exception: if the variable is not a number
        """
        if calculation.type[0] == 'calc':
            if calculation.type[1] == 'PLUS':
                #self.variables[id][1] 
                result = float(self._get_value(calculation.childs[0], username)) + float(self._get_value(calculation.childs[1], username))
                
            elif calculation.type[1] == 'MINUS':
                #self.variables[id][1]
                result = float(self._get_value(calculation.childs[0], username)) - float(self._get_value(calculation.childs[1], username))
            else:
                raise Exception("Unknown calculation type")
            with db_lock:
                store = Store(database)
                store.find(UserVariableSet, UserVariableSet.username == username).set(**{id:result})
                store.commit()
                store.close()
        elif calculation.type == 'terms':
                result = float(self._get_value(calculation.childs[0], username))
                with db_lock:
                    store = Store(database)
                    store.find(UserVariableSet, UserVariableSet.username == username).set(**{id:result})
                    store.commit()
                    store.close()
        else:   
            raise Exception("Unknown manipulation type")
    
    def _get_value(self, term, username):
        """gets the value of the term of the user
        
        Args:
            term: term is the term to get the value from
            username: the username of the user
            
        Returns:
            the value of the term
            
        Raises: 
            Exception: if the variable is not found
            Exception: if the variable type is unknown
        """
        global database, db_lock
        with db_lock:
            store = Store(database)
            valueset = store.find(UserVariableSet, UserVariableSet.username == username).one()
            store.close()
            if term.type[0] == 'id':
                value = getattr(valueset, term.type[1])
                return value #self.variables[term.type[1]][1] 
            elif term.type[0] == 'str':
                return term.type[1]
            elif term.type[0] == 'var':
                return term.type[1]
            elif term.type[0] == '<return>':
                value = getattr(valueset, '_return')
                return value #self.variables['_return'][1]
            else:
                raise Exception("Unknown term type", term)
            
        
    def _extract_actions(self, current_state, condition, actions):
        """extracts the actions from the actions clause and adds them to the state machine transition table
        
        Args:
            current_state: current_state is the current state
            condition: condition is the condition to perform the actions
            actions: actions is the list of actions to perform
            
        Raises:
            Exception: if the action type is unknown
        """
        for action in actions:
            action_func = None
            if action.type == 'speak':
                action_func = CallBack(self._speak_action, action.childs[0])
            elif action.type == 'exit':
                action_func = CallBack(self._exit_action)
            elif action.type[0] == 'goto':
                action_func = CallBack(self._goto_action, str(action.type[1]))
            elif action.type[0] == 'update':
                action_func = CallBack(self._update_action, action.type[1], action.childs[0])
            else:
                raise Exception("Invalid action")
            if condition in self.action_dict[current_state].keys():
                self.action_dict[current_state][condition].append(action_func)
            else:
                self.action_dict[current_state][condition] = [action_func]
                

    
    
        
        

                    
if __name__ == "__main__":
    with open("test/stub/ast.stub", "rb") as f:
        ast = pickle.load(f)
    state_machine = StateMachine(ast,db_path="server/database.db", debug=True)
    state_machine.interpret()
    print(state_machine)

    
    
    
    
    