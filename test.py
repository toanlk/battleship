# -*- coding: utf-8 -*-
import os, sys
import random, pprint, json
import numpy as np

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

    map = Map(inviteRequest['boardHeight'], inviteRequest['boardWidth'])

    pos = Position(inviteRequest['ships'])
    positions = pos.generate()

    ship_map = np.zeros([inviteRequest['boardWidth'], inviteRequest['boardHeight']])
    for item in positions:
        for s_pos in item['coordinates']:
            ship_map[s_pos[0], s_pos[1]] = 1

    bot = Bot(inviteRequest['boardHeight'], inviteRequest['boardWidth'])

    hit_rate = 0
    shot_map = np.zeros([inviteRequest['boardWidth'], inviteRequest['boardHeight']])
    simple_shot_map = []
    targets = []
    potential_targets = []

    while hit_rate < 100:
        guess_row, guess_col, potential_targets = bot.hunt_target(targets, potential_targets, shot_map)

        shot_map[guess_row][guess_col] = 1
        simple_shot_map.append([guess_row, guess_col])
        if ship_map[guess_row, guess_col] == 1:
            is_sunk, ship_hit = map.is_sunk_ship(positions, simple_shot_map, guess_row, guess_col)
            targets, potential_targets = bot.target_hit(guess_row, guess_col, is_sunk, ship_hit, targets, potential_targets, shot_map)

        hit_rate = map.hit_rate(positions, simple_shot_map)

    # shot_map = []
    pprint.pprint(positions)
    # pprint.pprint(simple_shot_map)
    map.draw(positions, simple_shot_map)