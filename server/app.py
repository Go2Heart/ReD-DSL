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

Copyright (c) 2022 Yibin Yan
"""
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import jwt
import json
from flask import Flask, jsonify, request
from flask_cors import cross_origin
from server.yacc import Parser
from server.lexer import Lexer
from server.controller import Controller


secret = "secret"
port = 5000


app = Flask(__name__)

try:
    lexer = Lexer()
    parser = Parser(lexer, debug=False)
    config: dict = json.load(open("config.json", "r"))
    secret = config["key"]
    port = config["port"]
    db_path = config["db_path"]
    script_path = config["script_path"]
    with open(script_path, "r") as f:
        script = f.read()
    controller = Controller(lexer, parser, script, db_path, debug=False)
    controller.register("test", "test")
    input_string = ""
except SyntaxError as e:
    print(e)
    exit(1)


@app.route("/send")
@cross_origin()
def send():
    """this is the send api
    Args:
        Http GET Message: {"msg": "some message", "state": "current_state", "token": "some token"}
        
    Returns:
        {"msg": "some message", "state": "next_state", "timeout": "timeout_value", "exit": "True/False"} and HTTP status code 200
    
    Raises:    
        if exception occurs, return HTTP Error 500 with error message
    """
    try:
        msg = request.args["msg"]
        state = request.args["state"]
        token = request.args["token"]
        user = jwt.decode(token, secret, algorithms=["HS256"])
        if state is None or state == '':
            state = controller.state_machine.initial_state

        next_state, output, timeout, exit = controller.accept_condition(
            state, msg, user["username"])
    except Exception as e:
        print(e)
        return jsonify({"msg": "An exception has taken place, please try again!\n The error info:" + str(e) + '\n'}), 500
    return jsonify({"msg": output, "next_state": next_state, "timeout": timeout, "exit": exit}), 200


@app.route("/register")
@cross_origin()
def register():
    """this is the register api
    
    Args:
        Http GET Message:{"username" : "some username", "password": "some password"}
    
    Returns:
        {"token": "some token", "msg": "welcome message"} and HTTP status code 200
        
    Raises:
        if the username is already taken, return HTTP Error 403 with error message
    """
    try:
        username = request.args["username"]
        password = request.args["password"]
        controller.register(username, password)
        token = jwt.encode({"username": username}, secret, algorithm="HS256")
        msg = "Welcome to the game, " + username + "!"
    except Exception as e:
        print(e)
        return jsonify({"msg": str(e)}), 403
    return jsonify({"token": token, "msg": msg}), 200


@app.route("/login")
@cross_origin()
def login():
    """this is the login api
    
    Args:
        Http GET Message:{"username" : "some username", "password": "some password"}
        
    Returns:
        {"token": "some token", "msg": "welcome message"} and HTTP status code 200
        
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
    return jsonify({"token": token, "msg": msg}), 200


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=port)
