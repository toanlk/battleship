# -*- coding: utf-8 -*-
import os, sys
import random, pprint, json

from module.bot import Bot
from module.map import Map
from module.position import Position

inviteRequest =  {
    "boardWidth": 20,
    "boardHeight": 8,
    "ships": [
            {
            "type": "CV",
            "quantity": 2
            },
            {
            "type": "BB",
            "quantity": 2
            },
            {
            "type": "OR",
            "quantity": 1
            },
            {
            "type": "CA",
            "quantity": 2
            },
            {
            "type": "DD",
            "quantity": 2
            }
        ]
    }

def get_ships(request_ships):
    positions = []
    all_position = []

    for ship in request_ships:
        for i in range(0, ship['quantity']):
            pos = Position()
            position = pos.generate_position(ship['type'], all_position)
            positions.append({'coordinates': position, 'type': ship['type']})
            all_position.extend(position)

    return positions

# -----------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    os.system('clear')

    pos = Position(inviteRequest['ships'])
    positions = pos.generate()
    pprint.pprint(positions)

    bot = Bot(inviteRequest['boardHeight'], inviteRequest['boardWidth'])

    shot_map = []
    for i in range(0, 150):
        fire_position = bot.guess_random(shot_map)
        shot_map.append(fire_position)

    # shot_map = []
    map = Map(inviteRequest['boardHeight'], inviteRequest['boardWidth'])
    map.draw(positions, shot_map)