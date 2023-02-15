# -*- coding: utf-8 -*-
import os
import json
import random, pprint

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

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def draw_map_with_ship(size_x, size_y, ship_size, ship_x, ship_y, direction):
    # Initialize the map
    map = [['.' for x in range(size_y)] for y in range(size_x)]
    if direction == "horizontal":
        # Place ship horizontally
        if ship_x + ship_size <= size_y:
            for i in range(ship_x, ship_x + ship_size):
                map[ship_y][i] = '*'
    else:
        # Place ship vertically
        if ship_y + ship_size <= size_x:
            for i in range(ship_y, ship_y + ship_size):
                map[i][ship_x] = '*'

    # Draw the map
    for i in range(size_x):
        for j in range(size_y):
            print(map[i][j], end=" ")
        print()

def generate_position(size, all_position):
    positions = []
    is_exist = False
    positions = generate_position_randomly(size)

    # do
    # {
    #     positions = GeneratePositionRandomly(size);
    #     IsExist = positions.Where(AP => AllPosition.Exists(ShipPos => ShipPos.x == AP.x && ShipPos.y == AP.y)).Any();
    # }
    # while (IsExist);

    # AllPosition.AddRange(positions);

    return positions

def generate_position_randomly(size):
    positions = []

    # odd for horizontal and even for vertical
    # pick row and column
    direction = random.randint(1, size)
                                            
    row = random.randint(1, 11)
    col = random.randint(1, 11)
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

    all_position = []

    ships = {
        "CV": 5,
        "BB": 4,
        "OR": 4,
        "CA": 3,
        "DD": 2,
    }

    for ship in request_ships:
        size = ships.get(ship['type'], [])
        position = generate_position(size, all_position)
        all_position.append(position)

    return all_position

# -----------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    os.system('clear')

    # Destroyer: 2x1
    # Cruiser: 3x1
    # Carrier: 5x1
    # Oil rig: 2x2
    # Battleship: 4x1

    # draw_map_with_ship(inviteRequest['boardHeight'], inviteRequest['boardWidth'], 5, 5, 5, 'horizontal')
    positions = get_ships(inviteRequest['ships'])
    pprint.pprint(positions)