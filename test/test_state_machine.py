import os
import unittest
from server.interpreter import StateMachine
from server.yacc import Parser
from server.lexer import Lexer

class TestStateMachine(unittest.TestCase):
    def setUp(self):
        self.lexer = Lexer()
        self.parser = Parser(self.lexer)

    def test_interpreter(self):
        with open(os.path.join(os.path.dirname(__file__), "script/interpreter_test/result1.txt"), "r") as f:
            result = f.read().strip()
        with open(os.path.join(os.path.dirname(__file__), "script/interpreter_test/test1.txt"), "r") as f:
            script = f.read()
        state_machine = StateMachine(self.parser.parse(script), "./interpreter_test1.db")
        state_machine.interpret()
        action_table = state_machine.action_dict
        self.assertEqual(repr(action_table), result)
        del state_machine, action_table
        
        with open(os.path.join(os.path.dirname(__file__), "script/interpreter_test/result2.txt"), "r") as f:
            result = f.read().strip()
        with open(os.path.join(os.path.dirname(__file__), "script/interpreter_test/test2.txt"), "r") as f:
            script = f.read()
        state_machine = StateMachine(self.parser.parse(script), "./interpreter_test2.db")
        state_machine.interpret()
        action_table = state_machine.action_dict
        self.assertEqual(repr(action_table), result)
        
        
        
        
        
        
if __name__ == "__main__":
    unittest.main()
        