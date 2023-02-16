# -*- coding: utf-8 -*-
import os, sys
import random, pprint, json

SHIP_TYPE = {
        "CV": 5, # Carrier
        "BB": 4, # Battleship
        "OR": 4, # Oil rig
        "CA": 3, # Cruiser
        "DD": 2, # Destroyer
    }

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
        "quantity": 1
        },
        {
        "type": "OR",
        "quantity": 1
        },
        {
        "type": "CA",
        "quantity": 1
        },
        {
        "type": "DD",
        "quantity": 2
        }
        ]
    }

def draw_map_with_ship(size_x, size_y, ships):
    # Initialize the map
    map = [['.' for x in range(size_y)] for y in range(size_x)]

    for ship in ships:
        for pos in ship['coordinates']:
            try:
                map[pos[0]][pos[1]] = 'x'
            except:
                pprint.pprint(pos)
                pass
            

    # Draw the map
    for i in range(size_x):
        for j in range(size_y):
            print(map[i][j], end=" ")
        print()

def generate_position(ship_type, all_position):
    positions = []
    is_exist = False

    size = SHIP_TYPE.get(ship_type, [])
    
    while not is_exist:
        positions = generate_position_randomly(size)
        print(ship_type)
        print(positions)
        for pos in positions:
            if pos in all_position:
                is_exist = False
                break
        is_exist = True

    return positions

def generate_position_randomly(size):
    positions = []

    # odd for horizontal and even for vertical
    # pick row and column
    direction = random.randint(1, size)
                                            
    row = random.randint(0, 7)
    col = random.randint(0, 19)
    if (direction % 2 != 0) :
        # left first, then right
        if (row - size > 0):
            for i in range(0, size):
                positions.append([row - i, col])
        else: # row
            for i in range(0, size):
                positions.append([row + i, col])
    else:
        # top first, then bottom
        if (col - size > 0):
            for i in range(0, size):
                positions.append([row, col - i])
        else: # row
            for i in range(0, size):
                positions.append([row, col + i])

    return positions

def get_ships(request_ships):
    positions = []
    all_position = []

    for ship in request_ships:
        position = generate_position(ship['type'], all_position)
        positions.append({'coordinates': position, 'type': ship['type']})
        all_position.extend(position)

    return positions

# -----------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    os.system('clear')

    positions = get_ships(inviteRequest['ships'])

    draw_map_with_ship(inviteRequest['boardHeight'], inviteRequest['boardWidth'], positions)