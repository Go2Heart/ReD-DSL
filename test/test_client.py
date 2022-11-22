from flask import Flask, jsonify, request, abort
from flask_cors import cross_origin

app = Flask(__name__)

state = "start"
exit = False
timeout = 999
user = "test"
user_dict = {"test": "test"}


@app.route('/register')
@cross_origin()
def register():
    try:
        username = request.args['username']
        password = request.args['password']
        msg = 'Welcome to the game, ' + username + '!'
        global user
        if username not in user_dict:
            user = username
            user_dict[username] = password
        else:
            username = None
            raise Exception('Username already taken')
    except Exception as e:
        print(e)
        return jsonify({'msg': str(e)}), 403
    return jsonify({'token': username, 'msg': msg}), 200

@app.route('/login')
@cross_origin()
def login():
    try:
        username = request.args['username']
        password = request.args['password']
        msg = 'Welcome back, ' + username + '!'
        global user
        if username not in user_dict:
            username = None
            raise Exception('User not found')
        elif user_dict[username] != password:
            username = None
            raise Exception('Wrong password')
    except Exception as e:
        print(e)
        return jsonify({'msg': str(e)}), 400
    return jsonify({'token': username, 'msg': msg}), 200

@app.route('/send')
@cross_origin()
def send():
    try:
        token = request.args['token']
        msg = request.args['msg']
        global user
        if token != user:
            abort(403)
        if msg == 'exit':
            global exit
            output = 'Bye!'
            exit = True
        elif msg == 'hello':
            output = 'Hello, ' + user + '!'
        elif msg == '<on_enter>':
            output = 'Input [hello] to say hello to me.\n Input [exit] to exit the game.\n'
        else:
            output = 'I don\'t understand.'
        return jsonify({'msg': output, 'next_state': state, 'timeout': 999, 'exit': exit}), 200
    except Exception as e:
        return jsonify({'msg': 'An exception has taken place, please try again!\n The error info:' + str(e) + '\n'}), 500
    
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=9001)