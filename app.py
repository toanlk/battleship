# -*- coding: utf-8 -*-
import os, sys

from flask import Flask
from flask import request

from module.position import Position

APP_PATH = os.getcwd()

app = Flask(__name__)

# -----------------------------------------------------------------------------------------------------
@app.route("/game-over", methods=["POST"])
def game_over():
    data = request.json
    return { 'success': True }

# -----------------------------------------------------------------------------------------------------
@app.route("/notify", methods=["POST"])
def notify():
    data = request.json
    return data

# -----------------------------------------------------------------------------------------------------
@app.route("/shoot", methods=["POST"])
def shoot():
    data = request.json
    return data

# -----------------------------------------------------------------------------------------------------
@app.route("/place-ships", methods=["POST"])
def place_ships():
    # html = open(APP_PATH + '/cache/data.html', 'r').read()
    pos = Position(inviteRequest['ships'])
    positions = pos.generate()
    return data

# -----------------------------------------------------------------------------------------------------
@app.route("/invite", methods=["POST"])
def invite():
    data = request.json
    print(data)
    return { 'success': True }

@app.route("/")
def index():
    print(request.headers['X-Session-Id'])
    return "Moemoe Tonton"

# -----------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        app.run(debug=True)
        app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
    except Exception as e:
        pass