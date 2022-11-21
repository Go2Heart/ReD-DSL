"""brief: this defines a least runable script to test the state machine

Copyright (c) 2022 Yibin Yan
"""
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from server.yacc import Parser
from server.lexer import Lexer
from server.controller import Controller
import select


def input_with_timeout(prompt, timeout):
    """Input with timeout
    
    Args:
        prompt: the prompt message
        timeout: the timeout value
    
    Returns:
        the input string
    
    Raises:
        TimeoutError: if the timeout is reached
    """
    if prompt is not None:
        sys.stdout.write(prompt)
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.readline().rstrip('\n')  # expect stdin to be line-buffered
    raise TimeoutError


if __name__ == "__main__":
    lexer = Lexer()
    parser = Parser(lexer, debug=False)
    with open("./test/script/test1.txt", "r") as f:
        script = f.read()
    controller = Controller(lexer, parser, script, debug=True)
    controller.register("test", "test")
    input_string = ""
    current_state = controller.state_machine.initial_state
    current_state, output, timeout, exit = controller.accept_condition(current_state, "<on_enter>", "test")
    while exit == False:
        try:
            condition = input_with_timeout(None, timeout)
            current_state, output, timeout, exit = controller.accept_condition(
                current_state, condition, "test")
        except TimeoutError:
            current_state, output, timeout, exit = controller.accept_condition(
                current_state, "<on_timeout>", "test")
