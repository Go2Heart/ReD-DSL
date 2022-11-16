import os
import sys
import jwt
from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
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


app = Flask(__name__)
#app.debug = True
#app.secret_key = 'development key'
#toolbar = DebugToolbarExtension(app)

lexer = Lexer()
parser = Parser(lexer, debug=False)
with open("test.txt", "r") as f:
    script = f.read()
controller = Controller(lexer, parser, script, debug=True)
controller.register("test", "test")
input_string = ""


@app.route("/")
def connect():
    """
        @brief: this is the connection test
    """
    username = "test"
    token = jwt.encode({"username": username}, "secret", algorithm="HS256")  
    return jsonify({"username": username, "token": token }), 200

@app.route("/send")
@cross_origin()
def send():
    """
        @brief: this is the send api
        @param: {"msg": "some message", "state": "current_state", "token": "some token"}
        @return {"msg": "some message", "state": "next_state", "exit": "true/false"}
        @note: if the token is invalid, return 400
    """
    try:
        msg = request.args["msg"]
        state = request.args["state"]
        token = request.args["token"]
        user = jwt.decode(token, "secret", algorithms=["HS256"])
        if state is None or state == '':
            state = controller.state_machine.initial_state
        
        next_state, output = controller.accept_condition(state, msg, user["username"])
        print(output)
    except Exception as e:
        abort(400)
        pass
    #return {"msg":output, "next_state": next_state}
    return jsonify({"msg":output, "next_state": next_state}), 200