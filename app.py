"""This is the backend of the application.

It is responsible for the following:
    1. Parsing the script
    2. Generating the AST
    3. Constructing the state machine and action table
    4. Handling the user input
    5. Executing the action table
    6. Sending the output to the frontend

It uses RESTful API to communicate with the frontend.
Every time the frontend sends a request to the backend, the backend will
return a JSON object containing the corresponding fields.
"""

import os
import sys
import jwt
from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
from yacc import Parser, ASTNode
from lexer import Lexer
from interpreter import StateMachine, CallBack
from controller import Controller
import select
import sys


secret = "secret"


app = Flask(__name__)


lexer = Lexer()
parser = Parser(lexer, debug=False)
with open("test.txt", "r") as f:
    script = f.read()
controller = Controller(lexer, parser, script, debug=True)
controller.register("test", "test")
input_string = ""


@app.route("/")
@cross_origin()
def connect():
    """this is the connection test"""
    username = "test"
    token = jwt.encode({"username": username}, secret, algorithm="HS256")
    return jsonify({"username": username, "token": token}), 200


@app.route("/send")
@cross_origin()
def send():
    """this is the send api
    Args:
        Http GET Message: {"msg": "some message", "state": "current_state", "token": "some token"}
        
    Returns:
        {"msg": "some message", "state": "next_state", "exit": "true/false"} and HTTP status code 200
    
    Raises:    
        if the token is invalid, return HTTP Error 401 with error message
    """
    try:
        msg = request.args["msg"]
        state = request.args["state"]
        token = request.args["token"]
        user = jwt.decode(token, secret, algorithms=["HS256"])
        if state is None or state == '':
            state = controller.state_machine.initial_state

        next_state, output, timeout = controller.accept_condition(
            state, msg, user["username"])
    except Exception as e:
        print(e)
        return jsonify({"msg": "An exception has taken place, please try again!\n The error info:" + str(e) + '\n'}), 401
    return jsonify({"msg": output, "next_state": next_state, "timeout": timeout}), 200


@app.route("/register")
@cross_origin()
def register():
    """this is the register api
    
    Args:
        Http GET Message:{"username" : "some username", "password": "some password"}
    
    Returns:
        {"username": "some username", "token": "some token"}
        
    Raises:
        if the username is already taken, return HTTP Error 401 with error message
    """
    try:
        username = request.args["username"]
        password = request.args["password"]
        controller.register(username, password)
        token = jwt.encode({"username": username}, secret, algorithm="HS256")
        msg = "Welcome to the game, " + username + "!"
    except Exception as e:
        print(e)
        return jsonify({"msg": str(e)}), 401
    return jsonify({"username": username, "token": token, "msg": msg}), 200


@app.route("/login")
@cross_origin()
def login():
    """this is the login api
    
    Args:
        Http GET Message:{"username" : "some username", "password": "some password"}
        
    Returns:
        {"username: "some username", "token": "some token"}
        
    Raises:
        if the username or password is wrong, return 400 with error message
    """
    try:
        username = request.args["username"]
        password = request.args["password"]
        controller.login(username, password)
        token = jwt.encode({"username": username}, secret, algorithm="HS256")
        msg = "Welcome back, " + username + "!"
    except Exception as e:
        print(e)
        return jsonify({"msg": str(e)}), 400
    return jsonify({"username": username, "token": token, "msg": msg}), 200


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=9001)
