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


secret = "secret"




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
    token = jwt.encode({"username": username}, secret, algorithm="HS256")  
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
        user = jwt.decode(token, secret, algorithms=["HS256"])
        if state is None or state == '':
            state = controller.state_machine.initial_state
        
        next_state, output = controller.accept_condition(state, msg, user["username"])
        print(output)
    except Exception as e:
        print(e)
        return jsonify({"msg": "An exception has taken place, please try again!"}), 400
    return jsonify({"msg":output, "next_state": next_state}), 200

@app.route("/register")
@cross_origin()
def register():
    """
        @brief: this is the register api
        @param: {"username" : "some username", "password": "some password"}
        @return {"username": "some username", "token": "some token"}
        @note: if the username is already taken, return 400
    """
    try:
        username = request.args["username"]
        password = request.args["password"]
        controller.register(username, password)
        token = jwt.encode({"username": username}, secret, algorithm="HS256")
        msg = "Welcome to the game, " + username + "!"
    except Exception as e:
        print(e)
        return jsonify({"msg": str(e)}), 400
    return jsonify({"username": username, "token": token , "msg": msg}), 200

@app.route("/login")
@cross_origin()
def login():
    """
        @brief: this is the login api
        @param: {"username" : "some username", "password": "some password"}
        @return {"username: "some username", "token": "some token"}
        @note: if the username or password is wrong, return 400
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
    return jsonify({"username": username, "token": token ,"msg": msg}), 200