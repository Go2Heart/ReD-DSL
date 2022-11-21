import os
import unittest
from server.yacc import Parser
from server.lexer import Lexer


class TestParser(unittest.TestCase):
    def setUp(self):
        self.lexer = Lexer()
        self.parser = Parser(self.lexer)

    def test_parse(self):
        with open(os.path.join(os.path.dirname(__file__), "script/parser_test/result1.txt"), "r") as f:
            result = f.read().strip()
        with open(os.path.join(os.path.dirname(__file__), "script/parser_test/test1.txt"), "r") as f:
            script = f.read()
            self.assertEqual(repr(self.parser.parse(script)), result)
            
        with open(os.path.join(os.path.dirname(__file__), "script/parser_test/result2.txt"), "r") as f:
            result = f.read().strip()
        with open(os.path.join(os.path.dirname(__file__), "script/parser_test/test2.txt"), "r") as f:
            script = f.read()
            self.assertEqual(repr(self.parser.parse(script)), result)
            
        with self.assertRaises(SyntaxError):
            with open(os.path.join(os.path.dirname(__file__), "script/parser_test/test3.txt"), "r") as f:
                script = f.read()
                self.parser.parse(script)
                
        with self.assertRaises(SyntaxError):
            with open(os.path.join(os.path.dirname(__file__), "script/parser_test/test4.txt"), "r") as f:
                script = f.read()
                self.parser.parse(script)
if __name__ == "__main__":
    unittest.main()
