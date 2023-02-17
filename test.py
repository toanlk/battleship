# -*- coding: utf-8 -*-
import os, sys
import random, pprint, json

from module.map import Map
from module.position import Position

inviteRequest =  {
    "boardWidth": 20,
    "boardHeight": 8,
    "ships": [
            {
            "type": "CV",
            "quantity": 1
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
    # pprint.pprint(positions)

    map = Map(inviteRequest['boardHeight'], inviteRequest['boardWidth'])
    map.draw(positions)