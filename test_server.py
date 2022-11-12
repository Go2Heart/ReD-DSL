from parser import Parser, ASTNode
from lexer import Lexer
from state_machine import StateMachine, CallBack
from controller import Controller
"""
    @brief: this defines a least runable script to test the state machine
"""

if __name__ == "__main__":
    lexer = Lexer()
    parser = Parser(lexer, debug=False)
    with open("test.txt", "r") as f:
        script = f.read()
    controller = Controller(lexer, parser, script, debug=True)
    input_string = ""
    current_state = controller.state_machine.initial_state
    current_state = controller.accept_condition(current_state, "<on_enter>")
    while True:
        print ("Current state: ", current_state)
        input_string = input()
        current_state = controller.accept_condition(current_state, input_string)
        