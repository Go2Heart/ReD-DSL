import os
import sys
import jwt
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'