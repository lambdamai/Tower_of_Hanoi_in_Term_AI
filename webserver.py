#!/usr/bin/env python3
import sys
from flask import app, jsonify, Flask

app = Flask(__name__)
game = None

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/get_game_state')
def get_state():
    f = { "board1": game.pyramids }
    return jsonify(**f)
   
def run(game_):
    global game
    if game_:
        game = game_
        app.run()
    else: raise Exception('Game is Undefined')

if __name__ == '__main__':
    print(sys.argv[0])
    app.run()
