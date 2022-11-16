"""
    @brief: this defines a least runable script to test the state machine
"""

from parser import Parser, ASTNode
from lexer import Lexer
from state_machine import StateMachine, CallBack
from controller import Controller
import select
import sys


def input_with_timeout(prompt, timeout):
    if prompt is not None:
        sys.stdout.write(prompt)
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.readline().rstrip('\n')  # expect stdin to be line-buffered
    raise TimeoutError


def test_input(current_state):
    """
        @brief: test input function using threading
    """
    input_string = input()
    current_state = controller.accept_condition(current_state, input_string, "test")


if __name__ == "__main__":
    lexer = Lexer()
    parser = Parser(lexer, debug=False)
    with open("test.txt", "r") as f:
        script = f.read()
    controller = Controller(lexer, parser, script, debug=True)
    controller.register("test", "test")
    input_string = ""
    current_state = controller.state_machine.initial_state
    current_state,output = controller.accept_condition(current_state, "<on_enter>", "test")
    while True:
        #print("Current state: ", current_state)
        try:
            condition = input_with_timeout(None, 10)
            current_state,output = controller.accept_condition(
                current_state, condition, "test")
        except TimeoutError:
            current_state,output = controller.accept_condition(
                current_state, "<on_timeout>:10", "test")
