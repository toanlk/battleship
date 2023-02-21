# -*- coding: utf-8 -*-
import os, sys, json, pprint

from flask import Flask
from flask import request

from module.bot import Bot
from module.position import Position

APP_PATH = os.getcwd()

app = Flask(__name__)

def read_file(session_id):
    data =[]
    with open("cache/" + session_id + ".json", 'r') as file:
        data = json.load(file)
    return data

def save_file(session_id, data):
    with open("cache/" + session_id + ".json", "w") as outfile:
        outfile.write(data)

# -----------------------------------------------------------------------------------------------------
@app.route("/game-over", methods=["POST"])
def game_over():
    data = request.json
    session_id = request.headers['X-Session-Id']
    try:
        save_file(session_id + "_game_over", data)
    except:
        pass
    
    return { 'success': True }

# -----------------------------------------------------------------------------------------------------
@app.route("/notify", methods=["POST"])
def notify():
    data = request.json
    session_id = request.headers['X-Session-Id']

    try:
        notify_data = read_file(session_id + "_notify")
        if notify_data:
            notify_data.append(data)
            save_file(session_id + "_notify", notify_data)
        else:
            save_file(session_id + "_notify", data)
    except:
        pass

    return { 'success': True }

# -----------------------------------------------------------------------------------------------------
@app.route("/shoot", methods=["POST"])
def shoot():
    data = request.json

    session_id = request.headers['X-Session-Id']
    json_object = read_file(session_id)

    shot_map = []
    if 'shot_map' in json_object:
        shot_map = json_object['shot_map']
        
    bot = Bot()

    fire_position = []
    for i in range(0, data['maxShots']):
        pos = bot.guess_random(shot_map)
        fire_position.append(pos)

    shot_map.extend(fire_position)
    json_object['shot_map'] = shot_map
    save_file(session_id, json.dumps(json_object))
    
    return {"coordinates" : fire_position}

# -----------------------------------------------------------------------------------------------------
@app.route("/place-ships", methods=["POST"])
def place_ships():
    session_id = request.headers['X-Session-Id']
    json_object = read_file(session_id)

    pos = Position(json_object['ships'])
    positions = pos.generate()

    return {"ships": positions}

# -----------------------------------------------------------------------------------------------------
@app.route("/invite", methods=["POST"])
def invite():
    # Store invite
    json_object = json.dumps(request.json, indent=4)
    session_id = request.headers['X-Session-Id']

    try:
        save_file(session_id, json_object)
    except:
        pass
    
    return { 'success': True }

@app.route("/")
def index():
    print(request.headers['X-Session-Id'])
    return "Moemoe Tonton"

# -----------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        os.system('clear')

        app.run(debug=True)
        app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
    except Exception as e:
        pass