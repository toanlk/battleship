# -*- coding: utf-8 -*-
import os, sys, json, pprint
import numpy as np

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

        print("Notify: ")
        print(data)

        if data['shots']['status'] == "HIT":
            json_object = read_file(session_id)

            is_sunk = False
            if len(data['sunkShips']) > 0:
                is_sunk = True
            
            guess_row = data['shots']['coordinate'][0]
            guess_col = data['shots']['coordinate'][1]
            shot_map = np.array(json_object['shot_map'])
            targets, potential_targets = bot.target_hit(guess_row, guess_col, is_sunk, data['sunkShips']['coordinates'], json_object['targets'], json_object['potential_targets'], shot_map)
            json_object['targets'] = targets
            json_object['potential_targets'] = potential_targets

            save_file(session_id, json.dumps(json_object))

        notify_data = read_file(session_id + "_notify")
        if notify_data:
            notify_data.append(data)
            save_file(session_id + "_notify", notify_data)
        else:
            save_file(session_id + "_notify", data)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        pass

    return { 'success': True }

# -----------------------------------------------------------------------------------------------------
@app.route("/shoot", methods=["POST"])
def shoot():
    data = request.json

    session_id = request.headers['X-Session-Id']
    json_object = read_file(session_id)

    targets = []
    if 'targets' in json_object:
        targets = json_object['targets']

    potential_targets = []
    if 'potential_targets' in json_object:
        potential_targets = json_object['potential_targets']

    shot_map = np.zeros([json_object['boardWidth'], json_object['boardHeight']])
    if 'shot_map' in json_object:
        shot_map = np.array(json_object['shot_map'])

    simple_shot_map = []
    if 'simple_shot_map' in json_object:
        simple_shot_map = json_object['simple_shot_map']
        
    bot = Bot()

    fire_position = []
    for i in range(0, data['maxShots']):
        # pos = bot.guess_random(shot_map)
        # fire_position.append(pos)

        guess_row, guess_col, potential_targets = bot.hunt_target(targets, potential_targets, shot_map)
        fire_position.append([guess_row, guess_col])

        print("Shoot: " + str(fire_position))

        shot_map[guess_row][guess_col] = 1
        simple_shot_map.append([guess_row, guess_col])

    simple_shot_map.extend([guess_row, guess_col])
    json_object['simple_shot_map'] = simple_shot_map
    json_object['shot_map'] = shot_map.tolist()
    json_object['targets'] = targets
    json_object['potential_targets'] = potential_targets

    save_file(session_id, json.dumps(json_object))
    
    return {"coordinates" : fire_position}

# -----------------------------------------------------------------------------------------------------
@app.route("/place-ships", methods=["POST"])
def place_ships():
    session_id = request.headers['X-Session-Id']
    json_object = read_file(session_id)

    pos = Position(json_object['ships'])
    positions = pos.generate()
    pprint.pprint(positions)

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
        if os.name == 'nt':
            os.system('cls')
            app.run(debug=True)
            app.run(host="10.10.2.58", port=5000, debug=False, threaded=True)

        else:
            os.system('clear')

            app.run(debug=True)
            app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
    except Exception as e:
        pass