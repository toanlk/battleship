# -*- coding: utf-8 -*-
import os

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

# -----------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    os.system('clear')

    draw_map_with_ship(8, 20, 5, 5, 5, 'horizontal')