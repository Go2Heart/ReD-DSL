import os
import unittest
from server.yacc import Parser
from server.lexer import Lexer
from server.controller import Controller
from server.interpreter import *

class TestController(unittest.TestCase):
    """Test the controller with a more complex script
    
    Use the script in script/controller_test/test1.txt, which a copy of bank service script.
    Test the controller login, register, accept_condition, and compare function.
    
    Arttibutes:
        lexer (Lexer): Lexer object
        parser (Parser): Parser object
        controller (Controller): Controller object
    """
    def setUp(self):
        self.lexer = Lexer()
        self.parser = Parser(self.lexer)
        with open(os.path.join(os.path.dirname(__file__), "script/controller_test/test1.txt"), "r") as f:
            script = f.read()
        self.controller = Controller(self.lexer, self.parser, script, "./test1.db")
        
    def test_controller(self):
        # test action table and condition accept
        with open(os.path.join(os.path.dirname(__file__), "script/controller_test/result1.txt"), "r") as f:
            action_table_result = f.read().strip()
        self.assertEqual(repr(self.controller.action_table), action_table_result)
        self.controller.register("test_controller", "test_password")
        current_state = self.controller.state_machine.initial_state
        current_state, output, timeout, exit = self.controller.accept_condition(current_state, "<on_enter>", "test_controller")
        self.assertEqual(current_state, "welcome")
        with open(os.path.join(os.path.dirname(__file__), "script/controller_test/output1.txt"), "r") as f:
            output_result = f.read()
        self.assertEqual(output, output_result)
        self.assertEqual(timeout, 30)
        self.assertEqual(exit, False)
        
        # test User Variable Set is being set correctly and compare function is working
        current_state, output, timeout, exit = self.controller.accept_condition(current_state, "topup", "test_controller")
        current_state, output, timeout, exit = self.controller.accept_condition(current_state, "-50", "test_controller")    # calling comparing function
        current_state, output, timeout, exit = self.controller.accept_condition(current_state, "topup", "test_controller")
        current_state, output, timeout, exit = self.controller.accept_condition(current_state, "50", "test_controller")     # calling comparing function
        store = Store(self.controller.state_machine.get_database())
        self.assertEqual(store.get(UserVariableSet, "test_controller").x, 150)
        self.assertEqual(store.get(UserVariableSet, "test_controller")._return, "50")
        self.assertEqual(current_state, "welcome")
        self.assertEqual(output, "You have topped up 50 dollars\n"+output_result)
        self.assertEqual(timeout, 30)
        self.assertEqual(exit, False)
        store.close()
        
        # test login with wrong password
        with self.assertRaises(Exception):
            self.controller.login("test_controller", "wrong_password")
        
        # test login with non-existent username
        with self.assertRaises(Exception):
            self.controller.login("wrong_user", "test_password")
        
        # test register with existing username
        with self.assertRaises(Exception):
            self.controller.register("test_controller", "test_password")
        
        
if __name__ == "__main__":
    unittest.main()