from lexer import Lexer
from parser import Parser


class StateMachine:
    def __init__(self, lexer, parser):
        self._lexer = lexer
        self._parser = parser
        self._variables = {}
        self._timeout = 0
        self._timeout_var = None
        self._timeout_state = None
        self._timeout_count = 0
        self._default_state = None
        self._exit_state = None

        self._current_state = None
        self._states = {}
        self._events = {}
        self._actions = {state: {} for state in self._states}

    def _add_state(self, state):
        self._states[state.name] = state

    def _add_event(self, event):
        self._events[event.name] = event

    def _add_action(self, cur_state, next_state, action):
        self._actions[action.state][action.event] = action
